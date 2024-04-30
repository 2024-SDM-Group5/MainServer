from pydantic import BaseModel, Field, HttpUrl
from typing import List
class SimplifiedMap(BaseModel):
    """For simplified maps in the Get_Maps listing"""
    id: int
    name: str
    iconUrl: HttpUrl = Field(None)
    author: str
    authorId: int
    viewCount: int
    collectCount: int
    hasCollected: bool = Field(..., description="Flag indicating if the map is currently being favorited by the authenticated user")
    center: dict  # Contains 'lat' and 'lng' fields

SimplifiedMaps_Ex =  [
    {
        "id": 11,
        "name": "台北飲料地圖",
        "iconUrl": "https://picsum.photos/200",
        "author": "enip",
        "authorId": 1,
        "viewCount": 441,
        "collectCount": 189,
        "hasCollected": True,
        "center": {
            "lat": 25.0329694,
            "lng": 121.5654118
        }
    },
    {
        "id": 12,
        "name": "飲料導覽",
        "iconUrl": "https://picsum.photos/200",
        "author": "enip",
        "authorId": 1,
        "viewCount": 370,
        "collectCount": 152,
        "hasCollected": False,
        "center": {
            "lat": 25.0329694,
            "lng": 121.5654118
        }
    },
    {
        "id": 13,
        "name": "夜市飲料攻略",
        "iconUrl": "https://picsum.photos/200",
        "author": "enip",
        "authorId": 1,
        "viewCount": 295,
        "collectCount": 117,
        "hasCollected": False,
        "center": {
            "lat": 25.0329694,
            "lng": 121.5654118
        }
    }
]

class PaginatedMapResponse(BaseModel):
    total: int
    maps: List[SimplifiedMap]
    limit: int
    offset: int

class CompleteMap(SimplifiedMap):
    """For complete maps in the Get_Maps listing"""
    description: str

CompleteMap_Ex = {
    "id": 11,
    "name": "台北飲料地圖",
    "iconUrl": "https://picsum.photos/200",
    "center": {
        "lat": 25.0329694,
        "lng": 121.5654118
    },
    "author": "enip",
    "authorId": 1,
    "viewCount": 441,
    "collectCount": 189,
    "hasCollected": False,
    "description": "這是一張台北市飲料地圖，收錄了許多好喝的飲料店！",
}


class MapCreate(BaseModel):
    map_name: str
    lat: float
    lng: float
    icon_url: HttpUrl = Field(None)
    tags: List[str] = []
    rest_ids: List[str] = []


class MapUpdate(MapCreate):
    id: int

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
