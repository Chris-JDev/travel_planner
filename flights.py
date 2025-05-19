import os
import requests
from dotenv import load_dotenv

load_dotenv()

AVIATIONSTACK_ACCESS_KEY = os.getenv("AVIATIONSTACK_ACCESS_KEY")

def get_flight_price(origin_code: str, destination_code: str, date: str):
    url = f"http://api.aviationstack.com/v1/flights"
    params = {
        'access_key': AVIATIONSTACK_ACCESS_KEY,
        'origin': origin_code,
        'destination': destination_code,
        'date': date,
        'limit': 1  # Limit to 1 result
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Check if the response contains flight data
        if 'data' in data and data['data']:
            return data['data'][0]['price']  # Adjust based on the actual response structure
        else:
            return None
    except Exception as e:
        print(f"Error fetching flight data: {e}")
        return None
