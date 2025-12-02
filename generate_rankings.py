import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from time import sleep 
import sys 
import re 

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

HEADERS = {'User-Agent': 'Mozilla/5.0'}

# ===============================================
# FUNÇÕES DE UTILIDADE E SCRAPING
# ===============================================

def _get_names_from_guild_url(url):
    """Busca nomes na tabela principal de membros da guilda."""
    try:
        # Requisição direta, sem proxy
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.content, "html.parser")
        guild_table = soup.find("table", class_="TableContent") 
        guild_list = []
        seen_names = set()

        if guild_table:
            rows = guild_table.find_all("tr", recursive=False)[1:]
            for row in rows:
                tds = row.find_all("td")
                
                # A tabela da guild tem as colunas: 0=Rank#, 1=Nome, 2=Voc, 3=Lv, 4=Cargo
                if len(tds) > 4: 
                    name_cell = tds[1]
                    rank_cell = tds[4] 

                    link = name_cell.find("a", href=lambda href: href and "subtopic=characters" in href)
                    
                    if link and link.text.strip():
                        name = link.text.strip()
                        guild_rank = rank_cell.text.strip()
                        
                        # Garante que não há duplicatas, mantendo a ordem
                        if name not in seen_names:
                            seen_names.add(name)
                            guild_list.append({
                                "name": name,
                                "rank": guild_rank
                            })
                            
        return guild_list 

    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao buscar lista da guild: {e}") 
        return []
    except Exception as e:
        print(f"ERRO: Falha desconhecida ao processar página da guild: {e}")
        return []

def _save_member_list(guild_structured_list):
    """SALVA a lista de nomes e ranks da guild em um JSON separado para a página Home."""
    try:
        # Extrai apenas os nomes para a contagem, se necessário
        member_names = [member['name'] for member in guild_structured_list]
        
        json_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_members": len(guild_structured_list),
            "members": guild_structured_list # Lista estruturada com nome e rank
        }
        file_name = "members_list.json"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print(f"JSON '{file_name}' salvo com sucesso para a Home.")
    except Exception as e:
        print(f"ERRO FATAL ao salvar lista de membros JSON: {e}")

def _scrape_highscores_page(skill, page, vocation_id=None):
    """Executa a requisição HTTP e retorna a tabela de highscores."""
    
    vocation_param = f"&vocation={vocation_id}" if vocation_id else ""
    url = f"https://miracle74.com/?subtopic=highscores&list={skill}&page={page}{vocation_param}"
    
    try:
        sleep(1.5) # Pausa ESSENCIAL
        
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')
        
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

def _filter_and_save(skill_key, guild_names_for_filter, all_highscores, value_name):
    """Função auxiliar para filtrar, ordenar e salvar o resultado final em JSON."""
    
    guild_names_lower = {name.lower() for name in guild_names_for_filter} 
    nomes_em_comum = []
    
    for entry in all_highscores:
        if entry["nome"].lower() in guild_names_lower:
            nomes_em_comum.append(entry)

    def sort_key(entry):
        cleaned_value = entry['order_value'].replace(',', '').replace('.', '').replace(' ', '')
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

def rankear_guild_por_skill(skill_key, guild_names_for_filter):
    """Busca e filtra o ranking para skills individuais (e.g., sword, exp)."""
    
    all_highscores = []
    
    NAME_INDEX = 2
    
    if skill_key == 'experience':
        VALUE_INDEX = 4
        ORDER_INDEX = 5
        VALUE_NAME = "Level"
    else:
        VALUE_INDEX = 5
        ORDER_INDEX = 5
        VALUE_NAME = "Skill"
    
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

    _filter_and_save(skill_key, guild_names_for_filter, all_highscores, VALUE_NAME)


def rankear_mage_skills(guild_names_for_filter, skill_key):
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
    
    _filter_and_save(skill_key, guild_names_for_filter, all_highscores, "Skill")


def rankear_mage_defense(guild_names_for_filter, skill_key):
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

    _filter_and_save(skill_key, guild_names_for_filter, all_highscores, "Skill")


# ===============================================
# FUNÇÃO PRINCIPAL DE EXECUÇÃO DA AUTOMACAO
# ===============================================

def main():
    """Função principal que gerencia o fluxo de trabalho."""
    
    print("Iniciando geração de rankings. (Headless Mode)")
    print(f"Buscando nomes da guild em: {GUILD_URL}")
    guild_structured_list = _get_names_from_guild_url(GUILD_URL)
    
    if not guild_structured_list:
        print("ERRO: nenhum membro encontrado na guild. Encerrando.")
        sys.exit(1) # Sai com erro
        
    
    # 1. SALVA A LISTA ESTRUTURADA DE MEMBROS (Para a nova Home)
    _save_member_list(guild_structured_list)
    
    # 2. CRIA A LISTA SIMPLES DE NOMES (Para o filtro dos rankings)
    guild_names_for_filter = [member['name'] for member in guild_structured_list]
    
    print(f"{len(guild_names_for_filter)} membros encontrados. Iniciando scraping sequencial...")
    
    # 3. Roda todos os rankings em ordem
    for skill_key in SKILLS.keys():
        print("-" * 30)
        
        if skill_key == 'mage_skill':
            print(f"Iniciando MAGE COMBATE (Agregação)...")
            rankear_mage_skills(guild_names_for_filter, skill_key)
        elif skill_key == 'mage_defense':
            print(f"Iniciando MAGE DEFENSE (Shielding Agregação)...")
            rankear_mage_defense(guild_names_for_filter, skill_key)
        else:
            print(f"Iniciando {SKILLS[skill_key]} (Individual)...")
            rankear_guild_por_skill(skill_key, guild_names_for_filter)
            
    print("-" * 30)
    print("TODOS OS RANKINGS GERADOS COM SUCESSO.")


if __name__ == "__main__":
    main()