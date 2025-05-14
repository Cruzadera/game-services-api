import requests
from bs4 import BeautifulSoup
from app.models import ResponseGameOnline
from typing import List

def scrape_nintendo_nso_games() -> List[ResponseGameOnline]:
    """
    Extrae los juegos disponibles con suscripción a Nintendo Switch Online y Expansion Pack desde Nintendo Life.
    Retorna una lista de ResponseGamePass con 'NSO' o 'NSO Expansion' como tier correspondiente.
    """
    base_url = "https://www.nintendolife.com/games/browse?subscription=nso%2Cnso-expansion&page={}"
    page_number = 1
    games_dict = {}

    while True:
        url = base_url.format(page_number)
        print(f"Consultando NSO: {url}")
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error al acceder a la página {page_number} (código {response.status_code})")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        game_cards = soup.find_all("div", class_="c-game")

        if not game_cards:
            print(f"No se encontraron más juegos en la página {page_number}.")
            break

        for card in game_cards:
            title_tag = card.find("h2", class_="c-game_title")
            if not title_tag:
                continue

            game_name = title_tag.get_text(strip=True)
            if not game_name:
                continue

            # Determina si el juego pertenece a NSO o NSO Expansion Pack
            meta_info = card.find("p", class_="c-game_subtitle")
            tiers = []

            if meta_info:
                text = meta_info.get_text().lower()
                if "expansion" in text:
                    tiers.append("NSO Expansion")
                else:
                    tiers.append("NSO")

            if game_name not in games_dict:
                games_dict[game_name] = set()

            for tier in tiers:
                games_dict[game_name].add(tier)

        page_number += 1

    results = [
        ResponseGameOnline(game=name, tiers=list(tiers))
        for name, tiers in games_dict.items()
    ]
    return results