from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models import ResponseGameOnline
from app.scrapers.gamepass_scraper import advanced_search_game_core, advanced_search_game_standard, advanced_search_game_ultimate
from app.utils.helpers import buildResponseGameOnline
from app.services.gamepass_service import fill_games_in_gamepass
from app.services.nintendoonline_service import fill_games_in_nso
from app.services.psplus_service import fill_games_in_psplus
from app.services.streaming_games_service import fill_games_in_streaming
from app.services.games_service import get_games_paginated, get_game_by_id, search_game_by_name

router = APIRouter()


class GameQuery(BaseModel):
    game_name: str


@router.get("/", tags=["General"])
def read_root():
    """
    Endpoint raíz que da la bienvenida a la API.
    """
    return JSONResponse(content={"message": "Welcome to the Game Services API"})


@router.post("/game-pass", response_model=ResponseGameOnline, tags=["GamePass"])
def search_game(query: GameQuery):
    """
    Realiza una búsqueda avanzada en el listado de Game Pass.

    Recibe un JSON con:
    - **game_name**: Término a buscar (la búsqueda no distingue mayúsculas/minúsculas y permite coincidencias parciales).

    Devuelve un objeto ``ResponseGameOnline`` con:
    - **title**: Nombre del juego encontrado.
    - **tiers**: Lista de niveles en los que está disponible el juego.
    """
    resultGPU = advanced_search_game_ultimate(query.game_name)
    resultGPS = advanced_search_game_standard(query.game_name)
    resultGPC = advanced_search_game_core(query.game_name)

    if resultGPU.in_gamepass == False and resultGPS.in_gamepass == False and resultGPC.in_gamepass == False:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró ningún juego que contenga '{query.game_name}'."
        )

    return buildResponseGameOnline(resultGPC, resultGPS, resultGPU)


@router.post("/fill-online-services", tags=["Online Services"])
async def update_online_services():
    try:
        print(">>> Llamando a Game Pass")
        await fill_games_in_gamepass()

        print(">>> Llamando a Nintendo Switch Online")
        await fill_games_in_nso()

        print(">>> Llamando a PS Plus")
        await fill_games_in_psplus()

        print(">>> Llamando a GeForce NOW / Streaming")
        await fill_games_in_streaming()

        return JSONResponse(status_code=200, content={"message": "Todo OK"})
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/search", tags=["Games"])
async def search_game(game: str):
    result = await search_game_by_name(game)
    if not result:
        raise HTTPException(status_code=404, detail=f"No se encontró '{game}' en la base de datos.")

    return ResponseGameOnline(title=result["title"], tiers=result["tiers"])


@router.get("/games", tags=["Games"])
async def list_games(page: int = 1, limit: int = 10):
    return await get_games_paginated(page, limit)


@router.get("/games/{game_id}", tags=["Games"])
async def get_game(game_id: str):
    game = await get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game
