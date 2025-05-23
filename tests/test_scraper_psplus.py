import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.scrapers.psplus_scraper import scrape_playstation_plus_extra_games, scrape_playstation_plus_premium_games, scrape_playstation_plus_essential_games

if __name__ == "__main__":
    games = scrape_playstation_plus_extra_games()
    games_premium = scrape_playstation_plus_premium_games()
    games_essential = scrape_playstation_plus_essential_games()

    print("\n🧪 Resultados del scraper PS Plus Essential:")
    for game in games_essential:
        print(f"- {game.game} ({', '.join(game.tiers)})")

    print("\n🧪 Resultados del scraper PS Plus Extra:")
    for game in games[:10]:
        print(f"- {game.game} ({', '.join(game.tiers)})")

    print("\n🧪 Resultados del scraper PS Plus Premium:")
    for game in games_premium[:10]:
        print(f"- {game.game} ({', '.join(game.tiers)})")

    print(f"\n✅ Total juegos encontrados: {len(games)+len(games_premium)+len(games_essential)}")
