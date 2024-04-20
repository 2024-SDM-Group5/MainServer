from pydantic import BaseModel, Field, HttpUrl
from app.schemas.diaries import SimpleDiary
from typing import List
class SimplifiedRestaurant(BaseModel):
    name: str
    address: str
    location: dict
    telephone: str
    rating: float = Field(None, ge=0, le=5)
    placeId: str
    viewCount: int = Field(0, ge=0)  
    favCount: int = Field(0, ge=0)

class PaginatedRestaurantResponse(BaseModel):
    total: int
    restaurants: List[SimplifiedRestaurant]
    limit: int
    offset: int

class Restaurant(SimplifiedRestaurant):
    diaries: list[SimpleDiary]
    hasFavorited: bool = Field(..., description="Flag indicating if the restaurant is currently being favorited by the authenticated user")