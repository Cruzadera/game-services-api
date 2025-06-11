from typing import List, Optional
from bson import ObjectId
from app.database import games_collection

async def search_game_by_name(name: str):
    return await games_collection.find_one({
        "game": {"$regex": name, "$options": "i"}
    })

async def get_games_paginated(page: int = 1, limit: int = 10) -> List[dict]:
    """Return games paginated using page and limit."""
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10
    skip = (page - 1) * limit
    cursor = games_collection.find({}).skip(skip).limit(limit)
    games: List[dict] = []
    async for game in cursor:
        game["_id"] = str(game["_id"])
        games.append(game)
    return games


async def get_game_by_id(game_id: str) -> Optional[dict]:
    """Return a single game by its MongoDB _id."""
    try:
        obj_id = ObjectId(game_id)
    except Exception:
        return None
    game = await games_collection.find_one({"_id": obj_id})
    if game:
        game["_id"] = str(game["_id"])
    return game
