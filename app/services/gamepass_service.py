from app.models import ResponseGameOnline
from app.scrapers.gamepass_scraper import advanced_search_game_core, advanced_search_game_standard, advanced_search_game_ultimate, scrape_all_gamepass_games
from app.database import upsert_games
from app.utils.logger import log_info

async def fill_games_in_gamepass():
    log_info("Scraping juegos de Game Pass...", icon="🔎")
    games = await scrape_all_gamepass_games()

    if not isinstance(games, list):
        log_info("Resultado inesperado: no es una lista. Se fuerza a lista vacía.", icon="⚠️")
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