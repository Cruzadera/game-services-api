from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models import ResponseSearch, ResponseGamePass
from app.scrapers.gamepass_scraper import advanced_search_game_core, advanced_search_game_standard, advanced_search_game_ultimate, scrape_all_gamepass_games
from app.utils.helpers import buildResponseGamePass
from app.database import upsert_games
from typing import List
from app.services.gamepass_service import fill_games_in_gamepass

router = APIRouter()


class GameQuery(BaseModel):
    game_name: str


@router.get("/", tags=["General"])
def read_root():
    """
    Endpoint raíz que da la bienvenida a la API.
    """
    return JSONResponse(content={"message": "Welcome to the Game Services API"})


@router.post("/game-pass", response_model=ResponseGamePass, tags=["GamePass"])
def search_game(query: GameQuery):
    """
    Realiza una búsqueda avanzada en el listado de Game Pass.

    Recibe un JSON con:
    - **game_name**: Término a buscar (la búsqueda no distingue mayúsculas/minúsculas y permite coincidencias parciales).

    Retorna un objeto con:
    - **game**: El nombre original del juego encontrado.
    - **in_gamepass**: Valor True, indicando que el juego se encontró en el catálogo.
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

    return buildResponseGamePass(resultGPC, resultGPS, resultGPU)


@router.post("/fill-gamepass", response_model=List[ResponseGamePass], tags=["GamePass"])
async def search_gamepass():
    """
    Actualiza o crea nuevos juegos con los tiers correspondiente que tiene disponible en el GamePass
    """
    try:
        result = await fill_games_in_gamepass()
        return {"message": "Game Pass database updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500)
