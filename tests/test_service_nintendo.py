import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from app.services.nintendoonline_service import fill_games_in_nso

if __name__ == "__main__":
    asyncio.run(fill_games_in_nso())