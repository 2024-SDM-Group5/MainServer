from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional 

from app.schemas.maps import MapCreate, MapUpdate, SimplifiedMap, CompleteMap, PostResponse, PutResponse, PaginatedMapResponse
from app.dependencies.auth import get_current_user, get_optional_user
from app.schemas.users import UserLoginInfo
from app.schemas.restaurants import PaginatedRestaurantResponse
router = APIRouter(prefix="/api/v1/maps", tags=["maps"])

@router.get("", response_model=PaginatedMapResponse)
async def get_maps(
    orderBy: str = Query("favCount", enum=["favCount", "createTime"]),
    tags: Optional[List[str]] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    reverse: bool = Query(False),
    q: Optional[str] = Query(None),
):
    print(tags, offset, limit, reverse)
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
    total = len(maps)
    maps = maps[offset:offset+limit]
    return {
        "total": total,
        "maps": maps,
        "limit": limit,
        "offset": offset
    }


# --- Create_Map ---
@router.post("", response_model=PostResponse, status_code=201)
async def create_map(map_data: MapCreate, user: UserLoginInfo = Depends(get_current_user)):
    new_map_id = 1
    return {
        "success": True,
        "message": f"User {user.userId} created map number {new_map_id}",
    }

# --- Single_Map ---
@router.get("/{id}", response_model=CompleteMap)
async def get_single_map(
    id: int = Path(...), 
    user: Optional[UserLoginInfo] = Depends(get_optional_user)
):
    map_data = {
        "id": 11,
        "name": "台北飲料地圖",
        "iconUrl": "https://picsum.photos/200",
        "center": {
            "lat": 25.0329694,
            "lng": 121.5654118
        },
        "author": "enip",
        "viewCount": 441,
        "favCount": 189,
        "hasCollected": False,
    }
    if user:
        map_data["hasCollected"] = True
    return map_data

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
):
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
    total = len(restaurants)
    restaurants = restaurants[offset:offset+limit]
    return PaginatedRestaurantResponse(total=total, restaurants=restaurants, limit=limit, offset=offset)

# --- Modify_Map ---
@router.put("/{id}", response_model=PutResponse)
async def modify_map(
    map_data: MapUpdate, 
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):
    return {
        "success": True,
        "message": f"Map data {id} updated successfully",
    }


# --- Delete_Map ---
@router.delete("/{id}", response_model=PostResponse)
async def delete_map(id: int = Path(...), user: UserLoginInfo = Depends(get_current_user)):
    return {
        "success": True,
        "message": f"Map number {id} deleted successfully",
    }

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