import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)


def test_read_root():
    """
    Verifica que el endpoint raíz ("/") responda con un código 200 y el mensaje esperado.
    """
    response = client.get("/")
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
    assert response.json() == {"message": "Welcome to the Game Services API"}, \
        f"Expected message to be 'Welcome to the Game Services API', but got {response.json()}"


@patch("app.routes.search_game_by_name", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_post_game_search(mock_search_game_by_name):
    mock_search_game_by_name.return_value = {
        "title": "Halo",
        "tiers": ["GamePass Ultimate"]
    }

    response = client.get("/search?game=Halo")
    assert response.status_code == 200
    assert "Halo" in response.text


@patch("app.routes.get_games_paginated", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_games_paginated(mock_get_games):
    mock_get_games.return_value = [
        {"_id": "1", "title": "Game 1"},
        {"_id": "2", "title": "Game 2"},
    ]

    response = client.get("/games?page=1&limit=2")
    assert response.status_code == 200
    assert response.json() == [
        {"_id": "1", "title": "Game 1"},
        {"_id": "2", "title": "Game 2"},
    ]


@patch("app.routes.get_game_by_id", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_game_by_id(mock_get_game):
    mock_get_game.return_value = {"_id": "1", "title": "Game 1"}

    response = client.get("/games/1")
    assert response.status_code == 200
    assert response.json() == {"_id": "1", "title": "Game 1"}

