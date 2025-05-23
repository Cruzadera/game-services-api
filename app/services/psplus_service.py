from app.scrapers.psplus_scraper import scrape_all_psplus_games  # Asegúrate de que la función esté correctamente importada
from app.database import upsert_games
from app.utils.logger import log_info
import traceback

async def fill_games_in_psplus():
    try:
        log_info("Scraping juegos de PS Plus...", icon="🔎")
        games = await scrape_all_psplus_games()  # Llamamos a la función scrape_all_psplus_games() que implementamos antes
        log_info(f"{len(games)} juegos obtenidos de PS Plus.", icon="✅")

        if not isinstance(games, list):
            log_info("Resultado inesperado: no es una lista.", icon="⚠️")
            games = []

        formatted_games = [
            game.dict() if hasattr(game, "dict") else game
            for game in games if game is not None
        ]

        log_info(f"Insertando {len(formatted_games)} juegos en la base de datos...", icon="📦")

        if formatted_games:
            await upsert_games(formatted_games)

        log_info("Inserción completada.", icon="✅")
        return formatted_games

    except Exception as e:
        log_info("Error inesperado durante fill_games_in_psplus:", icon="🔥")
        traceback.print_exc()
        return []
