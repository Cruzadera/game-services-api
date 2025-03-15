import requests
from bs4 import BeautifulSoup
from app.models import ResponseSearch

def advanced_search_game_ultimate(game_query: str) -> ResponseSearch:
    """
    Recorre las páginas del listado de Game Pass Ultimate en TrueAchievements
    y verifica si el término de búsqueda se encuentra dentro del nombre de algún juego.
    """
    query_lower = game_query.strip().lower()
    base_url = "https://www.trueachievements.com/game-pass-ultimate/games?page={}"

    return search_advanced(base_url, query_lower, game_query);

def advanced_search_game_standard(game_query: str) -> ResponseSearch:
    """
    Recorre las páginas del listado de Game Pass Standard en TrueAchievements
    y verifica si el término de búsqueda se encuentra dentro del nombre de algún juego.
    """
    query_lower = game_query.strip().lower()
    base_url = "https://www.trueachievements.com/game-pass-standard/games?page={}"

    return search_advanced(base_url, query_lower, game_query);


def advanced_search_game_core(game_query: str) -> ResponseSearch:
    """
    Recorre las páginas del listado de Game Pass Core en TrueAchievements
    y verifica si el término de búsqueda se encuentra dentro del nombre de algún juego.
    """
    query_lower = game_query.strip().lower()
    base_url = "https://www.trueachievements.com/game-pass-standard/games?page={}"

    return search_advanced(base_url, query_lower, game_query)

def search_advanced(base_url: str, query_lower: str, game_query:str) -> ResponseSearch:
    page_number = 1
    while True:
        url = base_url.format(page_number)
        print(f"Consultando: {url}")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"No se pudo acceder a la página (código {response.status_code}).")
            return ResponseSearch(game="", in_gamepass=False)

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="maintable")
        if not table:
            print("No se encontró la tabla con la clase 'maintable'. Fin de la búsqueda.")
            return ResponseSearch(game="", in_gamepass=False)

        tbody = table.find("tbody") or table
        rows = tbody.find_all("tr")
        if not rows:
            print("No se encontraron filas en la tabla. Fin de la búsqueda.")
            return {"game": "", "in_gamepass": False}

        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 2:
                continue

            origin_game_name = cells[1].get_text(strip=True)
            game_name = origin_game_name.lower()
            if query_lower in game_name:
                print(f"¡Encontrado '{game_query}' como '{origin_game_name}'!")
                return ResponseSearch(game=origin_game_name, in_gamepass=True)

        # Si no hay siguiente página, salimos
        next_link = soup.find("a", text=">")
        if not next_link:
            return ResponseSearch(game="", in_gamepass=False)

        page_number += 1

# Ejemplo de uso:
if __name__ == "__main__":
    juego_a_buscar = "plague tale"
    if advanced_search_game_ultimate(juego_a_buscar):
        print(f"El término '{juego_a_buscar}' coincide con algún juego en Game Pass Ultimate.")
    else:
        print(f"No se encontró ningún juego que contenga '{juego_a_buscar}'.")