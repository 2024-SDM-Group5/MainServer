from pydantic import BaseModel
from app.schemas.maps import SimplifiedMap
from app.schemas.restaurants import SimplifiedRestaurant

class MapDisplay(SimplifiedMap):
    pass

class DiaryDisplay(BaseModel):
    id: int
    imageUrl: str

class RestaurantDisplay(SimplifiedRestaurant):
    pass
    