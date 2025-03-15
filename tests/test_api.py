from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Game Services API"}

def test_post_game_search():
    """
    Testea la búsqueda de un juego en el servicio de Game Pass.
    """
    game_name = "Halo"
    response = client.post("/game", json={"game_name": game_name})
    
    assert response.status_code in [200, 404]
    
    if response.status_code == 200:
        data = response.json()
        assert "game" in data
        assert "tiers" in data
        assert isinstance(data["tiers"], list)

def test_invalid_game_request():
    """
    Verifica que el endpoint maneje correctamente una petición inválida.
    """
    response = client.post("/game", json={})
    assert response.status_code == 422  # Unprocessable Entity debido a datos incorrectos
