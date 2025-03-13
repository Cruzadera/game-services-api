# Game Services API

This API provides endpoints to query information about video game streaming services—including Xbox Game Pass (and related services like Xbox Cloud Gaming), Amazon Luna, GeForce Now, and others—by scraping the respective websites.

## Requirements

- Python 3.8.10 (or later)
- FastAPI
- Uvicorn
- Requests
- BeautifulSoup4
- SQLAlchemy (optional, if you plan to use a database)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YourUsername/game-services-api.git
   cd game-services-api

2. Create and activate a virtual environment:
   - On Linux/macOS:
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```
   - On Windows:
     ```bash
     python -m venv env
     env\Scripts\activate
     ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt

4. Running the API Locally
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 10000 --reload
  ```
Your API will be available at http://localhost:10000.