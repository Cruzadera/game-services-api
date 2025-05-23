from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(
    title="Game Services API",
    description="API para consultar la disponibilidad de juegos en plataformas de suscripción como Xbox Game Pass, PlayStation Plus (Essential, Extra, Premium) y Nintendo Online. Permite buscar si un juego está incluido en estos servicios de juegos en línea.",
    version="0.0.3"
)

# Habilita CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=9000, reload=True)
