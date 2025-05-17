# flights.py
import os
from dotenv import load_dotenv
from amadeus import Client, ResponseError

load_dotenv()

AMADEUS_CLIENT_ID     = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")

amadeus = Client(
    client_id=AMADEUS_CLIENT_ID,
    client_secret=AMADEUS_CLIENT_SECRET
)

def get_flight_price(origin_code: str, destination_code: str, date: str):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin_code,
            destinationLocationCode=destination_code,
            departureDate=date,
            adults=1,
            max=1
        )
        offers = response.data
        if not offers:
            return None
        return offers[0]["price"]["total"]
    except ResponseError as e:
        print(f"Amadeus API error: {e}")
        return None
