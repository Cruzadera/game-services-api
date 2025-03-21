from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

client = AsyncIOMotorClient(MONGO_DETAILS)

db = client['ludic']

games_collection = db['games']

print("Connected to Database...")

async def fetch_all_games():
    games = []
    # Ahora games_collection es un objeto de colección y podemos usar find()
    cursor = games_collection.find({})
    async for game in cursor:
        games.append(game)
    return games

async def upsert_games(games_data: list):
    """
    Inserta o actualiza los datos de juegos en MongoDB.
    """
    await games_collection.delete_many({})  # Limpia la colección antes de insertar nuevos datos

    if games_data:
        # Convertir cada objeto a diccionario si aún no lo es
        formatted_games = [
            game.dict() if hasattr(game, "dict") else game for game in games_data
        ]
        await games_collection.insert_many(formatted_games)