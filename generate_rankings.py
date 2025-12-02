import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from time import sleep 
import sys 
import re 

session = requests.Session()
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
})

# ===============================================
# CONFIGURAÇÕES GLOBAIS
# ===============================================

MAX_PAGES = 10 
GUILD_URL = "https://miracle74.com/?subtopic=guilds&action=show&guild=600" 

SKILLS = {
    'experience': 'Level / Exp',
    'sword': 'Sword',
    'axe': 'Axe',
    'club': 'Club',
    'dist': 'Distance',
    'maglevel': 'Magic Level',
    'shielding': 'Shielding',
    'fishing': 'Fishing',
    'mage_skill': 'Mage Combat Skills', 
    'mage_defense': 'Mage Defense Skills', 
}

# ===============================================
# FUNÇÕES DE UTILIDADE E SCRAPING
# ===============================================

def _get_names_from_guild_url(url):
    """Busca nomes na tabela principal de membros da guilda."""
    try:
        # Tenta a requisição
        resp = session.get(url, timeout=15)
        resp.raise_for_status()

        # O restante da lógica de scraping da guild...
        soup = BeautifulSoup(resp.content, "html.parser")
        guild_table = soup.find("table", class_="TableContent") 
        nomes = []

        if guild_table:
            rows = guild_table.find_all("tr", recursive=False)[1:]
            for row in rows:
                tds = row.find_all("td")
                if len(tds) > 1:
                    name_cell = tds[1] 
                    link = name_cell.find("a", href=lambda href: href and "subtopic=characters" in href)
                    
                    if link and link.text.strip():
                        nome = link.text.strip()
                        if nome and "guild" not in nome.lower(): 
                            nomes.append(nome)
                            
        return list(set(nomes)) 

    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao buscar lista da guild: {e}") 
        return []
    except Exception as e:
        print(f"ERRO: Falha desconhecida ao processar página da guild: {e}")
        return []

def _scrape_highscores_page(skill, page, vocation_id=None):
    """Executa a requisição HTTP e retorna a tabela de highscores."""
    
    vocation_param = f"&vocation={vocation_id}" if vocation_id else ""
    url = f"https://miracle74.com/?subtopic=highscores&list={skill}&page={page}{vocation_param}"
    
    try:
        sleep(1.5) # Pausa ESSENCIAL
        
        # Faz a requisição com encoding definido
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
        
        # Tenta decodificar como UTF-8
        resp.encoding = 'utf-8' 
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        tables = soup.find_all('table', class_='TableContent')
        if len(tables) < 2:
             return None 
             
        return tables[1] 

    except requests.exceptions.RequestException as e:
        print(f"ERRO DE REQUISIÇÃO (Pág {page}): {url} - {e}")
        return None
    except Exception as e:
        print(f"ERRO DE PARSING (Pág {page}): {e}")
        return None

def _filter_and_save(skill_key, guild_names, all_highscores, value_name):
    """Função auxiliar para filtrar, ordenar e salvar o resultado final em JSON."""
    
    guild_names_lower = {name.lower() for name in guild_names} 
    nomes_em_comum = []
    
    for entry in all_highscores:
        if entry["nome"].lower() in guild_names_lower:
            nomes_em_comum.append(entry)

    def sort_key(entry):
        cleaned_value = str(entry['order_value']).replace(',', '').replace('.', '').replace(' ', '')
        try:
            return int(cleaned_value)
        except ValueError:
            return 0 
        
    try:
        nomes_em_comum.sort(key=sort_key, reverse=True) 
    except Exception:
        pass 
    
    # --- SALVAR EM JSON ---
    json_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "skill_name": SKILLS[skill_key],
        "value_type": value_name,
        "ranking": []
    }
    
    if nomes_em_comum:
        for rank_na_guild, entry in enumerate(nomes_em_comum, start=1):
            json_data["ranking"].append({
                "rank_guild": rank_na_guild,
                "nome": entry['nome'],
                "valor": entry['display_value'],
            })

    try:
        file_name = f"ranking_{skill_key}.json"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print(f"JSON '{file_name}' salvo com sucesso.")
        
    except Exception as e:
        print(f"ERRO FATAL ao salvar JSON: {e}")

# ===============================================
# LÓGICA DE RANKING - BASE E AGREGADA
# ===============================================

def rankear_guild_por_skill(skill_key, guild_names):
    """Busca e filtra o ranking para skills individuais (e.g., sword, exp)."""
    
    all_highscores = []
    
    # --- DEFINIÇÃO DOS ÍNDICES DE EXTRAÇÃO ---
    NAME_INDEX = 2
    
    if skill_key == 'experience':
        VALUE_INDEX = 4
        ORDER_INDEX = 5
        VALUE_NAME = "Level"
    else:
        VALUE_INDEX = 5
        ORDER_INDEX = 5
        VALUE_NAME = "Skill"
    
    # --- 1. COLETA DOS DADOS (Páginas 1 a 10) ---
    for page in range(1, MAX_PAGES + 1):
        
        table = _scrape_highscores_page(skill_key, page)
        if table is None:
            break
        
        for tr in table.find_all("tr", bgcolor=True):
            tds = tr.find_all("td")
            
            if len(tds) > ORDER_INDEX: 
                nome_tag = tds[NAME_INDEX].find("a")
                
                if nome_tag:
                    nome = nome_tag.text.strip()
                    value_to_display = tds[VALUE_INDEX].text.strip()
                    value_to_order = tds[ORDER_INDEX].text.strip()
                    
                    all_highscores.append({
                        "nome": nome, 
                        "display_value": value_to_display, 
                        "order_value": value_to_order
                    })

    _filter_and_save(skill_key, guild_names, all_highscores, VALUE_NAME)


