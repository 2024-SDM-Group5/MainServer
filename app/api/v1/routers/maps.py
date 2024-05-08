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
)
from app.dependencies.auth import get_current_user, get_optional_user
from app.schemas.users import UserLoginInfo
from app.schemas.restaurants import PaginatedRestaurantResponse
from app.dependencies.db import get_db
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
    user: Optional[UserLoginInfo] = Depends(get_optional_user),
    db = Depends(get_db)
):
    query_params = {
        "orderBy": orderBy,
        "offset": offset,
        "limit": limit,
        "q": q,
        "auth_user_id": user.userId if user else -1
    }
    map_list = crud_map.get_maps(db, query_params)
    if reverse:
        map_list = map_list[::-1]
    return PaginatedMapResponse(total=len(map_list), maps=map_list[offset:offset+limit], limit=limit, offset=offset)

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
    map = crud_map.get_map(db, id, user.userId if user else -1)
    if not map:
        raise HTTPException(status_code=404, detail="Map not found")
    return map

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
        "q": q,
    }

    if user:
        query_params["auth_user_id"] = user.userId
    total, restaurants_list = crud_map.get_restaurants(db=db, map_id=id, query_params=query_params)
    if reverse:
        restaurants_list = restaurants_list[::-1]
    restaurants_list = restaurants_list[offset:offset+limit]
    return PaginatedRestaurantResponse(total=total, restaurants=restaurants_list, limit=limit, offset=offset)

# --- Modify_Map ---
@router.put("/{id}", response_model=PutResponse)
async def modify_map(
    map_data: MapUpdate, 
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db),
):
    update_dict = {}
    if map_data.description is not None:
        update_dict["description"] = map_data.description
    if map_data.name is not None:
        update_dict["map_name"] = map_data.name
    if map_data.iconUrl is not None:
        update_dict["icon_url"] = map_data.iconUrl
    if map_data.tags:
        update_dict["tags"] = map_data.tags
    if map_data.restaurants:
        update_dict["rest_ids"] = map_data.restaurants

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
async def collect_map(
    id: int = Path(...), 
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):
    try:
        crud_map.collect_map(db, user.userId, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} collected map {id}"
    }


@router.delete("/{id}/collect", response_model=PostResponse)
async def uncollect_map(
    id: int = Path(...), 
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):
    try:
        crud_map.uncollect_map(db, user.userId, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True,
        "message": f"{user.userId} has uncollected map number {id}",
    }
