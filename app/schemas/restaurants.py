from pydantic import BaseModel, Field, HttpUrl
from app.schemas.comments import Comment

class SimplifiedRestaurant(BaseModel):
    name: str
    location: dict
    rating: float = Field(None, ge=0, le=5)
    placeId: str
    viewCount: int = Field(0, ge=0)  
    favCount: int = Field(0, ge=0)  

class Restaurant(SimplifiedRestaurant):
    comments: list[Comment]