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
    if not games_data:
        return

    for game in games_data:
        doc = game.dict() if hasattr(game, "dict") else game
        existing = await games_collection.find_one({"game": doc["game"]})
        if existing:
            doc["tiers"] = list(set(existing.get("tiers", []))
                                | set(doc.get("tiers", [])))
        await games_collection.update_one(
            {"game": doc["game"]},
            {"$set": doc},
            upsert=True
        )
