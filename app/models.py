from pydantic import BaseModel
from typing import List, Optional

class GameStatus(BaseModel):
    game: str
    in_gamepass: bool


class ResponseSearch(BaseModel):
    game: Optional[str] = None
    in_gamepass: bool

class ResponseGameOnline(BaseModel):
    title: str
    tiers: List[str] = []
    streaming: List[str] = []