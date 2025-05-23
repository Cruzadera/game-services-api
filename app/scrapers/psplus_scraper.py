import requests
from bs4 import BeautifulSoup
from app.models import ResponseGameOnline
from typing import List
from app.utils.logger import log_info

BASE_URL = "https://www.pushsquare.com/guides/all-ps-plus-games"
BLOG_URL = "https://blog.playstation.com/"


def scrape_playstation_plus_extra_games() -> List[ResponseGameOnline]:
    log_info("Consultando listado de PS Plus Extra desde Push Square...", icon="🔎")
    response = requests.get(BASE_URL)

    if response.status_code != 200:
        log_info(
            f"No se pudo acceder a la página (código {response.status_code})", icon="❌")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    header = soup.find("h3", id="all-ps-plus-extra-games-list")
    if not header:
        log_info("No se encontró el encabezado de PS Plus Extra.", icon="⚠️")
        return []

    ul = header.find_next("ul", class_="games-style-list")
    if not ul:
        log_info("No se encontró la lista de juegos para PS Plus Extra.", icon="⚠️")
        return []

    games_dict = {}
    for li in ul.find_all("li"):
        full_text = li.get_text(strip=True)
        if " – " in full_text:
            name, platform_text = full_text.split(" – ", 1)
            tiers = ["PS Plus Extra"]
            games_dict[name] = set(tiers)
        else:
            a_tag = li.find("a")
            if a_tag:
                name = a_tag.get_text(strip=True)
                tiers = ["PS Plus Extra"]
                games_dict[name] = set(tiers)

    results = [ResponseGameOnline(game=game, tiers=list(tiers))
               for game, tiers in games_dict.items()]
    log_info(f"Total juegos encontrados en Extra: {len(results)}", icon="🎮")
    return results


def scrape_playstation_plus_premium_games() -> List[ResponseGameOnline]:
    log_info(
        "Consultando listado de PS Plus Premium desde Push Square...", icon="🔎")
    response = requests.get(BASE_URL)

    if response.status_code != 200:
        log_info(
            f"No se pudo acceder a la página (código {response.status_code})", icon="❌")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    header = soup.find("h3", id="all-ps-plus-premium-games-list")
    if not header:
        log_info("No se encontró el encabezado de PS Plus Premium.", icon="⚠️")
        return []

    ul = header.find_next("ul", class_="games-style-list")
    if not ul:
        log_info(
            "No se encontró la lista de juegos para PS Plus Premium.", icon="⚠️")
        return []

    games_dict = {}
    for li in ul.find_all("li"):
        full_text = li.get_text(strip=True)
        if " – " in full_text:
            name, platform_text = full_text.split(" – ", 1)
            tiers = ["PS Plus Premium"]
            games_dict[name] = set(tiers)
        else:
            a_tag = li.find("a")
            if a_tag:
                name = a_tag.get_text(strip=True)
                tiers = ["PS Plus Premium"]
                games_dict[name] = set(tiers)

    results = [ResponseGameOnline(game=game, tiers=list(
        tiers)) for game, tiers in games_dict.items()]
    log_info(
        f"Total juegos encontrados en Premium: {len(results)}", icon="👑")
    return results


def scrape_playstation_plus_essential_games() -> List[ResponseGameOnline]:
    log_info("Consultando juegos de PS Plus Essential desde Push Square...", icon="🔎")
    response = requests.get(BASE_URL)

    if response.status_code != 200:
        log_info(f"No se pudo acceder a la página (código {response.status_code})", icon="❌")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    header = soup.find("h3", id="all-ps-plus-essential-games-available-now")
    if not header:
        log_info("No se encontró el encabezado de PS Plus Essential.", icon="⚠️")
        return []

    ul = header.find_next("ul", class_="games-style-list")
    if not ul:
        log_info("No se encontró la lista de juegos para PS Plus Essential.", icon="⚠️")
        return []

    games_dict = {}
    for li in ul.find_all("li"):
        a_tag = li.find("a")
        if not a_tag:
            continue
        name = a_tag.get_text(strip=True)
        if not name:
            continue
        games_dict[name] = set(["PS Plus Essential"])

    results = [ResponseGameOnline(game=game, tiers=list(tiers)) for game, tiers in games_dict.items()]
    log_info(f"Total juegos encontrados en Essential: {len(results)}", icon="📅")
    return results


async def scrape_all_psplus_games() -> List[ResponseGameOnline]:
    games_dict = {}

    # Scraping juegos de PS Plus Essential
    log_info("Iniciando scraping para PS Plus Essential...", icon="🔎")
    essential_games = scrape_playstation_plus_essential_games()
    for game in essential_games:
        games_dict.setdefault(game.game, set()).add("PS Plus Essential")

    # Scraping juegos de PS Plus Extra
    log_info("Iniciando scraping para PS Plus Extra...", icon="🔎")
    extra_games = scrape_playstation_plus_extra_games()
    for game in extra_games:
        games_dict.setdefault(game.game, set()).add("PS Plus Extra")

    # Scraping juegos de PS Plus Premium
    log_info("Iniciando scraping para PS Plus Premium...", icon="🔎")
    premium_games = scrape_playstation_plus_premium_games()
    for game in premium_games:
        games_dict.setdefault(game.game, set()).add("PS Plus Premium")

    log_info(f"Total juegos encontrados en PS Plus: {len(games_dict)}", icon="🎉")

    return [ResponseGameOnline(game=game, tiers=list(tiers)) for game, tiers in games_dict.items()]