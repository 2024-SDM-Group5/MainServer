import googlemaps
from dotenv import load_dotenv
import os
import asyncio
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
    name = place['name']
    address = place['formatted_address']
    telephone = place['formatted_phone_number']
    rating = place['rating']
    location = place['geometry']['location']
    return Restaurant(
        name=name, 
        address=address, 
        placeId=place_id,
        location=location, 
        telephone=telephone, 
        rating=rating,
        viewCount=0,
        favCount=0,
        comments=[]
    )

if __name__ == '__main__':
    # places = asyncio.run(get_places(25.0329694, 121.5654118, 1000))
    # print(places)
    place = asyncio.run(get_place_details("ChIJjfzEsLCrQjQRLJYMdi8QOaM"))
    print(place)
