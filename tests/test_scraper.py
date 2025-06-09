import pytest
import asyncio
import re
from app.scrapers.gamepass_scraper import (
    scrape_all_gamepass_games,
    advanced_search_game_ultimate,
    advanced_search_game_standard,
    advanced_search_game_core
)
from app.models import ResponseGameOnline, ResponseSearch

# FakeResponse para pruebas unitarias
class FakeResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

# Mocks de distintas situaciones para test unitarios

def fake_get_match(url):
    html = """
    <html>
      <body>
        <table class="maintable">
          <tbody>
            <tr>
              <td>1</td>
              <td>Plague Tale: Innocence</td>
            </tr>
          </tbody>
        </table>
      </body>
    </html>
    """
    return FakeResponse(200, html)

def fake_get_no_table(url):
    html = "<html><body><div>No hay tabla aquí</div></body></html>"
    return FakeResponse(200, html)

def fake_get_non_200(url):
    return FakeResponse(404, "")

def fake_get_no_rows(url):
    html = """
    <html>
      <body>
        <table class="maintable">
          <tbody></tbody>
        </table>
      </body>
    </html>
    """
    return FakeResponse(200, html)

def fake_get_pagination(url):
    match = re.search(r'page=(\d+)', url)
    page = int(match.group(1)) if match else 1
    if page == 1:
        html = """
        <html>
          <body>
            <table class="maintable">
              <tbody>
                <tr><td>1</td><td>Some Other Game</td></tr>
              </tbody>
            </table>
            <a>></a>
          </body>
        </html>
        """
        return FakeResponse(200, html)
    else:
        html = """
        <html>
          <body>
            <table class="maintable">
              <tbody>
                <tr><td>1</td><td>Plague Tale: Innocence</td></tr>
              </tbody>
            </table>
          </body>
        </html>
        """
        return FakeResponse(200, html)

@pytest.mark.asyncio
async def test_scrape_all_gamepass_games():
    games = await scrape_all_gamepass_games()
    assert isinstance(games, list)
    assert all(isinstance(game, ResponseGameOnline) for game in games)
    print("\n🧪 Resultados del scraper Game Pass:")
    for g in games[:10]:
        print(f"- {g.title} ({', '.join(g.tiers)})")
    print(f"\n✅ Total juegos encontrados: {len(games)}")

def test_advanced_search_game_ultimate_real():
    result = advanced_search_game_ultimate("plague tale")
    assert isinstance(result, ResponseSearch)
    assert isinstance(result.in_gamepass, bool)
    assert isinstance(result.game, str)

def test_match_first_page(monkeypatch):
    monkeypatch.setattr("app.scrapers.gamepass_scraper.scraper.get", lambda url: fake_get_match(url))
    result = advanced_search_game_ultimate("plague tale")
    assert result.in_gamepass is True
    assert "Plague Tale" in result.game

def test_no_table(monkeypatch):
    monkeypatch.setattr("app.scrapers.gamepass_scraper.scraper.get", lambda url: fake_get_no_table(url))
    result = advanced_search_game_ultimate("any game")
    assert result.in_gamepass is False
    assert result.game == ""

def test_non_200(monkeypatch):
    monkeypatch.setattr("app.scrapers.gamepass_scraper.scraper.get", lambda url: fake_get_non_200(url))
    result = advanced_search_game_ultimate("any game")
    assert result.in_gamepass is False
    assert result.game == ""

def test_no_rows(monkeypatch):
    monkeypatch.setattr("app.scrapers.gamepass_scraper.scraper.get", lambda url: fake_get_no_rows(url))
    result = advanced_search_game_ultimate("any game")
    assert result.in_gamepass is False
    assert result.game == ""

def test_pagination(monkeypatch):
    monkeypatch.setattr("app.scrapers.gamepass_scraper.scraper.get", lambda url: fake_get_pagination(url))
    result = advanced_search_game_ultimate("plague tale")
    assert result.in_gamepass is True
    assert "Plague Tale" in result.game
