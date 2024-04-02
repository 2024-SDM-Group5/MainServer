from pydantic import BaseModel, Field, HttpUrl

class Restaurant(BaseModel):
    name: str
    location: dict
    rating: float = Field(None, ge=0, le=5)  # Optional rating, between 0 and 5
    placeId: str
    viewCount: int = Field(0, ge=0)  
    favCount: int = Field(0, ge=0)  

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
    restaurants: list[Restaurant]
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
    restaurants: list[Restaurant] 

class PostResponse(BaseModel):
    success: bool
    message: str

class PutResponse(PostResponse):
    pass