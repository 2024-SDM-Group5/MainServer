from pydantic import BaseModel, Field, HttpUrl
from app.schemas.comments import RestaurantComment

class SimplifiedRestaurant(BaseModel):
    name: str
    address: str
    location: dict
    telephone: str
    rating: float = Field(None, ge=0, le=5)
    placeId: str
    viewCount: int = Field(0, ge=0)  
    favCount: int = Field(0, ge=0)  

class Restaurant(SimplifiedRestaurant):
    comments: list[RestaurantComment]