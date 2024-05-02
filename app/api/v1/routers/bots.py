from fastapi import APIRouter, HTTPException, Depends
from app.schemas.bots import BotRequest, BotResponse
from app.schemas.restaurants import CreateRestaurant
from app.services.openai import gpt_query
from app.services.places_api import search_nearby_restaurants
from app.crud.restaurants import bulk_insert
from app.dependencies.db import get_db
router = APIRouter(prefix="/api/v1/bots", tags=["bots"])

@router.post("/question", response_model=BotResponse)
async def question(user_data: BotRequest, db = Depends(get_db)):
    position = user_data.position
    keyword = user_data.req
    restaurants = search_nearby_restaurants(keyword, position.lat, position.lng)
    db_restaurants = [CreateRestaurant(**restaurant) for restaurant in restaurants]
    bulk_insert(db, db_restaurants)

    filtered_restaurants = [
        {
            'name': restaurant.get('name', ''),
            'rating': restaurant.get('rating', 0.0),
            'user_ratings_total': restaurant.get('user_ratings_total', 0),
            'place_id': restaurant.get('place_id', ''),
            'types': restaurant.get('types', []),
            'price_level': restaurant.get('price_level', 0)
        } for restaurant in restaurants
    ]

    response, error = gpt_query(user_data.req, filtered_restaurants)
    if error:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return BotResponse(res=response)