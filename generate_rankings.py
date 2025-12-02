import os
import json
import time
import requests
from bs4 import BeautifulSoup

# --------------------------------------------
# CONFIGURAÇÕES
# --------------------------------------------

GUILD_URL = "https://miracle74.com/?subtopic=guilds&action=show&guild=600"
OUTPUT_FILE = "rankings.json"

SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY")  # <-- PEGANDO DO SECRET

if not SCRAPERAPI_KEY:
    print("ERRO: SCRAPERAPI_KEY não encontrado no ambiente!")
    print("Você precisa cadastrar o secret no GitHub.")
    exit(1)


# --------------------------------------------
# FUNÇÃO DE REQUISIÇÃO COM RETRY
# --------------------------------------------

def fetch_with_scraperapi(url):
    api_url = f"http://api.scraperapi.com/?api_key={SCRAPERAPI_KEY}&url={url}"

    for attempt in range(1, 4):
        try:
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()
            return response.text

        except Exception as e:
            print(f"Tentativa {attempt}/3 falhou: {e}")
            time.sleep(3)

    print("Falhou todas as tentativas ScraperAPI.")
    return None


# --------------------------------------------
# PARSE DO SITE
# --------------------------------------------

def parse_guild_members(html):
    soup = BeautifulSoup(html, "html.parser")

    members_table = soup.find("table", {"class": "TableContent"})

    if not members_table:
        return []

    rows = members_table.find_all("tr")[1:]  # ignora cabeçalho

    members = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        name = cols[0].text.strip()
        lvl = int(cols[1].text.strip())

        members.append({"name": name, "level": lvl})

    return members


# --------------------------------------------
# GERA RANKINGS
# --------------------------------------------

def create_rankings(members):
    # Ordena por level DESC, e nome ASC em caso de empate
    members_sorted = sorted(members, key=lambda x: (-x["level"], x["name"]))

    rankings = {
        "top10": members_sorted[:10],
        "full": members_sorted
    }

    return rankings


# --------------------------------------------
# EXECUÇÃO PRINCIPAL
# --------------------------------------------

def main():
    print("Iniciando geração de rankings.")
    print(f"Buscando guild: {GUILD_URL}")

    html = fetch_with_scraperapi(GUILD_URL)

    if not html:
        print("ERRO: ScraperAPI retornou vazio ao buscar guild.")
        print("ERRO: Guild sem membros. Encerrando.")
        exit(1)

    members = parse_guild_members(html)

    if not members:
        print("ERRO: Nenhum membro encontrado.")
        exit(1)

    rankings = create_rankings(members)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(rankings, f, ensure_ascii=False, indent=2)

    print("Rankings gerados com sucesso!")


if __name__ == "__main__":
    main()
