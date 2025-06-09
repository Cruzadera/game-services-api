import cloudscraper
from bs4 import BeautifulSoup
from app.models import ResponseSearch, ResponseGameOnline
from typing import List, Dict
from app.utils.logger import log_info

scraper = cloudscraper.create_scraper()

def advanced_search_game_ultimate(game_query: str) -> ResponseSearch:
    query_lower = game_query.strip().lower()
    base_url = "https://www.trueachievements.com/game-pass-ultimate/games?page={}"
    return search_advanced(base_url, query_lower, game_query, "Ultimate")

def advanced_search_game_standard(game_query: str) -> ResponseSearch:
    query_lower = game_query.strip().lower()
    base_url = "https://www.trueachievements.com/game-pass-standard/games?page={}"
    return search_advanced(base_url, query_lower, game_query, "Standard")

def advanced_search_game_core(game_query: str) -> ResponseSearch:
    query_lower = game_query.strip().lower()
    base_url = "https://www.trueachievements.com/game-pass-core/games?page={}"
    return search_advanced(base_url, query_lower, game_query, "Core")

def search_advanced(base_url: str, query_lower: str, game_query: str, tier: str) -> ResponseSearch:
    page_number = 1
    while True:
        url = base_url.format(page_number)
        log_info(f"Consultando ({tier}): {url}", icon="🔎")

        response = scraper.get(url)
        if response.status_code != 200:
            log_info(f"No se pudo acceder a la página (código {response.status_code}) para el tier {tier}.", icon="❌")
            return ResponseSearch(game="", in_gamepass=False)

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="maintable")
        if not table:
            log_info(f"No se encontró la tabla con la clase 'maintable' en el tier {tier}. Fin de la búsqueda.", icon="❌")
            return ResponseSearch(game="", in_gamepass=False)

        tbody = table.find("tbody") or table
        rows = tbody.find_all("tr")
        if not rows:
            log_info(f"No se encontraron filas en la tabla en el tier {tier}. Fin de la búsqueda.", icon="❌")
            return ResponseSearch(game="", in_gamepass=False)

        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 2:
                continue

            origin_game_name = cells[1].get_text(strip=True)
            game_name = origin_game_name.lower()
            if query_lower in game_name:
                log_info(f"✔️ Juego encontrado ({tier}): {origin_game_name}", icon="🎮")
                return ResponseSearch(game=origin_game_name, in_gamepass=True)

        next_link = soup.find("a", string=">")
        if not next_link:
            return ResponseSearch(game="", in_gamepass=False)

        page_number += 1

async def scrape_all_gamepass_games() -> List[ResponseGameOnline]:
    games_dict: Dict[str, set] = {}
    tier_bases = {
        "Ultimate": "https://www.trueachievements.com/game-pass-ultimate/games?page={}",
        "Standard": "https://www.trueachievements.com/game-pass-standard/games?page={}",
        "Core": "https://www.trueachievements.com/game-pass-core/games?page={}"
    }

    for tier, base_url in tier_bases.items():
        page_number = 1
        while True:
            url = base_url.format(page_number)
            log_info(f"Consultando ({tier}): {url}", icon="🔎")

            response = scraper.get(url)
            if response.status_code != 200:
                log_info(f"No se pudo acceder a la página {page_number} para el tier {tier}.", icon="❌")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_="maintable")
            if not table:
                log_info(f"No se encontró la tabla en el tier {tier} en la página {page_number}.", icon="❌")
                break

            for row in table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) < 2:
                    continue
                game_name = cells[1].get_text(strip=True)
                if game_name:
                    games_dict.setdefault(game_name, set()).add(tier)

            next_link = soup.find("a", string=">")
            if not next_link:
                break

            page_number += 1

    log_info(f"Total juegos encontrados (Game Pass): {len(games_dict)}", icon="🎉")
    return [ResponseGameOnline(title=game, tiers=list(tiers)) for game, tiers in games_dict.items()]