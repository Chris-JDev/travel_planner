import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")

# --- Helper functions ---------------------------------------------------

def fetch_place_suggestions(input_text: str) -> list[str]:
    """Call Google Places Autocomplete API to get address suggestions."""
    url = (
        "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        f"?input={input_text}&key={GOOGLE_KEY}"
    )
    resp = requests.get(url).json()
    return [p["description"] for p in resp.get("predictions", [])]

def get_place_coordinates(address: str) -> tuple[float, float]:
    """Call Google Geocoding API to convert address into (lat, lng)."""
    url = (
        "https://maps.googleapis.com/maps/api/geocode/json"
        f"?address={address}&key={GOOGLE_KEY}"
    )
    res = requests.get(url).json()
    loc = res["results"][0]["geometry"]["location"]
    return loc["lat"], loc["lng"]

# --- Streamlit UI -------------------------------------------------------

st.title("🧳 Wander-log Clone")

# 1. Text input for search
place = st.text_input("Search a place to add:")

if place:
    # 2. Show autocomplete suggestions
    suggestions = fetch_place_suggestions(place)
    choice = st.selectbox("Did you mean…", suggestions)

    if choice:
        # 3. Geocode the chosen address
        lat, lng = get_place_coordinates(choice)

        # 4. Display on map
        st.map([{"lat": lat, "lon": lng}], zoom=12)
