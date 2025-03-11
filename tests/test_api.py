from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hola, mundo! Bienvenido a la API de Game Pass."

def test_get_game_status():
    # Este test es básico; en un caso real deberías usar un juego conocido o mockear la función de scraping.
    response = client.get("/game/ejemplo")
    # El endpoint retornará False si "ejemplo" no está en la lista, o None si hubo error.
    assert response.status_code in [200, 404]
