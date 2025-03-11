# Game Pass API

Esta API permite consultar si un juego está incluido en Xbox Game Pass mediante scraping de la página de TrueAchievements.

## Requisitos

- Python 3.8.10 (o superior)
- FastAPI
- Uvicorn
- Requests
- BeautifulSoup4
- SQLAlchemy (opcional, si se usa la base de datos)

## Instalación

1. Clona el repositorio.
2. Crea y activa un entorno virtual:
   - En Linux/macOS:
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```
   - En Windows:
     ```bash
     python -m venv env
     env\Scripts\activate
     ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
