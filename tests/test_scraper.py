from app.scrapers.gamepass_scrapper import advanced_search_game
from app.models import ResponseGamePass

def test_advanced_search_game():
    """
    Prueba el scraper con un juego que probablemente no esté en la lista.
    Se espera que la función devuelva una respuesta sin tiers.
    """
    resultado = advanced_search_game("un juego que no existe")

    # Se espera que retorne un objeto ResponseGamePass con tiers vacío
    assert isinstance(resultado, ResponseGamePass)
    assert resultado.tiers == []

def test_advanced_search_game_valid():
    """
    Prueba el scraper con un juego conocido en Game Pass.
    Como es un test real, asegúrate de usar un nombre válido.
    """
    resultado = advanced_search_game("terraria")

    # Si el juego está en Game Pass, debería devolver un objeto con tiers no vacío.
    assert isinstance(resultado, ResponseGamePass)
    assert len(resultado.tiers) > 0  # Debe tener al menos un nivel de suscripción
