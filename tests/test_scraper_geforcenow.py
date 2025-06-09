from app.scrapers.geforcenow_scraper import scrape_geforce_now_games
from app.models import ResponseGameOnline

def test_scrape_geforce_now_games_returns_list():
    results = scrape_geforce_now_games()

    assert isinstance(results, list)
    assert all(isinstance(game, ResponseGameOnline) for game in results)
    assert len(results) > 0, "No se encontraron juegos en GeForce NOW"

    for game in results:
        assert isinstance(game.title, str)
        assert game.title.strip() != ""
        assert isinstance(game.streaming, list)
        assert "GeForce NOW" in game.streaming

    # Imprimir los primeros 10 juegos (solo para verlos durante el test)
    print("\n📋 Primeros 10 juegos encontrados:")
    for game in results[:10]:
        print(f"- {game.title}")

