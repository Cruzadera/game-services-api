from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from typing import List
from pymongo import UpdateOne

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
    operations = []

    for doc in games:
        if "title" not in doc:
            continue

        operations.append(
            UpdateOne(
                {"title": doc["title"]},
                {"$set": doc},
                upsert=True
            )
        )

    if operations:
        result = await games_collection.bulk_write(operations)
        print(f"📦 Upserts: {result.upserted_count}, Modificados: {result.modified_count}")

async def upsert_streaming(games: List[dict]):
    operations = []

    for doc in games:
        if "title" not in doc or "streaming" not in doc:
            continue

        operations.append(
            UpdateOne(
                {"title": doc["title"]},
                {"$set": {"streaming": doc["streaming"]}},
                upsert=True
            )
        )

    if operations:
        result = await games_collection.bulk_write(operations)
        print(f"☁️ Upserts streaming: {result.upserted_count}, Modificados: {result.modified_count}")
