import pytest
import asyncio
from app.scrapers.gamepass_scraper import scrape_all_gamepass_games

@pytest.mark.asyncio
async def run_test():
    print("\n🔎 Ejecutando test para Game Pass Scraper...")
    games = await scrape_all_gamepass_games()

    print("\n🧪 Resultados del scraper Game Pass:")
    for g in games[:10]:  # solo los primeros 10 para no saturar la salida
        print(f"- {g.game} ({', '.join(g.tiers)})")

    print(f"\n✅ Total juegos encontrados: {len(games)}")

if __name__ == "__main__":
    asyncio.run(run_test())
