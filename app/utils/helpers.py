from app.models import ResponseSearch


def format_game_name(game_name: str) -> str:
    """
    Función auxiliar para formatear el nombre de un juego.
    """
    return game_name.strip().lower()


def buildResponseGamePass(resultGPC: ResponseSearch, resultGPS: ResponseSearch, resultGPU: ResponseSearch):
