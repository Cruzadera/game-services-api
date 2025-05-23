from app.database import games_collection

async def search_game_by_name(name: str):
    return await games_collection.find_one({
        "game": {"$regex": name, "$options": "i"}
    })