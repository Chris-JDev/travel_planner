# weather.py
import os, requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
CLIMATE_URL = "https://api.openweathermap.org/data/2.5/climate/month"

def get_current_weather(city: str):
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    r = requests.get(CURRENT_WEATHER_URL, params=params).json()
    return {
        "temp": r["main"]["temp"],
        "conditions": r["weather"][0]["description"]
    }

def get_monthly_climate(lat, lon):
    params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY}
    r = requests.get(CLIMATE_URL, params=params).json()
    return r["list"]
