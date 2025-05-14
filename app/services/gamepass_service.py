from app.models import ResponseGameOnline
from app.scrapers.gamepass_scraper import advanced_search_game_core, advanced_search_game_standard, advanced_search_game_ultimate, scrape_all_gamepass_games
from app.database import upsert_games


async def fill_games_in_gamepass():
    games = await scrape_all_gamepass_games()

    if not isinstance(games, list):  # 🔴 Si `games` no es una lista, forzamos a lista vacía
        games = []

    formatted_games = [
        game.dict() if hasattr(game, "dict") else game
        for game in games if game is not None
    ]

    if formatted_games:
        await upsert_games(formatted_games)

    return formatted_games  # ✅ Devuelve siempre una lista

