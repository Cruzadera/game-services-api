from app.scrapers.gamepass_scrapper import check_game_in_gamepass

def test_check_game_in_gamepass():
    # Este test es solo un ejemplo. La respuesta dependerá de la página real.
    resultado = check_game_in_gamepass("un juego que no existe")
    # Dado que es poco probable que "un juego que no existe" esté en la lista,
    # esperamos False o None en caso de error.
    assert resultado in [False, None]
