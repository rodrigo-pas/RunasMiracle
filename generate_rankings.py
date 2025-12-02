import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from time import sleep 
import sys 
import re 

# ===============================================
# PROXIES AUTOMÁTICOS (lista que gira sozinha)
# ===============================================
PROXIES = [
    "http://103.152.232.122:8080",
    "http://8.219.97.248:80",
    "http://103.180.250.242:8080",
    "http://103.127.1.130:80",
    "http://104.129.194.35:10605",
]

proxy_index = 0

def get_next_proxy():
    global proxy_index
    proxy = PROXIES[proxy_index % len(PROXIES)]
    proxy_index += 1
    return {
        "http": proxy,
        "https": proxy
    }

# ===============================================
# SESSÃO GLOBAL COM USER-AGENT REAL
# ===============================================

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

def safe_request(url):
    """Tenta requisição com vários proxies até funcionar."""
    for _ in range(len(PROXIES)):
        proxy = get_next_proxy()
        try:
            resp = session.get(url, timeout=15, proxies=proxy)
            if resp.status_code == 200:
                return resp
        except:
            continue
    raise Exception("Falha em todos os proxies.")

def _get_names_from_guild_url(url):
    """Busca nomes na tabela principal de membros da guilda."""
    try:
        resp = safe_request(url)
        soup = BeautifulSoup(resp.content, "html.parser")
        guild_table = soup.find("table", class_="TableContent")
        nomes = []

        if guild_table:
            rows = guild_table.find_all("tr", recursive=False)[1:]
            for row in rows:
                tds = row.find_all("td")
                if len(tds) > 1:
                    link = tds[1].find("a", href=lambda h: h and "subtopic=characters" in h)
                    if link:
                        nome = link.text.strip()
                        if nome:
                            nomes.append(nome)

        return list(set(nomes))

    except Exception as e:
        print(f"ERRO: Falha ao buscar lista da guild: {e}")
        return []

def _scrape_highscores_page(skill, page, vocation_id=None):
    vocation_param = f"&vocation={vocation_id}" if vocation_id else ""
    url = f"https://miracle74.com/?subtopic=highscores&list={skill}&page={page}{vocation_param}"

    try:
        sleep(1.5)
        resp = safe_request(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')

        tables = soup.find_all('table', class_='TableContent')
        if len(tables) < 2:
            return None

        return tables[1]

    except Exception as e:
        print(f"ERRO PÁGINA {page}: {e}")
        return None

# ===============================================
# SALVAMENTO / FILTRO
# ===============================================

def _filter_and_save(skill_key, guild_names, all_highscores, value_name):
    guild_names_lower = {name.lower() for name in guild_names}
    nomes_em_comum = [e for e in all_highscores if e["nome"].lower() in guild_names_lower]

    def sort_key(entry):
        cleaned = re.sub(r"[^\d]", "", str(entry['order_value']))
        return int(cleaned) if cleaned.isdigit() else 0

    nomes_em_comum.sort(key=sort_key, reverse=True)

    json_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "skill_name": SKILLS[skill_key],
        "value_type": value_name,
        "ranking": [
            {
                "rank_guild": i,
                "nome": e["nome"],
                "valor": e["display_value"]
            }
            for i, e in enumerate(nomes_em_comum, 1)
        ]
    }

    try:
        file_name = f"ranking_{skill_key}.json"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print(f"JSON '{file_name}' salvo.")
    except Exception as e:
        print(f"ERRO ao salvar JSON: {e}")

# ===============================================
# LÓGICA DE RANKING
# ===============================================

def rankear_guild_por_skill(skill_key, guild_names):
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
                name_tag = tds[NAME_INDEX].find("a")
                if name_tag:
                    all_highscores.append({
                        "nome": name_tag.text.strip(),
                        "display_value": tds[VALUE_INDEX].text.strip(),
                        "order_value": tds[ORDER_INDEX].text.strip()
                    })

    _filter_and_save(skill_key, guild_names, all_highscores, VALUE_NAME)

def rankear_mage_skills(guild_names, skill_key):
    mage_data = {}
    weapons = ['sword', 'club', 'axe']
    vocations = [1, 2]

    NAME_INDEX = 2
    VALUE_INDEX = 5

    for weapon in weapons:
        for voc in vocations:
            for page in range(1, MAX_PAGES + 1):
                table = _scrape_highscores_page(weapon, page, vocation_id=voc)
                if table is None:
                    continue

                for tr in table.find_all("tr", bgcolor=True):
                    tds = tr.find_all("td")
                    if len(tds) <= VALUE_INDEX:
                        continue

                    name_tag = tds[NAME_INDEX].find("a")
                    if not name_tag:
                        continue

                    name = name_tag.text.strip()
                    raw = re.sub(r"[^\d]", "", tds[VALUE_INDEX].text)
                    if not raw.isdigit():
                        continue

                    val = int(raw)

                    if name not in mage_data or val > mage_data[name]['order_value']:
                        mage_data[name] = {
                            "name": name,
                            "best_skill_value": val,
                            "best_skill_name": weapon.capitalize(),
                            "order_value": val
                        }

    arr = [
        {
            "nome": d["name"],
            "display_value": f"{d['best_skill_value']} ({d['best_skill_name']})",
            "order_value": d["order_value"]
        }
        for d in mage_data.values()
    ]

    _filter_and_save(skill_key, guild_names, arr, "Skill")

def rankear_mage_defense(guild_names, skill_key):
    arr = []
    NAME_INDEX = 2
    VALUE_INDEX = 5
    vocations = [1, 2]

    for voc in vocations:
        for page in range(1, MAX_PAGES + 1):
            table = _scrape_highscores_page("shielding", page, vocation_id=voc)
            if table is None:
                continue

            for tr in table.find_all("tr", bgcolor=True):
                tds = tr.find_all("td")
                if len(tds) <= VALUE_INDEX:
                    continue

                name_tag = tds[NAME_INDEX].find("a")
                if not name_tag:
                    continue

                raw = re.sub(r"[^\d]", "", tds[VALUE_INDEX].text)
                if not raw.isdigit():
                    continue

                arr.append({
                    "nome": name_tag.text.strip(),
                    "display_value": raw,
                    "order_value": int(raw)
                })

    _filter_and_save(skill_key, guild_names, arr, "Skill")

# ===============================================
# MAIN
# ===============================================

def main():
    print("Iniciando geração de rankings (com proxy automático).")
    guild_names = _get_names_from_guild_url(GUILD_URL)

    if not guild_names:
        print("ERRO: nenhum membro encontrado.")
        sys.exit(1)

    print(f"{len(guild_names)} membros encontrados.")

    for skill_key in SKILLS.keys():
        print("-" * 30)
        if skill_key == 'mage_skill':
            rankear_mage_skills(guild_names, skill_key)
        elif skill_key == 'mage_defense':
            rankear_mage_defense(guild_names, skill_key)
        else:
            rankear_guild_por_skill(skill_key, guild_names)

    print("Rankings finalizados.")

if __name__ == "__main__":
    main()
