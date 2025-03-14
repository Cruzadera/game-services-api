from app.scrapers.gamepass_scrapper import advanced_search_game

def test_advanced_search_game():
    """
    Prueba el scraper con un juego que probablemente no esté en la lista.
    Se espera que la función devuelva False si el juego no existe.
    """
    resultado = advanced_search_game("un juego que no existe")
    
    # Se espera que retorne False ya que el juego no está en el Game Pass
    assert resultado.in_gamepass == False

def test_advanced_search_game_valid():
    """
    Prueba el scraper con un juego conocido en Game Pass.
    Como es un test real, asegúrate de usar un nombre válido.
    """
    resultado = advanced_search_game("Halo")
    
    # Si el juego está en Game Pass, debería devolver un diccionario con el nombre original y True.
    assert isinstance(resultado, dict)
    assert "game" in resultado
    assert resultado.in_gamepass is True