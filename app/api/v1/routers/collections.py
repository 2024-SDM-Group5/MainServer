from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.schemas.maps import SimplifiedMap, SimplifiedMaps_Ex
from app.schemas.diaries import SimplifiedDiary, SimplifiedDiary_Ex
from app.schemas.restaurants import SimplifiedRestaurant, SimplifiedRestaurant_Ex
from app.schemas.users import UserLoginInfo
from app.dependencies.auth import get_current_user
router = APIRouter(prefix="/api/v1/collections", tags=["collections"])

@router.get("/map", response_model=List[SimplifiedMap])
async def get_map_collections(
    user: UserLoginInfo = Depends(get_current_user),
    orderBy: str = Query("collectCount", enum=["collectCount", "createTime"]),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    q: Optional[str] = Query(None),
):
    maps = SimplifiedMaps_Ex
    return maps


@router.get("/restaurant", response_model=List[SimplifiedRestaurant])
async def get_restaurant_collections(user: UserLoginInfo = Depends(get_current_user)):
    restaurants = SimplifiedRestaurant_Ex
    return restaurants

@router.get("/diary", response_model=List[SimplifiedDiary])
async def get_my_detail(user: UserLoginInfo = Depends(get_current_user)):
    diaries = SimplifiedDiary_Ex
    return diaries