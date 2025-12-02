import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from time import sleep
import sys
import os

# ===============================================
# CONFIGURAÇÃO DO SCRAPENINJA (ANTI-403)
# ===============================================

SCRAPENINJA_KEY = "eabee2fee1mshbaf906b9a758863p137b91jsnb6363b736c6e"

def safe_get(url):
    """Usa ScrapeNinja para contornar 403 no GitHub Actions."""
    api_url = "https://scrapeninja.p.rapidapi.com/scrape"

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "scrapeninja.p.rapidapi.com",
        "x-rapidapi-key": SCRAPENINJA_KEY
    }

    payload = {"url": url}

    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        return data.get("body", "")
    except Exception as e:
        print(f"ERRO ScrapeNinja: {e}")
        return None


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
# FUNÇÕES DE SCRAPING
# ===============================================

def _get_names_from_guild_url(url):
    """Busca nomes dos membros da guild."""
    try:
        html = safe_get(url)
        if not html:
            print("ERRO: ScrapeNinja retornou vazio ao buscar guild.")
            return []

        soup = BeautifulSoup(html, "html.parser")
        guild_table = soup.find("table", class_="TableContent")
        nomes = []

        if guild_table:
            rows = guild_table.find_all("tr", recursive=False)[1:]
            for row in rows:
                tds = row.find_all("td")
                if len(tds) > 1:
                    link = tds[1].find("a", href=lambda href: href and "subtopic=characters" in href)
                    if link and link.text.strip():
                        nomes.append(link.text.strip())

        return list(set(nomes))

    except Exception as e:
        print(f"ERRO ao buscar guild: {e}")
        return []


def _scrape_highscores_page(skill, page, vocation_id=None):
    """Retorna a tabela de highscores."""
    vocation_param = f"&vocation={vocation_id}" if vocation_id else ""
    url = f"https://miracle74.com/?subtopic=highscores&list={skill}&page={page}{vocation_param}"

    try:
        sleep(1.2)
        html = safe_get(url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table", class_="TableContent")

        if len(tables) < 2:
            return None

        return tables[1]

    except Exception:
        return None


# ===============================================
# FILTRO + SALVAMENTO
# ===============================================

def _filter_and_save(skill_key, guild_names, all_highscores, value_name):
    guild_lower = {x.lower() for x in guild_names}
    nomes = [x for x in all_highscores if x["nome"].lower() in guild_lower]

    def sort_key(entry):
        v = str(entry['order_value']).replace(",", "").replace(".", "").replace(" ", "")
        try:
            return int(v)
        except:
            return 0

    nomes.sort(key=sort_key, reverse=True)

    json_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "skill_name": SKILLS[skill_key],
        "value_type": value_name,
        "ranking": []
    }

    for i, entry in enumerate(nomes, start=1):
        json_data["ranking"].append({
            "rank_guild": i,
            "nome": entry["nome"],
            "valor": entry["display_value"]
        })

    file_name = f"ranking_{skill_key}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print(f"JSON gerado: {file_name}")


# ===============================================
# RANKING NORMAL
# ===============================================

def rankear_guild_por_skill(skill_key, guild_names):
    all_data = []
    NAME_INDEX = 2

    if skill_key == "experience":
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
            if len(tds) <= ORDER_INDEX:
                continue

            name_tag = tds[NAME_INDEX].find("a")
            if not name_tag:
                continue

            nome = name_tag.text.strip()
            all_data.append({
                "nome": nome,
                "display_value": tds[VALUE_INDEX].text.strip(),
                "order_value": tds[ORDER_INDEX].text.strip()
            })

    _filter_and_save(skill_key, guild_names, all_data, VALUE_NAME)


# ===============================================
# RANKING DE MAGE COMBAT + DEFENSE
# ===============================================

def rankear_mage_skills(guild_names, skill_key):
    mage_data = {}
    weapons = ["sword", "club", "axe"]
    vocations = [1, 2]

    NAME_INDEX = 2
    SKILL_IDX = 5

    for weapon in weapons:
        for voc in vocations:
            for page in range(1, MAX_PAGES + 1):

                table = _scrape_highscores_page(weapon, page, voc)
                if table is None:
                    continue

                for row in table.find_all("tr", bgcolor=True):
                    tds = row.find_all("td")
                    if len(tds) <= SKILL_IDX:
                        continue

                    name_tag = tds[NAME_INDEX].find("a")
                    if not name_tag:
                        continue

                    nome = name_tag.text.strip()
                    val_str = tds[SKILL_IDX].text.strip().replace(",", "").replace(".", "")

                    try:
                        val = int(val_str)
                    except:
                        continue

                    if nome not in mage_data or val > mage_data[nome]["order_value"]:
                        mage_data[nome] = {
                            "nome": nome,
                            "display_value": f"{val} ({weapon.capitalize()})",
                            "order_value": val
                        }

    _filter_and_save(skill_key, guild_names, list(mage_data.values()), "Skill")


def rankear_mage_defense(guild_names, skill_key):
    all_data = []
    vocations = [1, 2]
    NAME_INDEX = 2
    SKILL_IDX = 5

    for voc in vocations:
        for page in range(1, MAX_PAGES + 1):
            table = _scrape_highscores_page("shielding", page, voc)
            if table is None:
                continue

            for row in table.find_all("tr", bgcolor=True):
                tds = row.find_all("td")
                if len(tds) <= SKILL_IDX:
                    continue

                name_tag = tds[NAME_INDEX].find("a")
                if not name_tag:
                    continue

                nome = name_tag.text.strip()
                val_str = tds[SKILL_IDX].text.strip().replace(",", "").replace(".", "")

                try:
                    val = int(val_str)
                except:
                    continue

                all_data.append({
                    "nome": nome,
                    "display_value": str(val),
                    "order_value": val
                })

    _filter_and_save(skill_key, guild_names, all_data, "Skill")


# ===============================================
# MAIN
# ===============================================

def main():
    print("Iniciando geração de rankings.")
    print(f"Buscando guild: {GUILD_URL}")

    guild_names = _get_names_from_guild_url(GUILD_URL)

    if not guild_names:
        print("ERRO: Guild sem membros. Encerrando.")
        sys.exit(1)

    print(f"{len(guild_names)} membros encontrados.")

    for skill_key in SKILLS.keys():
        print("-" * 40)
        print(f"Processando: {SKILLS[skill_key]}")

        if skill_key == "mage_skill":
            rankear_mage_skills(guild_names, skill_key)
        elif skill_key == "mage_defense":
            rankear_mage_defense(guild_names, skill_key)
        else:
            rankear_guild_por_skill(skill_key, guild_names)

    print("Finalizado todos os rankings.")


if __name__ == "__main__":
    main()
