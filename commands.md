# Konfiguracja
- Przygotowanie środowiska:
- - `cp .env.example .env`
- - wypłenienie danych w ".env"

# Instalacja zależności
- Produkcyjne:
- - `pip install -r requirements.txt`
- Developerskie: 
- - `pip install -r requirements-dev.txt`

# Lokalnie (bez dockera)
- Uruchomienie serwera aplikacyjnego:
- `uvicorn reservationapi.src.main:app --host 0.0.0.0 --port 8000`

# Docker
- Budowanie projektu (z odświeżeniem cache):
- - `docker compose build --no-cache`
- Uruchomienie projektu:
- - `docker compose up`
- Zatrzymanie kontenerów:
- - `docker compose down`

# Dokumentacja API
- Swagger:
- - `http://localhost:8000/docs`
