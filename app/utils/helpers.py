from app.models import ResponseGameOnline, ResponseSearch


def format_game_name(game_name: str) -> str:
    """
    Función auxiliar para formatear el nombre de un juego.
    """
    return game_name.strip().lower()


def buildResponseGameOnline(resultGPC: ResponseSearch, resultGPS: ResponseSearch, resultGPU: ResponseSearch) -> ResponseGameOnline:
    """
    Construye la respuesta de la API combinando los resultados de los distintos niveles de Game Pass.
    
    Retorna un objeto con:
    - **game**: El nombre original del juego encontrado.
    - **in_gamepass**: True si el juego está en alguna de las versiones de Game Pass.
    - **tiers**: Lista de los niveles en los que está disponible (Ultimate, Standard, Core).
    """

    tiers = []

    if resultGPU and resultGPU.in_gamepass:
        tiers.append("Ultimate")
    if resultGPS and resultGPS.in_gamepass:
        tiers.append("Standard")
    if resultGPC and resultGPC.in_gamepass:
        tiers.append("Core")

    return ResponseGameOnline(
        game=resultGPU.game if resultGPU and resultGPU.in_gamepass 
        else resultGPS.game if resultGPS and resultGPS.in_gamepass 
        else resultGPC.game if resultGPC and resultGPC.in_gamepass 
        else "Unknown",
        tiers=tiers
    )

    
