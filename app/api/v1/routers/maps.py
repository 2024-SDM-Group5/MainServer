from fastapi import APIRouter, Depends, Query, Path
from typing import List, Optional
import logging
from fastapi.exceptions import HTTPException

from app.models.dbModel import Map
from app.schemas.maps import (
    SimplifiedMap,
    MapCreate, 
    MapUpdate, 
    CompleteMap, 
    PostResponse,
    PutResponse, 
    PaginatedMapResponse,
    SimplifiedMaps_Ex,
    CompleteMap_Ex
)
from app.dependencies.auth import get_current_user, get_optional_user
from app.schemas.users import UserLoginInfo
from app.schemas.restaurants import PaginatedRestaurantResponse, SimplifiedRestaurant_Ex
from app.dependencies.db import get_db
from app.services.cloud_storage import save_file_to_gcs
import app.crud.maps as crud_map
import app.crud.users as crud_user

router = APIRouter(prefix="/api/v1/maps", tags=["maps"])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@router.get("", response_model=PaginatedMapResponse)
async def get_maps(
    orderBy: str = Query("favCount", enum=["favCount", "createTime"]),
    tags: Optional[List[str]] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    reverse: bool = Query(False),
    q: Optional[str] = Query(None),
    db = Depends(get_db)
):
    map_lists = crud_map.get_maps(db, offset, limit)
    map_results = [
        SimplifiedMap(
            id=permap.map_id,
            name=permap.map_name,
            center={"lat": permap.lat, "lng": permap.lng},
            authorId=permap.author,
            viewCount=permap.view_cnt,
            iconUrl=permap.icon_url if permap.icon_url else None
        ) 
        for permap in map_lists
    ]
    return PaginatedMapResponse(
        total=len(map_lists),
        maps=map_results,
        limit=limit,
        offset=offset
    )

# --- Create_Map ---
@router.post("", response_model=PostResponse, status_code=201)
async def create_map(
    map_data: MapCreate, 
    user: UserLoginInfo = Depends(get_current_user), 
    db = Depends(get_db)
):
    try:
        map_res = crud_map.create_map(db, map_data, user)
        return {
            "success": True,
            "message": f"User {user.userId} created map number {map_res}",
            }
    except Exception as e:
        logger.error(f"Error in create_map: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error - Failed to create map")

# --- Single_Map ---
@router.get("/{id}", response_model=CompleteMap)
async def get_single_map(
    id: int = Path(...), 
    user: Optional[UserLoginInfo] = Depends(get_optional_user),
    db = Depends(get_db)
):
    try:
        permap = crud_map.get_map(db, id)
        user_info = crud_user.get_user_by_id(db, user.userId)
        map_result = CompleteMap(
            id=permap.map_id,
            name=permap.map_name,
            center={"lat": permap.lat, "lng": permap.lng},
            authorId=permap.author,
            viewCount=permap.view_cnt,
            author=user_info.user_name, 
            hasCollected=False,
        )
        if permap.icon_url:
            map_result.iconUrl = permap.icon_url
        if user:
            map_result.hasCollected = True
        return map_result
    except Exception as e:
        logger.error(f"Error in get_maps: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error - Failed to get maps")

@router.get("/{id}/restaurants", response_model=PaginatedRestaurantResponse)
async def get_restaurants(
    id: int = Path(...),
    orderBy: str = Query("favCount", enum=["favCount", "createTime"]),
    tags: Optional[List[str]] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    reverse: bool = Query(False),
    q: Optional[str] = Query(None),
    sw: Optional[str] = Query(None),
    ne: Optional[str] = Query(None),
    user: Optional[UserLoginInfo] = Depends(get_optional_user),
    db = Depends(get_db)
):
    if id == 0:
        raise HTTPException(status_code=307, detail="Temporary Redirect", headers={"Location": "/api/v1/restaurants"})
    
    query_params = {
        "orderBy": orderBy,
        "offset": offset,
        "limit": limit,
        "q": q,
    }

    if user:
        query_params["auth_user_id"] = user.userId
    total, restaurants_list = crud_map.get_restaurants(db=db, map_id=id, query_params=query_params)
    if reverse:
        restaurants_list = restaurants_list[::-1]
    return PaginatedRestaurantResponse(total=total, restaurants=restaurants_list, limit=limit, offset=offset)

# --- Modify_Map ---
@router.put("/{id}", response_model=PutResponse)
async def modify_map(
    map_data: MapUpdate, 
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db),
):
    update_dict = {
        key: value for key, value in map_data.model_dump().items() 
        if value is not None and key != "id"
    }
    logger.info(f"update_dict: {update_dict}")
    update_result = crud_map.update_map(db, id, update_dict, user.userId)

    if update_result:
        return {
            "success": True,
            "message": f"Map data {id} updated successfully",
        }
    else:
        raise HTTPException(status_code=500, detail=f"Server Error")

# --- Delete_Map ---
@router.delete("/{id}", response_model=PostResponse)
async def delete_map(id: int = Path(...), user: UserLoginInfo = Depends(get_current_user), db = Depends(get_db)):
    try:
        map_delete = crud_map.delete_map(db,id)
        logger.info(f"{map_delete} deleted successfully")
        return {
            "success": True,
            "message": f"Map number {id} deleted successfully",
        }
    except Exception as e:
        logger.error(f"Error in delete_map: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error - Failed to delete map")

@router.post("/{id}/collect", response_model=PostResponse)
async def collect_map(id: int = Path(...), user: UserLoginInfo = Depends(get_current_user)):
    return {
        "success": True,
        "message": f"{user.userId} has collected map number {id}",
    }


@router.delete("/{id}/collect", response_model=PostResponse)
async def uncollect_map(id: int = Path(...), user: UserLoginInfo = Depends(get_current_user)):
    return {
        "success": True,
        "message": f"{user.userId} has uncollected map number {id}",
    }
