from app.scrapers.nintendoonline_scraper import scrape_all_nso_games
from app.database import upsert_games

async def fill_games_in_nso():
    games = await scrape_all_nso_games()

    if not isinstance(games, list):
        games = []

    formatted_games = [
        game.dict() if hasattr(game, "dict") else game
        for game in games if game is not None
    ]

    if formatted_games:
        await upsert_games(formatted_games)

    return formatted_games