from fastapi import APIRouter, HTTPException, Depends
from app.schemas.bots import BotRequest, BotResponse
from app.schemas.restaurants import CreateRestaurant
from app.services.openai import gpt_query, request_rewriting
from app.services.places_api import search_nearby_restaurants
from app.crud.restaurants import bulk_insert
from app.crud.diaries import recommend_diary
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
router = APIRouter(prefix="/api/v1/bots", tags=["bots"])

@router.post("/question", response_model=BotResponse)
async def question(
    user_data: BotRequest, db = Depends(get_db),
    user = Depends(get_current_user)
):
    position = user_data.position
    keyword = user_data.req

    keyword, error = request_rewriting(keyword)
    if error:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    restaurants = search_nearby_restaurants(keyword, position.lat, position.lng)
    diaries = recommend_diary(db, user.userId)
    db_restaurants = [CreateRestaurant(**restaurant) for restaurant in restaurants]
    bulk_insert(db, db_restaurants)

    filtered_restaurants = [
        {
            'name': restaurant.get('name', ''),
            'rating': restaurant.get('rating', 0.0),
            'user_ratings_total': restaurant.get('user_ratings_total', 0),
            'place_id': restaurant.get('place_id', ''),
            'types': restaurant.get('types', []),
            'price_level': restaurant.get('price_level', 0),
            'my_comment': []
        } for restaurant in restaurants
    ]

    for diary in diaries:
        diary_insert = diary._asdict()
        diary_insert.pop('place_id', None)
        for restaurant in filtered_restaurants:
            if diary.place_id == restaurant['place_id']:
                restaurant['my_comment'].append(diary_insert)

    if not filtered_restaurants:
        response = "對不起，附近沒有符合條件的餐廳，試試看其他關鍵字吧！"
        BotResponse(res=response, placeId="")


    recommend_id = None
    retry = 0
    while recommend_id is None and retry < 5:
        retry += 1
        response, error = gpt_query(user_data.req, filtered_restaurants)
        if response != "" and error:
            return BotResponse(res=response, placeId="")
        for restaurant in restaurants:
            if restaurant['name'] in response:
                recommend_id = restaurant['place_id']
                break
        print("Retrying...")

    if error:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return BotResponse(res=response, placeId=recommend_id)