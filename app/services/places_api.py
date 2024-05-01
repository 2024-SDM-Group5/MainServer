import googlemaps
import requests
import json
from app.schemas.restaurants import Restaurant
from app.core.config import Config

api_key = Config.GOOGLE_MAPS_API_KEY
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
    photos = place.get('photos', [])
    photos = [photo['photo_reference'] for photo in photos]
    return {
        "name": name, 
        "address": address, 
        "placeId": place_id,
        "location": location, 
        "telephone": telephone, 
        "rating": rating,
        "photos": photos
    }


def search_nearby_restaurants(keyword, lat, lng, radius=1000):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'keyword': keyword,
        'language': 'zh-TW',
        'location': f'{lat},{lng}',
        'radius': 1000,
        'type': 'restaurant',
        'key': api_key,
        'opennow': True,
    }
    
    response = requests.get(url, params=params)
    results = response.json().get('results', [])

    filtered_results = [
        {
            'name': result.get('name'),
            'rating': result.get('rating'),
            'user_ratings_total': result.get('user_ratings_total'),
            'place_id': result.get('place_id'),
            'types': result.get('types'),
            'price_level': result.get('price_level'),
            'location': result.get('geometry', {}).get('location', {}),
            'photo_url': result.get('photos', [{}])[0].get('photo_reference', '')
        } 
        for result in results
    ]
    print(filtered_results[0])
    return filtered_results

