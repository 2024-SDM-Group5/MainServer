from pydantic import BaseModel, Field, HttpUrl
from app.schemas.restaurants import SimplifiedRestaurant

class SimplifiedMap(BaseModel):
    """For simplified maps in the Get_Maps listing"""
    id: int
    name: str
    iconUrl: HttpUrl = Field(None)
    author: str
    viewCount: int
    favCount: int

class CompleteMap(SimplifiedMap):
    """For complete maps in the Get_Maps listing"""
    restaurants: list[SimplifiedRestaurant]
    center: dict  # Contains 'lat' and 'lng' fields

class MapCreate(BaseModel):
    name: str
    iconUrl: HttpUrl = Field(None)
    authorId: int
    tags: list[str]
    restaurants: list[str]

class MapUpdate(MapCreate):
    """Reuses MapCreate as a base, all fields remain optional for updates"""
    pass 

class MapDisplay(BaseModel):
    id: int
    name: str
    iconUrl: HttpUrl = Field(None)
    center: dict  # Contains 'lat' and 'lng' fields
    author: str
    viewCount: int
    favCount: int 
    restaurants: list[SimplifiedRestaurant] 

class PostResponse(BaseModel):
    success: bool
    message: str

class PutResponse(PostResponse):
    pass