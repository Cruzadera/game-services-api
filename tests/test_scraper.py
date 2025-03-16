import re
import pytest
from app.scrapers.gamepass_scraper import (
    advanced_search_game_ultimate,
    advanced_search_game_standard,
    advanced_search_game_core,
)
from app.models import ResponseSearch

# Definimos una clase para simular la respuesta de requests
class FakeResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

# Simula una respuesta donde se encuentra el juego en la primera página
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

# Simula una respuesta donde la tabla no se encuentra
def fake_get_no_table(url):
    html = "<html><body><div>No hay tabla aquí</div></body></html>"
    return FakeResponse(200, html)

# Simula una respuesta con un código HTTP diferente de 200
def fake_get_non_200(url):
    return FakeResponse(404, "")

# Simula una respuesta con la tabla pero sin filas
def fake_get_no_rows(url):
    html = """
    <html>
      <body>
        <table class="maintable">
          <tbody>
          </tbody>
        </table>
      </body>
    </html>
    """
    return FakeResponse(200, html)

# Simula paginación: en la página 1 no hay match pero existe un enlace ">"
# y en la página 2 se encuentra el juego buscado
def fake_get_pagination(url):
    match = re.search(r'page=(\d+)', url)
    page = int(match.group(1)) if match else 1
    if page == 1:
        html = """
        <html>
          <body>
            <table class="maintable">
              <tbody>
                <tr>
                  <td>1</td>
                  <td>Some Other Game</td>
                </tr>
              </tbody>
            </table>
            <a>></a>
          </body>
        </html>
        """
        return FakeResponse(200, html)
    elif page == 2:
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
    else:
        # Si se llega a una página sin más datos
        html = "<html><body>No more pages</body></html>"
        return FakeResponse(200, html)

# Test: Caso match en la primera página
def test_advanced_search_game_ultimate_match(monkeypatch):
    monkeypatch.setattr(
        "app.scrapers.gamepass_scraper.requests.get",
        lambda url: fake_get_match(url)
    )
    result = advanced_search_game_ultimate("plague tale")
    assert isinstance(result, ResponseSearch)
    assert result.in_gamepass is True
    assert "Plague Tale" in result.game

# Test: Caso en el que la tabla no se encuentra
def test_advanced_search_game_no_table(monkeypatch):
    monkeypatch.setattr(
        "app.scrapers.gamepass_scraper.requests.get",
        lambda url: fake_get_no_table(url)
    )
    result = advanced_search_game_ultimate("any game")
    assert isinstance(result, ResponseSearch)
    assert result.in_gamepass is False
    assert result.game == ""

# Test: Caso en el que el código HTTP no es 200
def test_advanced_search_game_non_200(monkeypatch):
    monkeypatch.setattr(
        "app.scrapers.gamepass_scraper.requests.get",
        lambda url: fake_get_non_200(url)
    )
    result = advanced_search_game_ultimate("any game")
    assert isinstance(result, ResponseSearch)
    assert result.in_gamepass is False
    assert result.game == ""

# Test: Caso en el que se encuentra la tabla pero sin filas
def test_advanced_search_game_no_rows(monkeypatch):
    monkeypatch.setattr(
        "app.scrapers.gamepass_scraper.requests.get",
        lambda url: fake_get_no_rows(url)
    )
    result = advanced_search_game_ultimate("any game")
    # En este caso, según el código, se retorna un diccionario
    # Si prefieres que siempre retorne un ResponseSearch, podrías modificar el código.
    assert isinstance(result, dict)
    assert result.get("in_gamepass") is False

# Test: Caso con paginación (el juego se encuentra en la segunda página)
def test_advanced_search_game_pagination(monkeypatch):
    monkeypatch.setattr(
        "app.scrapers.gamepass_scraper.requests.get",
        lambda url: fake_get_pagination(url)
    )
    result = advanced_search_game_ultimate("plague tale")
    assert isinstance(result, ResponseSearch)
    assert result.in_gamepass is True
    assert "Plague Tale" in result.game
