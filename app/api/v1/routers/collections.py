from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.schemas.maps import SimplifiedMap, SimplifiedMaps_Ex
from app.schemas.diaries import SimplifiedDiary, SimplifiedDiary_Ex
from app.schemas.restaurants import SimplifiedRestaurant, SimplifiedRestaurant_Ex
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

@router.get("/map", response_model=List[SimplifiedMap])
async def get_map_collections(
    user: UserLoginInfo = Depends(get_current_user),
    db: orm.Session=fastapi.Depends(get_db),
    orderBy: str = Query("collectCount", enum=["collectCount", "createTime"]),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    q: Optional[str] = Query(None),
):
    maps = SimplifiedMaps_Ex
    # maps = []
    # map_ids = await db.query(dbModel.UserMapCollect).with_entities(dbModel.UserMapCollect.map_id).filter(dbModel.UserMapCollect.user_id == user).all()
    # for id in map_ids:
    #     map = await db.query(dbModel.Map).filter(dbModel.Map.map_id == id).first()
    #     author = await db.query(dbModel.User).with_entities(dbModel.User.user_name).filter(dbModel.User.user_name == map.author).first()
    #     maps.append(SimplifiedMap(id=map.map_id, name=map.map_name, iconUrl=map.icon_url, author=author, viewCount=map.view_cnt, collectCount=map.collect_cnt))
    return maps


@router.get("/restaurant", response_model=List[SimplifiedRestaurant])
async def get_restaurant_collections(user: UserLoginInfo = Depends(get_current_user)):
    restaurants = SimplifiedRestaurant_Ex
    return restaurants

@router.get("/diary", response_model=List[SimplifiedDiary])
async def get_my_detail(user: UserLoginInfo = Depends(get_current_user)):
    diaries = SimplifiedDiary_Ex
    return diaries