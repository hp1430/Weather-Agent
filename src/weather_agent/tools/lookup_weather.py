import requests
from ..constants import WEATHER_CODES
from ..config import GEOCODE_URL, WEATHER_REQUEST_TIMEOUT, FORECAST_URL

def lookup_weather(location: str) -> str:
    try:
        geo = requests.get(
            GEOCODE_URL,
            params={
                "name": location,
                "count": 1
            },
            timeout=WEATHER_REQUEST_TIMEOUT
        )

        geo.raise_for_status()

        matches = geo.json().get("results")

        if not matches:
            return f"We couldn't find a place called {location}"
        
        place = matches[0]

        lat, lon = place.get("latitude"), place.get("longitude")

        label = ", ".join(
            part for part in (place.get("name"), place.get("country")) if part
        )

        forecast = requests.get(
            FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,weather_code,wind_speed_10m"
            },
            timeout=WEATHER_REQUEST_TIMEOUT
        )

        forecast.raise_for_status()

        current = forecast.json().get("current")

        temperature = current.get("temperature_2m")
        weather_code = current.get("weather_code")
        wind_speed = current.get("wind_speed_10m")

        sky = WEATHER_CODES.get(weather_code, f"weather code {weather_code}")

        wind_note = f", wind {wind_speed} km/h" if wind_speed else ""

        return f"The current temperature in {label} is {temperature}°C, the sky is {sky}{wind_note}."


    except requests.exceptions.RequestException as err:
        return f"We couldn't look up the weather for {location}: {err}"
    except Exception as err:
        return f"Unexpected weather response error: {err}"