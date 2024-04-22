from pydantic import BaseModel, Field, HttpUrl
from app.schemas.diaries import SimplifiedDiary
from typing import List
class SimplifiedRestaurant(BaseModel):
    name: str
    address: str
    location: dict
    telephone: str
    rating: float = Field(None, ge=0, le=5)
    placeId: str
    viewCount: int = Field(0, ge=0)  
    collectCount: int = Field(..., ge=0)
    likeCount: int = Field(..., ge=0)
    dislikeCount: int = Field(..., ge=0)

class PaginatedRestaurantResponse(BaseModel):
    total: int
    restaurants: List[SimplifiedRestaurant]
    limit: int
    offset: int

class Restaurant(SimplifiedRestaurant):
    diaries: list[SimplifiedDiary] = Field([], description="List of diaries associated with the restaurant")
    hasCollected: bool = Field(False, description="Flag indicating if the restaurant is currently being collected by the authenticated user")
    hasLiked: bool = Field(False, description="Flag indicating if the restaurant is currently being liked by the authenticated user")
    hasDisliked: bool = Field(False, description="Flag indicating if the restaurant is currently being disliked by the authenticated user")
class PostResponse(BaseModel):
    success: bool
    message: str