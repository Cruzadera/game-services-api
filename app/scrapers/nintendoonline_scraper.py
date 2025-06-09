import time
import cloudscraper
from bs4 import BeautifulSoup
from app.models import ResponseGameOnline
from typing import List
from app.utils.logger import log_info

scraper = cloudscraper.create_scraper()

def scrape_nintendo_nso_games() -> List[ResponseGameOnline]:
    base_url = "https://www.nintendolife.com/games/browse?subscription=nso%2Cnso-expansion&page={}"
    page_number = 1
    games_dict = {}

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.nintendolife.com/",
        "Connection": "keep-alive",
    }

    while True:
        url = base_url.format(page_number)
        log_info(f"Consultando NSO: {url}", icon="🔎")
        response = scraper.get(url, headers=headers)

        if response.status_code != 200:
            log_info(f"Página {page_number} no accesible (código {response.status_code}). Finalizando scrape.", icon="❌")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        game_cards = soup.select("ul.items > li.item.item-content.item-game")

        if not game_cards:
            log_info(f"No se encontraron más juegos en la página {page_number}. Fin del scrape.", icon="✅")
            break

        for card in game_cards:
            title_tag = card.select_one("a.title")
            subtitle_tag = card.select_one("span.subtitle")

            if not title_tag:
                continue

            subtitle_span = title_tag.find("span", class_="subtitle")
            if subtitle_span:
                subtitle_span.decompose()

            game_name = title_tag.get_text(strip=True)
            if not game_name:
                continue

            tiers = []
            if subtitle_tag:
                subtitle_text = subtitle_tag.get_text(strip=True).lower()
                if "expansion" in subtitle_text:
                    tiers.append("NSO Expansion")
                else:
                    tiers.append("NSO")

            if game_name not in games_dict:
                games_dict[game_name] = set()

            for tier in tiers:
                games_dict[game_name].add(tier)

        page_number += 1
        time.sleep(1)

    if not games_dict:
        log_info("No se recogieron juegos. ¿La web ha cambiado su estructura?", icon="⚠️")
        return []

    results = [
        ResponseGameOnline(title=name, tiers=list(tiers))
        for name, tiers in games_dict.items()
    ]
    log_info(f"Total juegos encontrados: {len(results)}", icon="🎉")
    return results