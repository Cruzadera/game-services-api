from app.models import ResponseGamePass


def format_game_name(game_name: str) -> str:
    """
    Función auxiliar para formatear el nombre de un juego.
    """
    return game_name.strip().lower()


def buildResponseGamePass(resultGPC, resultGPS, resultGPU) -> ResponseGamePass:
    """
    Construye la respuesta de la API combinando los resultados de los distintos niveles de Game Pass.
    
    Retorna un objeto con:
    - **game**: El nombre original del juego encontrado.
    - **in_gamepass**: True si el juego está en alguna de las versiones de Game Pass.
    - **tiers**: Lista de los niveles en los que está disponible (Ultimate, Standard, Core).
    """

    game_name = None
    tiers = []

    # Determinar el nombre del juego (el primero encontrado)
    if resultGPU:
        game_name = resultGPU["game"]
        tiers.append("Ultimate")
    if resultGPS:
        game_name = game_name or resultGPS["game"]
        tiers.append("Standard")
    if resultGPC:
        game_name = game_name or resultGPC["game"]
        tiers.append("Core")

    return ResponseSearch(
        game=game_name,
        in_gamepass=True,
        tiers=tiers
    )

    
