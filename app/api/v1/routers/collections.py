from fastapi import APIRouter, Depends
from typing import List
from app.schemas.collections import MapDisplay, RestaurantDisplay, DiaryDisplay
from app.schemas.users import UserLoginInfo
from app.dependencies.auth import get_current_user
router = APIRouter(prefix="/api/v1/collections", tags=["collections"])

@router.get("/map", response_model=List[MapDisplay])
async def get_map_collections(user: UserLoginInfo = Depends(get_current_user)):
    maps = [
        {
            "id": 11,
            "name": "台北飲料地圖",
            "iconUrl": "https://picsum.photos/200",
            "author": "enip",
            "viewCount": 441,
            "favCount": 189
        },
        {
            "id": 12,
            "name": "飲料導覽",
            "iconUrl": "https://picsum.photos/200",
            "author": "enip",
            "viewCount": 370,
            "favCount": 152
        },
        {
            "id": 13,
            "name": "夜市飲料攻略",
            "iconUrl": "https://picsum.photos/200",
            "author": "enip",
            "viewCount": 295,
            "favCount": 117
        }
    ]
    return maps


@router.get("/restaurant", response_model=List[RestaurantDisplay])
async def get_restaurant_collections(user: UserLoginInfo = Depends(get_current_user)):
    restaurants = [
        {
            "name": "Restaurant 1",
            "location": {
                "lat": 25.0329694,
                "lng": 121.5654177
            },
            "address": "台北市大安區辛亥路二段170號",
            "telephone": "02 1234 5554",
            "rating": 4.5,
            "placeId": "asdjglsakjgka",
            "viewCount": 400,
            "favCount": 100,
        },
        {
            "name": "Restaurant 2",
            "location": {
                "lat": 25.0329694,
                "lng": 121.5654177
            },
            "address": "台北市大安區辛亥路二段170號",
            "telephone": "02 1234 5554",
            "rating": 4.2,
            "placeId": "wewtwatqawt",
            "viewCount": 400,
            "favCount": 100,
        },
        {
            "name": "Restaurant 3",
            "location": {
                "lat": 25.0329694,
                "lng": 121.5654177
            },
            "address": "台北市大安區辛亥路二段170號",
            "telephone": "02 1234 5554",
            "rating": 4.2,
            "placeId": "wewtwatqawt",
            "viewCount": 400,
            "favCount": 100,
        }
    ]

    return restaurants

@router.get("/diary", response_model=List[DiaryDisplay])
async def get_my_detail(user: UserLoginInfo = Depends(get_current_user)):
    return [
        {
            "id": 1,
            "imageUrl": "https://picsum.photos/200"
        },
        {
            "id": 2,
            "imageUrl": "https://picsum.photos/200"
        },
        {
            "id": 3,
            "imageUrl": "https://picsum.photos/200"
        }
    ]