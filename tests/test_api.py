from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Hola, mundo! Bienvenido a la API de Game Services."

def test_post_game_search():
    """
    Testea la búsqueda de un juego en el servicio de Game Pass.
    """
    game_name = "Halo"
    response = client.post("/game", json={"game_name": game_name})

    assert response.status_code in [200, 404]  # Puede devolver éxito o que no lo encontró.
    
    json_response = response.json()
    
    if response.status_code == 200:
        assert "game" in json_response
        assert "in_gamepass" in json_response
        assert isinstance(json_response["game"], str)
        assert isinstance(json_response["in_gamepass"], bool)
    
    if response.status_code == 404:
        assert "detail" in json_response
        assert f"No se encontró ningún juego que contenga '{game_name}'" in json_response["detail"]

def test_invalid_game_request():
    """
    Verifica que el endpoint maneje correctamente una petición inválida.
    """
    response = client.post("/game", json={})
    assert response.status_code == 422 
