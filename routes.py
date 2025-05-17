# routes.py
import os, requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

GEOCODE_URL      = "https://maps.googleapis.com/maps/api/geocode/json"
DIRECTIONS_URL   = "https://maps.googleapis.com/maps/api/directions/json"
DISTMATRIX_URL   = "https://maps.googleapis.com/maps/api/distancematrix/json"

def geocode(place: str):
    params = {"address": place, "key": API_KEY}
    r = requests.get(GEOCODE_URL, params=params).json()
    if r.get("status") != "OK":
        raise Exception(f"Geocoding error for {place}: {r.get('status')}")
    loc = r["results"][0]["geometry"]["location"]
    return loc["lat"], loc["lng"]

def get_directions(origin: str, destination: str, mode: str="driving"):
    params = {
        "origin": origin, "destination": destination,
        "mode": mode, "key": API_KEY
    }
    r = requests.get(DIRECTIONS_URL, params=params).json()
    if r.get("status") != "OK":
        raise Exception(f"Directions error: {r.get('status')}")
    route = r["routes"][0]
    leg   = route["legs"][0]
    return {
        "polyline": route["overview_polyline"]["points"],
        "distance": leg["distance"]["text"],
        "duration": leg["duration"]["text"]
    }

def get_distance_matrix(locations: list[str], mode: str="driving"):
    params = {
        "origins":   "|".join(locations),
        "destinations": "|".join(locations),
        "mode":      mode,
        "key":       API_KEY
    }
    r = requests.get(DISTMATRIX_URL, params=params).json()
    if r.get("status") != "OK":
        raise Exception(f"Distance Matrix error: {r.get('status')}")
    matrix = []
    for row in r["rows"]:
        matrix.append([elem["distance"]["value"] for elem in row["elements"]])
    return matrix  # in meters
