import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GEOCODE_URL = os.getenv("GEOCODE_URL", "https://geocoding-api.open-meteo.com/v1/search")

FORECAST_URL = os.getenv("FORECAST_URL", "https://api.open-meteo.com/v1/forecast")

WEATHER_REQUEST_TIMEOUT = int(os.getenv("WEATHER_REQUEST_TIMEOUT", "10"))

PROJECT_ROOT = Path(__file__).parent

PROMPTS_DIR = PROJECT_ROOT / "prompts"