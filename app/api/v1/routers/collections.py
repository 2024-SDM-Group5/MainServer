from fastapi import APIRouter, Depends
from typing import List
from app.schemas.collections import MapDisplay, RestaurantDisplay, DiaryDisplay
from app.schemas.users import UserLoginInfo
from app.dependencies.auth import get_current_user
import db.database as database
import sqlalchemy.orm as orm
import fastapi
import models.dbModel as dbModel
router = APIRouter(prefix="/api/v1/collections", tags=["collections"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/map", response_model=List[MapDisplay])
async def get_map_collections(user: UserLoginInfo = Depends(get_current_user), db: orm.Session=fastapi.Depends(get_db)):
    maps = [
        {
            "id": 11,
            "name": "台北飲料地圖",
            "iconUrl": "https://picsum.photos/200",
            "author": "enip",
            "viewCount": 441,
            "collectCount": 189
        },
        {
            "id": 12,
            "name": "飲料導覽",
            "iconUrl": "https://picsum.photos/200",
            "author": "enip",
            "viewCount": 370,
            "collectCount": 152
        },
        {
            "id": 13,
            "name": "夜市飲料攻略",
            "iconUrl": "https://picsum.photos/200",
            "author": "enip",
            "viewCount": 295,
            "collectCount": 117
        }
    ]
    maps = []
    map_ids = db.query(dbModel.UserMapCollect).with_entities(dbModel.UserMapCollect.map_id).filter(dbModel.UserMapCollect.user_id == user).all()
    for id in map_ids:
        map = db.query(dbModel.Map).filter(dbModel.Map.map_id == id).first()
        author = db.query(dbModel.User).with_entities(dbModel.User.user_name).filter(dbModel.User.user_name == map.author).first()
        maps.append(MapDisplay(id=map.map_id, name=map.map_name, iconUrl=map.icon_url, author=author, viewCount=map.view_cnt, collectCount=map.collect_cnt))
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
            "placeId": "ChIJexSiLC-qQjQR0LgDorEWhig",
            "viewCount": 400,
            "collectCount": 100,
            "likeCount": 100,
            "dislikeCount": 101
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
            "placeId": "ChIJexSiLC-qQjQR0LgDorEWhig",
            "viewCount": 400,
            "collectCount": 100,
            "likeCount": 100,
            "dislikeCount": 101
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
            "placeId": "ChIJexSiLC-qQjQR0LgDorEWhig",
            "viewCount": 400,
            "collectCount": 100,
            "likeCount": 100,
            "dislikeCount": 101
        }
    ]

    return restaurants

@router.get("/diary", response_model=List[DiaryDisplay])
async def get_my_detail(user: UserLoginInfo = Depends(get_current_user)):
    return [
        {
            "id": 1,
            "imageUrl": "https://picsum.photos/200",
            "restaurantName": "JJ Poke"
        },
        {
            "id": 2,
            "imageUrl": "https://picsum.photos/200",
            "restaurantName": "Boba Guys"
        },
        {
            "id": 3,
            "imageUrl": "https://picsum.photos/200",
            "restaurantName": "Happy Lemon"
        }
    ]