from fastapi import APIRouter, Path
from app.schemas.restaurants import Restaurant
from app.models.places_api import get_place_details
router = APIRouter(prefix="/api/v1/restaurants", tags=["restaurants"])


@router.get("/{place_id}", response_model=Restaurant)
async def get_single_restaurant(place_id: str = Path(...)):
    restaurant = await get_place_details(place_id)
    # restaurant_data = {
    #     "name": "Restaurant 1",
    #     "location": {
    #         "lat": 25.0329694,
    #         "lng": 121.5654177
    #     },
    #     "rating": 4.5,
    #     "placeId": "asdjglsakjgka",
    #     "viewCount": 400,
    #     "favCount": 100,
    #     "comments": [
    #         {"userId": 1, "date": "2024/1/23", "items": ["炒飯"], "content": "不錯", "rating": 5},
    #         {"userId": 2, "date": "2024/1/23", "items": ["炒麵"], "content": "不好吃", "rating": 1}
    #     ]
    # }
    print(restaurant)
    return restaurant