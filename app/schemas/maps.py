from pydantic import BaseModel, Field, HttpUrl
from app.schemas.restaurants import SimplifiedRestaurant
from typing import List
class SimplifiedMap(BaseModel):
    """For simplified maps in the Get_Maps listing"""
    id: int
    name: str
    iconUrl: HttpUrl = Field(None)
    author: str
    viewCount: int
    favCount: int

class PaginatedMapResponse(BaseModel):
    total: int
    maps: List[SimplifiedMap]
    limit: int
    offset: int

class CompleteMap(SimplifiedMap):
    """For complete maps in the Get_Maps listing"""
    center: dict  # Contains 'lat' and 'lng' fields
    hasCollected: bool = Field(..., description="Flag indicating if the map is currently being favorited by the authenticated user")

class MapCreate(BaseModel):
    name: str
    iconUrl: HttpUrl = Field(None)
    authorId: int
    tags: list[str]
    restaurants: list[str] = Field([])

class MapUpdate(MapCreate):
    """Reuses MapCreate as a base, all fields remain optional for updates"""
    pass 

class MapDisplay(BaseModel):
    id: int
    name: str
    iconUrl: HttpUrl = Field(None)
    center: dict
    author: str
    viewCount: int
    favCount: int 

class PostResponse(BaseModel):
    success: bool
    message: str

class PutResponse(PostResponse):
    pass