import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.scrapers.nintendoonline_scraper import scrape_nintendo_nso_games

def main():
    print("Iniciando test del scraper de Nintendo NSO...\n")
    results = scrape_nintendo_nso_games()

    if not results:
        print("❌ No se encontró ningún juego.")
        return

    print(f"✅ Se encontraron {len(results)} juegos:\n")
    for game in results[:20]:  # muestra solo los primeros 20 para no saturar la consola
        print(f"- {game.game} [{', '.join(game.tiers)}]")

if __name__ == "__main__":
    main()
