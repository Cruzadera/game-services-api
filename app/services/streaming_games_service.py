from app.scrapers.geforcenow_scraper import scrape_geforce_now_games
from app.database import upsert_streaming
from app.utils.logger import log_info
import traceback

async def fill_games_in_streaming():
    try:
        log_info("Scraping juegos de servicios de streaming (GeForce NOW, etc.)...", icon="☁️")
        games = scrape_geforce_now_games()
        log_info(f"{len(games)} juegos obtenidos de servicios de streaming.", icon="✅")

        if not isinstance(games, list):
            log_info("Resultado inesperado: no es una lista.", icon="⚠️")
            games = []

        formatted_games = [
            game.dict() if hasattr(game, "dict") else game
            for game in games if game is not None
        ]

        log_info(f"Insertando {len(formatted_games)} juegos en la base de datos...", icon="📦")

        if formatted_games:
            await upsert_streaming(formatted_games)

        log_info("Inserción completada.", icon="✅")
        return formatted_games

    except Exception as e:
        log_info("Error inesperado durante fill_games_in_streaming:", icon="🔥")
        traceback.print_exc()
        return []
