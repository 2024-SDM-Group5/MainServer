from pydantic import BaseModel, Field, HttpUrl
from app.schemas.diaries import SimplifiedDiary
from typing import List
class SimplifiedRestaurant(BaseModel):
    name: str
    location: dict
    rating: float = Field(None, ge=0, le=5)
    placeId: str
    viewCount: int = Field(0, ge=0)  
    collectCount: int = Field(..., ge=0)
    likeCount: int = Field(..., ge=0)
    dislikeCount: int = Field(..., ge=0)
    hasCollected: bool = Field(..., description="Flag indicating if the restaurant is currently being collected by the authenticated user")
    hasLiked: bool = Field(..., description="Flag indicating if the restaurant is currently being liked by the authenticated user")
    hasDisliked: bool = Field(..., description="Flag indicating if the restaurant is currently being disliked by the authenticated user")
    photoUrl: str = Field(None)

SimplifiedRestaurant_Ex = [
    {
        "name": "Restaurant 1",
        "location": {
            "lat": 25.0329694,
            "lng": 121.5654177
        },
        "rating": 4.5,
        "placeId": "ChIJexSiLC-qQjQR0LgDorEWhig",
        "viewCount": 400,
        "collectCount": 100,
        "likeCount": 100,
        "dislikeCount": 100,
        "hasCollected": False,
        "hasLiked": False,
        "hasDisliked": False,
        "photoUrl": "https://picsum.photos/200"
    },
    {
        "name": "Restaurant 2",
        "location": {
            "lat": 25.0329694,
            "lng": 121.5654177
        },
        "rating": 4.2,
        "placeId": "ChIJexSiLC-qQjQR0LgDorEWhig",
        "viewCount": 400,
        "collectCount": 100,
        "likeCount": 101,
        "dislikeCount": 100,
        "hasCollected": True,
        "hasLiked": False,
        "hasDisliked": False,
        "photoUrl": "https://picsum.photos/200"
    },
    {
        "name": "Restaurant 3",
        "location": {
            "lat": 25.0329694,
            "lng": 121.5654177
        },
        "rating": 4.2,
        "placeId": "ChIJexSiLC-qQjQR0LgDorEWhig",
        "viewCount": 400,
        "collectCount": 100,
        "likeCount": 100,
        "dislikeCount": 100,
        "hasCollected": False,
        "hasLiked": False,
        "hasDisliked": True,
        "photoUrl": "https://picsum.photos/200"
    }
]

class CreateRestaurant(BaseModel):
    name: str
    location: dict
    rating: float = Field(None, ge=0, le=5)
    place_id: str
    photo_url: str = Field(None)

class FullCreateRestaurant(CreateRestaurant):
    address: str
    telephone: str

class PaginatedRestaurantResponse(BaseModel):
    total: int
    restaurants: List[SimplifiedRestaurant]
    limit: int
    offset: int

class Restaurant(SimplifiedRestaurant):
    telephone: str
    address: str
    diaries: list[SimplifiedDiary] = Field([], description="List of diaries associated with the restaurant")
    # photos: list[str] = Field([], description="List of photo references for the restaurant")
class PostResponse(BaseModel):
    success: bool
    message: str