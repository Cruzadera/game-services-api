from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from typing import List

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


async def upsert_games(games: List[dict]):
    for doc in games:
        if "title" not in doc:
            continue  # Evita fallos si falta el campo

        existing = await games_collection.find_one({"title": doc["title"]})

        if existing:
            await games_collection.update_one(
                {"title": doc["title"]},
                {"$set": doc}
            )
        else:
            await games_collection.insert_one(doc)
