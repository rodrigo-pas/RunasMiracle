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

# Regex para extrair números (incluindo separadores de milhar)
NUM_RE = re.compile(r'(-?\d[\d\.,]*)') 


# ===============================================
# UTILITÁRIOS
# ===============================================

def _extract_number(s):
    """Extrai o primeiro número de uma string e retorna int (ou None)."""
    if not s:
        return None
    m = NUM_RE.search(s)
    if not m:
        return None
    num = m.group(1)
    # normalizar: remover pontos (milhar) e trocar vírgula por nada
    num = num.replace('.', '').replace(',', '')
    try:
        return int(num)
    except ValueError:
        return None

# ===============================================
# SCRAPING BORING STUFF
# ===============================================

def _get_names_from_guild_url(url):
    """Busca nomes na tabela da guild."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find('table', class_='TableContent')
        if not table:
            print("WARN: tabela da guild não encontrada.")
            return []
        rows = table.find_all('tr', recursive=False)[1:]
        nomes = []
        for r in rows:
            tds = r.find_all('td')
            if len(tds) >= 2:
                link = tds[1].find('a', href=lambda h: h and 'subtopic=characters' in h)
                if link:
                    nome = link.text.strip()
                    if nome and 'guild' not in nome.lower():
                        nomes.append(nome)
        return sorted(list(set(nomes)))
    except Exception as e:
        print(f"ERRO: falha ao buscar guild: {e}")
        return []


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
        
        # A tabela de Highscores é a SEGUNDA 'TableContent' (índice 1)
        if len(tables) < 2:
            # print(f"WARN: tabela de highscores não encontrada para {skill} página {page}.")
            return None
            
        return tables[1]
        
    except requests.exceptions.RequestException as e:
        print(f"ERRO REQ: {skill} pág {page}: {e}")
        return None
    except Exception as e:
        print(f"ERRO DE PARSING (Pág {page}): {e}")
        return None


# ===============================================
# PARSE GENÉRICO DE TABELA (ADAPTAÇÃO)
# ===============================================
def parse_highscore_table(table):
    """
    Tenta parsear a tabela de highscore com base em índices fixos (como no seu código)
    e retorna lista de dicts: {'nome':..., 'display_value':..., 'order_value': int}
    """
    
    # Índices fixos, baseado no seu código anterior:
    NAME_IDX = 2
    DISPLAY_IDX = 4
    ORDER_IDX = 5 # Skill Value / Total Experience
    
    results = []
    
    # Itera sobre linhas que têm cores de fundo (linhas de resultado)
    for r in table.find_all(['tr', 'tbody'], bgcolor=True):
        tds = r.find_all('td')
        
        # Garante que a linha tem colunas suficientes para os índices fixos
        if len(tds) <= max(NAME_IDX, DISPLAY_IDX, ORDER_IDX):
            continue

        # Pega Nome: procura <a> na célula do nome
        name = None
        try:
            a = tds[NAME_IDX].find('a')
            if a and a.text.strip():
                name = a.text.strip()
        except Exception:
            pass
            
        if not name:
            continue

        # Pega os valores
        display_raw = tds[DISPLAY_IDX].get_text(strip=True)
        order_raw = tds[ORDER_IDX].get_text(strip=True)

        # Normaliza o valor de ordenação para INT
        order_num = _extract_number(order_raw)
        if order_num is None:
            order_num = _extract_number(display_raw)

        results.append({
            'nome': name,
            'display_value': display_raw,
            'order_value': order_num if order_num is not None else 0
        })

    return results


# ===============================================
# FILTRAGEM E SALVAMENTO
# ===============================================
def _filter_and_save(skill_key, guild_names, all_highscores, value_name):
    guild_lower = {n.lower() for n in guild_names}
    filtrados = [e for e in all_highscores if e['nome'].lower() in guild_lower]

    # ORDENAR CORRETAMENTE (skill desc, nome asc)
    filtrados.sort(
        key=lambda e: (-e.get('order_value', 0), e['nome'].lower())
    )

    json_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "skill_name": SKILLS.get(skill_key, skill_key),
        "value_type": value_name,
        "ranking": [
            {"rank_guild": i, "nome": e['nome'], "valor": e['display_value']}
            for i, e in enumerate(filtrados, start=1)
        ]
    }

    fname = f"ranking_{skill_key}.json"
    try:
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print(f"Salvo: {fname} ({len(filtrados)} items)")
    except Exception as e:
        print(f"ERRO salvar JSON {fname}: {e}")



# ===============================================
# RANKERS
# ===============================================
def rankear_guild_por_skill(skill_key, guild_names):
    """Busca e filtra o ranking para skills individuais (e.g., sword, exp)."""
    all_highscores = []
    
    for page in range(1, MAX_PAGES + 1):
        table = _scrape_highscores_page(skill_key, page)
        if table is None:
            continue
        all_highscores.extend(parse_highscore_table(table))

    value_name = "Level" if skill_key == 'experience' else "Skill"
    _filter_and_save(skill_key, guild_names, all_highscores, value_name)


def rankear_mage_skills(guild_names, skill_key):
    """Busca 3 weapons x 2 vocations x 10 pages (Combate) e agrega o melhor skill."""
    
    mage_map = {} 
    weapons = ['sword', 'club', 'axe']
    vocations = [1, 2] # 1: Sorcerer/MS, 2: Druid/ED
    
    for weapon in weapons:
        for vocation_id in vocations:
            for page in range(1, MAX_PAGES + 1):
                
                table = _scrape_highscores_page(weapon, page, vocation_id=vocation_id)
                if table is None:
                    continue
                
                parsed = parse_highscore_table(table)
                
                for entry in parsed:
                    name = entry['nome']
                    order_val = entry['order_value']
                    
                    if isinstance(order_val, int):
                        
                        # Verifica se é o melhor valor encontrado até agora para este mage
                        if name not in mage_map or order_val > mage_map[name]['order_value']:
                            mage_map[name] = {
                                'nome': name,
                                'display_value': entry['display_value'] + f" ({weapon.capitalize()})",
                                'order_value': order_val
                            }
        
    all_highscores = list(mage_map.values())
    _filter_and_save(skill_key, guild_names, all_highscores, "Skill")


def rankear_mage_defense(guild_names, skill_key):
    """Busca o ranking de Shielding para mages (Sorcerer e Druid) e filtra."""
    
    all_highscores = []
    skill = 'shielding'
    vocations = [1, 2] # 1: Sorcerer/MS, 2: Druid/ED

    for vocation_id in vocations:
        for page in range(1, MAX_PAGES + 1):
            
            table = _scrape_highscores_page(skill, page, vocation_id=vocation_id)
            if table is None:
                continue
            
            parsed = parse_highscore_table(table)
            all_highscores.extend(parsed)

    _filter_and_save(skill_key, guild_names, all_highscores, "Skill")


# ===============================================
# MAIN
# ===============================================
def main():
    """Função principal que gerencia o fluxo de trabalho."""
    
    print("Iniciando geração de rankings...")
    guild_names = _get_names_from_guild_url(GUILD_URL)
    if not guild_names:
        print("ERRO: nenhum membro encontrado na guild. Saindo.")
        sys.exit(1)
    print(f"{len(guild_names)} membros encontrados.")

    # 2. Roda todos os rankings em ordem
    for skill_key in SKILLS.keys():
        print("-" * 40)
        print(f"Processando: {skill_key}")
        
        if skill_key == 'mage_skill':
            rankear_mage_skills(guild_names, skill_key)
        elif skill_key == 'mage_defense':
            rankear_mage_defense(guild_names, skill_key)
        else:
            rankear_guild_por_skill(guild_names, skill_key) # Chamada original

    print("Finalizado.")

if __name__ == "__main__":
    main()