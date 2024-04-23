from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.schemas.maps import SimplifiedMap, SimplifiedMaps_Ex
from app.schemas.diaries import SimplifiedDiary, SimplifiedDiary_Ex
from app.schemas.restaurants import SimplifiedRestaurant, SimplifiedRestaurant_Ex
from app.schemas.users import UserLoginInfo
from app.dependencies.auth import get_current_user
from dependencies.db import get_db
from models import dbModel
from sqlalchemy.orm import Session
router = APIRouter(prefix="/api/v1/collections", tags=["collections"])

@router.get("/map", response_model=List[SimplifiedMap])
async def get_map_collections(
    db: Session = Depends(get_db),
    user: UserLoginInfo = Depends(get_current_user),
    orderBy: str = Query("collectCount", enum=["collectCount", "createTime"]),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    q: Optional[str] = Query(None),
):
    maps = db.query(dbModel.UserMapCollect).filter(dbModel.UserMapCollect.user_id == user.userId).all()
    map_ids = list(map(lambda x: x.map_id, maps))
    query = db.query(dbModel.Map).filter(dbModel.Map.map_id.in_(map_ids))
    if q:
        query = query.filter(dbModel.Map.map_name.ilike(f"%{q}%"))
    
    if orderBy == "collect_cnt":
        query = query.order_by(dbModel.Map.collect_cnt.desc())
    elif orderBy == "created":
        query = query.order_by(dbModel.Map.created.desc())
    
    query = query.offset(offset).limit(limit)
    map_collections = query.all()
    simplified_maps = [
        SimplifiedMap(
            id=map_instance.map_id,
            name=map_instance.map_name,
            iconUrl=map_instance.icon_url,
            author=db.query(dbModel.User).filter(dbModel.User.user_id == map_instance.author).first().user_name,
            authorId=map_instance.author,
            viewCount=map_instance.view_cnt,
            collectCount=map_instance.collect_cnt,
            hasCollected=True,  # Assuming this is always False for now
            center={"lat": map_instance.lat, "lng": map_instance.lng}
        )
        for map_instance in map_collections
    ]
    #maps = SimplifiedMaps_Ex
    return simplified_maps


@router.get("/restaurant", response_model=List[SimplifiedRestaurant])
async def get_restaurant_collections(user: UserLoginInfo = Depends(get_current_user)):
    restaurants = SimplifiedRestaurant_Ex
    return restaurants

@router.get("/diary", response_model=List[SimplifiedDiary])
async def get_my_detail(user: UserLoginInfo = Depends(get_current_user)):
    diaries = SimplifiedDiary_Ex
    return diaries