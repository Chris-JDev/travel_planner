# app.py
import streamlit as st
from dotenv import load_dotenv
from routes import geocode, get_distance_matrix, get_directions
from flights import get_flight_price
from weather import get_current_weather
from utils import solve_tsp_bruteforce
from streamlit_folium import folium_static
import folium, polyline

load_dotenv()
st.title("🌍 Multi-Stop Optimal Itinerary Planner")

# 1. User inputs
raw = st.text_area(
    "Enter each place you want to visit (one per line):",
    "Dubai, UAE\nParis, France\nLondon, UK\nRome, Italy"
)
places = [p.strip() for p in raw.splitlines() if p.strip()]
if len(places) < 2:
    st.warning("Please enter at least two places.")
    st.stop()

start = st.selectbox("Select your starting point:", places)

mode = st.selectbox("Transport mode:", ["driving", "walking", "bicycling", "transit"])
travel_date = st.date_input("Travel date (for flights/weather):")

if st.button("Compute Optimal Route"):
    # 2. Reorder so start is first
    places = [start] + [p for p in places if p != start]

    # 3. Fetch distance matrix
    with st.spinner("Computing distance matrix…"):
        matrix = get_distance_matrix(places, mode=mode)

    # 4. Solve TSP
    order, cost_meters = solve_tsp_bruteforce(matrix, start_index=0)
    ordered_places = [places[i] for i in order]

    st.subheader("🔀 Visit Order")
    for i, place in enumerate(ordered_places, 1):
        st.markdown(f"**{i}.** {place}")

    st.write(f"**Total ground distance:** {cost_meters/1000:.1f} km")

    # 5. For each leg, get directions & build a combined polyline
    full_coords = []
    st.subheader("🚗 Leg Details")
    for i in range(len(ordered_places)-1):
        a, b = ordered_places[i], ordered_places[i+1]
        leg = get_directions(a, b, mode)
        st.markdown(f"**{i+1}. {a} → {b}:** {leg['distance']} in {leg['duration']}")
        coords = polyline.decode(leg["polyline"])
        full_coords.extend(coords if not full_coords else coords[1:])  # avoid dup endpoints

    # 6. Optionally: get flight price between start & end
    orig_code = ordered_places[0].split(",")[0][:3].upper()
    dest_code= ordered_places[-1].split(",")[0][:3].upper()
    price = get_flight_price(orig_code, dest_code, str(travel_date))
    if price:
        st.write(f"✈️ **Estimated flight cost** from {ordered_places[0]} to {ordered_places[-1]}: ${price}")

    # 7. Current weather at final stop
    w = get_current_weather(ordered_places[-1])
    st.write(f"🌤️ **Current weather in {ordered_places[-1].split(',')[0]}:** {w['temp']}°C, {w['conditions']}")

    # 8. Render on map
    m = folium.Map(location=full_coords[0], zoom_start=6)
    folium.PolyLine(full_coords, weight=5).add_to(m)
    # mark each stop
    for idx, coord in enumerate(full_coords[:: len(full_coords)//(len(ordered_places)-1) or 1]):
        folium.Marker(coord, tooltip=ordered_places[idx]).add_to(m)

    folium_static(m)
