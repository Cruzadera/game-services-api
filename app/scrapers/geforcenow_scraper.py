import requests
from typing import List
from app.models import ResponseGameOnline
from app.utils.logger import log_info

GRAPHQL_URL = "https://api-prod.nvidia.com/services/gfngames/v1/gameList"

def scrape_geforce_now_games() -> List[ResponseGameOnline]:
    log_info("Consultando listado de juegos en GeForce NOW vía POST plano...", icon="☁️")

    graphql_body = (
        '{ apps(country:"US" language:"en_US") { '
        'items { title } } }'
    )

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.205 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "es-ES,es;q=0.9",
        "Origin": "https://www.nvidia.com",
        "Referer": "https://www.nvidia.com/",
    }

    try:
        response = requests.post(GRAPHQL_URL, data=graphql_body, headers=headers, timeout=15)

        if response.status_code != 200:
            log_info(f"❌ Respuesta no exitosa: {response.status_code}", icon="🚫")
            return []

        data = response.json()
        items = data.get("data", {}).get("apps", {}).get("items", [])

        return [
            ResponseGameOnline(title=item["title"], streaming=["GeForce NOW"])
            for item in items if "title" in item
        ]

    except Exception as e:
        log_info(f"🔥 Error durante la petición a la API de GeForce NOW: {e}", icon="🔥")
        return []
