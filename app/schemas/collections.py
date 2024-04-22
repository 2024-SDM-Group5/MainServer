from pydantic import BaseModel
from app.schemas.maps import SimplifiedMap
from app.schemas.restaurants import SimplifiedRestaurant
from app.schemas.diaries import SimplifiedDiary
class MapDisplay(SimplifiedMap):
    pass

class DiaryDisplay(SimplifiedDiary):
    pass
class RestaurantDisplay(SimplifiedRestaurant):
    pass
    