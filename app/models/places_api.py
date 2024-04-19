import googlemaps
from dotenv import load_dotenv
import os
from app.schemas.restaurants import Restaurant
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv('GOOGLE_MAPS_API_KEY')
if not api_key:
    raise ValueError("No API key provided. Set GOOGLE_MAPS_API_KEY environment variable.")

async def get_places(lat, lng, radius):
    """
    Get places around a given latitude and longitude with a given radius.
    """
    gmaps = googlemaps.Client(key=api_key)
    places = gmaps.places(query="restaurant", location=f"{lat},{lng}", radius=radius)
    return places

async def get_place_details(place_id):
    """
    Get details about a specific place.
    """
    gmaps = googlemaps.Client(key=api_key)
    place = gmaps.place(place_id)['result']
    place_id = place['place_id']
    location = place['geometry']['location']
    name = place.get('name', '')
    address = place.get('formatted_address', '')
    telephone = place.get('formatted_phone_number', '')
    rating = place.get('rating', 0)
    return Restaurant(
        name=name, 
        address=address, 
        placeId=place_id,
        location=location, 
        telephone=telephone, 
        rating=rating,
        viewCount=0,
        favCount=0,
        comments=[],
        hasFavorited=False
    )
