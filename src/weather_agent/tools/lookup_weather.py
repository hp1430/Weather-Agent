import requests
from ..config import GEOCODE_URL, WEATHER_REQUEST_TIMEOUT

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

        print(lat, lon)
        

    except requests.exceptions.RequestException as err:
        return f"We couldn't look up the weather for {location}: {err}"
    except Exception as err:
        return f"Unexpected weather response error: {err}"

lookup_weather(location="London")