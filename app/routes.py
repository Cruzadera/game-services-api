from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models import ResponseSearch
from app.scrapers.gamepass_scraper import advanced_search_game_core, advanced_search_game_standard, advanced_search_game_ultimate

router = APIRouter()

class GameQuery(BaseModel):
    game_name: str


@router.get("/", tags=["General"])
def read_root():
    """
    Endpoint raíz que da la bienvenida a la API.
    """
    return JSONResponse(content={"message": "Hola, mundo! Bienvenido a la API de Game Services."})


@router.post("/game", response_model=ResponseSearch, tags=["Game"])
def search_game(query: GameQuery):
    """
    Realiza una búsqueda avanzada en el listado de Game Pass
    
    Recibe un JSON con:
    - **game_name**: Término a buscar (la búsqueda no distingue mayúsculas/minúsculas y permite coincidencias parciales).
    
    Retorna un objeto con:
    - **game**: El nombre original del juego encontrado.
    - **in_gamepass**: Valor True, indicando que el juego se encontró en el catálogo.
    """
    resultGPU = advanced_search_game_ultimate(query.game_name)
    resultGPS = advanced_search_game_standard(query.game_name)
    resultGPC = advanced_search_game_core(query.game_name)
    
    if not resultGPU and not resultGPS and not resultGPC:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró ningún juego que contenga '{query.game_name}'."
        )
    else:
        buildResponseGamePass(resultGPC, resultGPS, resultGPU)
    return resultGPU
