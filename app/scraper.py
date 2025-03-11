import requests
from bs4 import BeautifulSoup
from app.models import ResponseSearch

def advanced_search_game(game_query: str) -> ResponseSearch:
    """
    Recorre las páginas del listado de Game Pass Ultimate en TrueAchievements y
    verifica si el término de búsqueda se encuentra dentro del nombre de algún juego.
    La búsqueda es case-insensitive y permite coincidencias parciales.
    
    Retorna True si se encuentra al menos un juego que coincida,
    o False en caso contrario.
    """
    query_lower = game_query.strip().lower()
    page_number = 1
    base_url = "https://www.trueachievements.com/game-pass-ultimate/games?page={}"

    while True:
        url = base_url.format(page_number)
        print(f"Consultando: {url}")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"No se pudo acceder a la página (código {response.status_code}).")
            return False

        soup = BeautifulSoup(response.text, "html.parser")
        # Buscamos la tabla con la clase "maintable"
        table = soup.find("table", class_="maintable")
        if not table:
            print("No se encontró la tabla con la clase 'maintable'.")
            # Imprime parte del HTML para depuración (opcional)
            print(soup.prettify()[:1000])
            return False

        # Algunas tablas usan <tbody>, otras no
        tbody = table.find("tbody") or table
        rows = tbody.find_all("tr")
        if not rows:
            print("No se encontraron filas en la tabla. Fin de la búsqueda.")
            return False

        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 2:
                continue

            # Según el HTML, el nombre del juego se encuentra en la segunda celda (índice 1)
            origin_game_name = cells[1].get_text(strip=True)
            game_name = cells[1].get_text(strip=True).lower()
            # Verifica si el término de búsqueda se encuentra dentro del nombre del juego
            if query_lower in game_name:
                print(f"¡Encontrado '{game_query}' en la página {page_number} como '{game_name}'!")
                return {"game": origin_game_name, "in_gamepass": True}

        # Verifica si existe una siguiente página
        next_link = soup.find("a", text=">")
        if not next_link:
            print("No se encontró enlace para la siguiente página. Fin de la búsqueda.")
            return False

        page_number += 1

# Ejemplo de uso:
if __name__ == "__main__":
    juego_a_buscar = "plague tale"
    if advanced_search_game(juego_a_buscar):
        print(f"El término '{juego_a_buscar}' coincide con algún juego en Game Pass Ultimate.")
    else:
        print(f"No se encontró ningún juego que contenga '{juego_a_buscar}'.")