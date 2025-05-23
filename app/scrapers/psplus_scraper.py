import requests
from bs4 import BeautifulSoup

def scrape_psplus_games(url="https://www.playstation.com/es-mx/ps-plus/games/"):
    """
    Scrapes the official PlayStation PS Plus games page and returns a list of game names.

    Note:
    - La estructura de la página puede cambiar. Revisa el HTML actual para ajustar los selectores.
    - Es posible que parte del contenido se cargue mediante JavaScript; en ese caso,
      podrías necesitar utilizar una herramienta que soporte renderizado (por ejemplo, Selenium o Playwright).

    Args:
        url (str): URL de la página de juegos de PS Plus.

    Returns:
        list: Lista con los nombres de los juegos disponibles en PS Plus.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; PSPlusScraper/1.0; +https://yourdomain.com)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve page. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Ejemplo: se asume que cada juego está contenido en un <div> con la clase "game-list-item"
    # y que el título se encuentra en un <h3> dentro de ese div.
    game_elements = soup.find_all("div", class_="game-list-item")
    games = []

    for element in game_elements:
        title_tag = element.find("h3")
        if title_tag:
            game_name = title_tag.get_text(strip=True)
            games.append(game_name)

    return games

if __name__ == "__main__":
    try:
        games = scrape_psplus_games()
        print("PS Plus Games:")
        for game in games:
            print(game)
    except Exception as e:
        print("Error:", e)
