import json
import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime

# -------------------------------------------------
# CONFIGURAÇÃO
# -------------------------------------------------
SCRAPERAPI_KEY = "S6b64b53de23174761e9ab2bd5c8d80c7"
GUILD_URL = "https://miracle74.com/?subtopic=guilds&action=show&guild=600"
BASE_URL = "https://miracle74.com/?subtopic=highscores"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# -------------------------------------------------
# FUNÇÃO SAFE_GET COM SCRAPERAPI
# -------------------------------------------------
def safe_get(url):
    """Faz GET usando ScraperAPI para evitar erros 403/429."""
    api_url = f"http://api.scraperapi.com/?api_key={SCRAPERAPI_KEY}&url={url}"

    for attempt in range(1, 4):
        try:
            resp = requests.get(api_url, timeout=60)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            print(f"Tentativa {attempt}/3 falhou: {e}")
            sleep(2 * attempt)

    print("Falhou todas as tentativas ScraperAPI.")
    return None

# -------------------------------------------------
# BUSCAR LISTA DE MEMBROS DA GUILD
# -------------------------------------------------
def _get_names_from_guild_url(url):
    html = safe_get(url)
    if not html:
        print("ERRO: ScraperAPI retornou vazio ao buscar guild.")
        return []

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "table table-striped"})
    if not table:
        print("ERRO: Nenhuma tabela encontrada. HTML mudou?")
        return []

    members = []
    rows = table.find_all("tr")[1:]  # pula cabeçalho

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            name = cols[1].text.strip()
            members.append(name)

    return members

# -------------------------------------------------
# BUSCAR HIGHSCORE PARA UM TIPO
# -------------------------------------------------
def _scrape_highscores_page(skill_id):
    """Retorna lista de tuplas (nome, valor)."""
    url = f"{BASE_URL}&list={skill_id}"

    html = safe_get(url)
    if not html:
        print(f"ERRO na página highscores list={skill_id}")
        return None

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table", {"class": "table table-striped"})
    if not table:
        print(f"ERRO: Nenhuma tabela encontrada para list={skill_id}")
        return None

    rows = table.find_all("tr")[1:]

    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            name = cols[1].text.strip()
            value_raw = cols[2].text.strip().replace(",", "")
            try:
                value = int(value_raw)
            except:
                value = 0
            data.append((name, value))

    return data

# -------------------------------------------------
# GERA RANKING PARA UMA SKILL
# -------------------------------------------------
def generate_ranking(skill_name, skill_id, all_members):
    print(f"----------------------------------------")
    print(f"Processando: {skill_name}")

    scraped = _scrape_highscores_page(skill_id)
    if scraped is None:
        print(f"ERRO ao obter highscores de {skill_name}")
        return

    filtered = [(name, value) for name, value in scraped if name in all_members]

    # ORDEM CORRETA:
    #  1) maior valor primeiro
    #  2) empate → ordem alfabética crescente
    filtered.sort(key=lambda x: (-x[1], x[0].lower()))

    output = [{"rank": i + 1, "name": n, "value": v} for i, (n, v) in enumerate(filtered)]

    filename = f"ranking_{skill_name.lower().replace(' ', '_')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"JSON gerado: {filename}")

# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    print("Iniciando geração de rankings.")
    print(f"Buscando guild: {GUILD_URL}")

    members = _get_names_from_guild_url(GUILD_URL)

    if not members:
        print("ERRO: Guild sem membros. Encerrando.")
        return

    print(f"{len(members)} membros encontrados.")

    tasks = [
        ("experience", 0),
        ("sword", 1),
        ("axe", 2),
        ("club", 3),
        ("dist", 4),
        ("maglevel", 5),
        ("shielding", 6),
        ("fishing", 7),
        ("mage_skill", 8),
        ("mage_defense", 9)
    ]

    for skill_name, skill_id in tasks:
        generate_ranking(skill_name, skill_id, members)

    print("Finalizado todos os rankings.")

# -------------------------------------------------
if __name__ == "__main__":
    main()
