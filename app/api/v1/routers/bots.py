from fastapi import APIRouter, HTTPException
from app.schemas.bots import BotRequest, BotResponse
from app.services.openai import gpt_query
from app.services.places_api import search_nearby_restaurants
router = APIRouter(prefix="/api/v1/bots", tags=["bots"])

@router.post("/question", response_model=BotResponse)
async def question(user_data: BotRequest):
    position = user_data.position
    keyword = user_data.req
    restaurants = search_nearby_restaurants(keyword, position.lat, position.lng)
    response, error = gpt_query(user_data.req, restaurants)
    if error:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return BotResponse(res=response)