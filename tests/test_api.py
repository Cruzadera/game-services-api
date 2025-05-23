import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

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
async def test_post_game_search():
    """
    Testea la búsqueda de un juego en el servicio de Game Pass.
    """
    game_name = "Halo"
    response = client.get(f"/search?game={game_name}")

    assert response.status_code in [200, 404], \
        f"Expected status code 200 or 404, but got {response.status_code}"

    if response.status_code == 200:
        data = response.json()
        assert "game" in data, "'game' key not found in response"
        assert "tiers" in data, "'tiers' key not found in response"
        assert isinstance(data["tiers"], list), "'tiers' is not a list"
    elif response.status_code == 404:
        assert response.json() == {"detail": "Game not found"}, \
            f"Expected 'Game not found' message, but got {response.json()}"