def rankear_mage_skills(guild_names, skill_key):
    """Busca 60 páginas (3 weapons x 2 vocations x 10 pages) e agrega o melhor skill. (COMBATE)"""
    
    mage_data = {} 
    weapons = ['sword', 'club', 'axe']
    vocations = {1: 'Sorcerer', 2: 'Druid'} 
    
    NAME_INDEX = 2
    SKILL_VALUE_INDEX = 5 

    for weapon in weapons:
        for vocation_id in vocations.keys():
            for page in range(1, MAX_PAGES + 1):
                
                table = _scrape_highscores_page(weapon, page, vocation_id=vocation_id)
                if table is None:
                    continue
                
                for row in table.find_all('tr', bgcolor=True):
                    cells = row.find_all('td')
                    if len(cells) <= SKILL_VALUE_INDEX: continue 
                    
                    name_tag = cells[NAME_INDEX].find('a')
                    if not name_tag: continue
                    name = name_tag.text.strip()
                    
                    skill_value_str = cells[SKILL_VALUE_INDEX].text.strip().replace(',', '').replace('.', '').replace(' ', '')
                    try:
                        skill_value = int(skill_value_str) 
                    except ValueError:
                        continue 
                    
                    if name not in mage_data:
                        mage_data[name] = {
                            'name': name,
                            'best_skill_value': skill_value,
                            'best_skill_name': weapon.capitalize(),
                            'order_value': skill_value 
                        }
                    else:
                        current_best = mage_data[name]['order_value']
                        if skill_value > current_best:
                            mage_data[name]['best_skill_value'] = skill_value
                            mage_data[name]['best_skill_name'] = weapon.capitalize()
                            mage_data[name]['order_value'] = skill_value
        
    all_highscores = []
    for name, data in mage_data.items():
        all_highscores.append({
            "nome": data['name'],
            "display_value": f"{data['best_skill_value']} ({data['best_skill_name']})",
            "order_value": data['order_value'] 
        })
    
    _filter_and_save(skill_key, guild_names, all_highscores, "Skill")


def rankear_mage_defense(guild_names, skill_key):
    """Busca o ranking de Shielding para mages (Sorcerer e Druid) e filtra."""
    
    skill = 'shielding'
    all_highscores = []
    vocations = {1: 'Sorcerer', 2: 'Druid'} 
    
    NAME_INDEX = 2
    SKILL_VALUE_INDEX = 5 

    for vocation_id in vocations.keys():
        for page in range(1, MAX_PAGES + 1):
            
            table = _scrape_highscores_page(skill, page, vocation_id=vocation_id)
            if table is None:
                continue
                
            for row in table.find_all('tr', bgcolor=True):
                cells = row.find_all('td')
                if len(cells) <= SKILL_VALUE_INDEX: continue 
                
                name_tag = cells[NAME_INDEX].find('a')
                if not name_tag: continue
                name = name_tag.text.strip()
                
                skill_value_str = cells[SKILL_VALUE_INDEX].text.strip().replace(',', '').replace('.', '').replace(' ', '')
                try:
                    skill_value = int(skill_value_str) 
                except ValueError:
                    continue 
                
                all_highscores.append({
                    "nome": name,
                    "display_value": str(skill_value),
                    "order_value": skill_value
                })

    _filter_and_save(skill_key, guild_names, all_highscores, "Skill")


# ===============================================
# FUNÇÃO PRINCIPAL DE EXECUÇÃO DA AUTOMACAO
# ===============================================

def main():
    """Função principal que gerencia o fluxo de trabalho."""
    
    print("Iniciando geração de rankings. (Headless Mode)")
    print(f"Buscando nomes da guild em: {GUILD_URL}")
    guild_names = _get_names_from_guild_url(GUILD_URL)
    
    if not guild_names:
        print("ERRO: nenhum membro encontrado na guild. Encerrando.")
        sys.exit(1)
        
    print(f"{len(guild_names)} membros encontrados. Iniciando scraping sequencial...")
    
    # 2. Roda todos os rankings em ordem
    for skill_key in SKILLS.keys():
        print("-" * 30)
        
        if skill_key == 'mage_skill':
            print(f"Iniciando MAGE COMBATE (Agregação)...")
            rankear_mage_skills(guild_names, skill_key)
        elif skill_key == 'mage_defense':
            print(f"Iniciando MAGE DEFENSE (Shielding Agregação)...")
            rankear_mage_defense(guild_names, skill_key)
        else:
            print(f"Iniciando {SKILLS[skill_key]} (Individual)...")
            rankear_guild_por_skill(skill_key, guild_names)
            
    print("-" * 30)
    print("TODOS OS RANKINGS GERADOS COM SUCESSO.")


if __name__ == "__main__":
    # Este bloco será executado pelo GitHub Actions
    main()