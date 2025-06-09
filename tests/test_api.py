import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)


def test_read_root():
    """
    Verifica que el endpoint raíz ("/") responda con un código 200 y el mensaje esperado.
    """
    response = client.get("/")
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
    assert response.json() == {"message": "Welcome to the Game Services API"}, \
        f"Expected message to be 'Welcome to the Game Services API', but got {response.json()}"


@pytest.mark.asyncio
async def test_post_game_search(monkeypatch):
    fake_result = {"title": "Halo", "tiers": ["Ultimate"]}

    monkeypatch.setattr(
        game_search_service.games_collection,
        "find_one",
        AsyncMock(return_value=fake_result)
    )

    response = client.get("/search?game=Halo")
    assert response.status_code == 200
    assert "Halo" in response.text
