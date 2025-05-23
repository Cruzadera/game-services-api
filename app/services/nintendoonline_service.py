from app.scrapers.nintendoonline_scraper import scrape_nintendo_nso_games
from app.database import upsert_games
import traceback

async def fill_games_in_nso():
    try:
        print("🔎 Scraping juegos de Nintendo...")
        games = scrape_nintendo_nso_games()
        print(f"✅ {len(games)} juegos obtenidos.")

        if not isinstance(games, list):
            print("⚠️ Resultado inesperado: no es una lista.")
            games = []

        formatted_games = [
            game.dict() if hasattr(game, "dict") else game
            for game in games if game is not None
        ]

        print(f"📦 Insertando {len(formatted_games)} juegos en la base de datos...")

        if formatted_games:
            await upsert_games(formatted_games)

        print("✅ Inserción completada.")
        return formatted_games

    except Exception as e:
        print("🔥 Error inesperado durante fill_games_in_nso:")
        traceback.print_exc()
        return []