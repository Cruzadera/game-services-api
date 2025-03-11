from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Game Pass API",
    description="API para consultar si un juego está incluido en Xbox Game Pass",
    version="1.0.0"
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
