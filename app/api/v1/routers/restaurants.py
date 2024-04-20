from fastapi import APIRouter, Path, Depends, HTTPException, Query
from app.schemas.restaurants import Restaurant, PaginatedRestaurantResponse, PostResponse
from app.services.places_api import get_place_details
from app.schemas.users import UserLoginInfo
from typing import Optional, List
from app.dependencies.auth import get_optional_user, get_current_user

router = APIRouter(prefix="/api/v1/restaurants", tags=["restaurants"])

@router.get("", response_model=PaginatedRestaurantResponse)
async def get_restaurants(
    orderBy: str = Query("favCount", enum=["favCount", "createTime"]),
    tags: Optional[List[str]] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    reverse: bool = Query(False),
    q: Optional[str] = Query(None),
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

@router.get("/{place_id}", response_model=Restaurant)
async def get_single_restaurant(place_id: str = Path(...), user: Optional[UserLoginInfo] = Depends(get_optional_user)):
    try:
        restaurant = await get_place_details(place_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # restaurant_data = {
    #     "name": "Restaurant 1",
    #     "location": {
    #         "lat": 25.0329694,
    #         "lng": 121.5654177
    #     },
    #     "rating": 4.5,
    #     "placeId": "asdjglsakjgka",
    #     "viewCount": 400,
    #     "favCount": 100,
    # }
    print(restaurant)
    if user:
        restaurant["hasCollected"] = True
    return restaurant

@router.post("/{place_id}/collect", response_model=PostResponse, status_code=201)
async def collect_diary(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):  
    return {
        "success": True, 
        "message": f"User {user.userId} collected place {place_id}"
    }

@router.delete("/{place_id}/collect", response_model=PostResponse)
async def uncollect_diary(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):  
    return {
        "success": True, 
        "message": f"User {user.userId} uncollected place {place_id}"
    }



