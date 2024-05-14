from fastapi import APIRouter, Path, Depends, HTTPException, Query
from app.schemas.restaurants import Restaurant, PaginatedRestaurantResponse, PostResponse
from app.services.places_api import get_place_details
from app.schemas.users import UserLoginInfo
from typing import Optional, List
from app.dependencies.auth import get_optional_user, get_current_user
from app.services.places_api import search_nearby_restaurants
from app.schemas.restaurants import CreateRestaurant
from app.crud.restaurants import bulk_insert, create_update_restaurant, get_restaurant
from app.dependencies.db import get_db
from app.dependencies.redis import get_redis_client
from app.services.redis_query import need_query_position, need_query_place
import app.crud.restaurants as crud_rest 

router = APIRouter(prefix="/api/v1/restaurants", tags=["restaurants"])

@router.get("", response_model=PaginatedRestaurantResponse)
def get_restaurants(
    orderBy: str = Query("collectCount", enum=["collectCount", "createTime"]),
    tags: Optional[List[str]] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    reverse: bool = Query(False),
    q: Optional[str] = Query(None),
    lat: float = Query(25.013686),
    lng: float = Query(121.540535),
    distance: int = Query(1000),
    sw: Optional[str] = Query(None),
    ne: Optional[str] = Query(None),
    user: Optional[UserLoginInfo] = Depends(get_optional_user),
    db = Depends(get_db),
    redis = Depends(get_redis_client)
):
    if sw and ne:
        sw = sw.split(",")
        ne = ne.split(",")
        sw_lat = float(sw[0])
        sw_lng = float(sw[1])
        ne_lat = float(ne[0])
        ne_lng = float(ne[1])
        lat = (sw_lat + ne_lat) / 2
        lng = (sw_lng + ne_lng) / 2
        
    if need_query_position(redis, lat, lng):
        nearby_restaurants = search_nearby_restaurants(q, lat, lng)
        db_restaurants = [CreateRestaurant(**restaurant) for restaurant in nearby_restaurants]
        bulk_insert(db, db_restaurants)

    query_params = {
        "orderBy": orderBy,
        "offset": offset,
        "limit": limit,
        "q": q,
    }

    if sw and ne:
        query_params["sw_lat"] = sw_lat
        query_params["sw_lng"] = sw_lng
        query_params["ne_lat"] = ne_lat
        query_params["ne_lng"] = ne_lng

    if user:
        query_params["auth_user_id"] = user.userId
    
    total, restaurants_list = crud_rest.query_restaurants(db, query_params)
    if reverse:
        restaurants_list = restaurants_list[::-1]
    return PaginatedRestaurantResponse(total=total, restaurants=restaurants_list, limit=limit, offset=offset)

@router.get("/test")
def get_restaurants(
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db),
    redis = Depends(get_redis_client)
):
    return {
        "msg": "hi"
    }

@router.get("/{place_id}", response_model=Restaurant)
async def get_single_restaurant(
    place_id: str = Path(...), 
    user: Optional[UserLoginInfo] = Depends(get_optional_user),
    db = Depends(get_db),
    redis = Depends(get_redis_client)
):
    try:
        restaurant = await get_place_details(place_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if need_query_place(redis, place_id):
        create_update_restaurant(db, restaurant)
    restaurant = get_restaurant(db, place_id, user.userId if user else -1)
    return restaurant
 
@router.post("/{place_id}/collect", response_model=PostResponse, status_code=201)
async def collect_restaurant(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):  
    try:
        crud_rest.collect_restaurant(db, user.userId, place_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} collected place {place_id}"
    }

@router.delete("/{place_id}/collect", response_model=PostResponse)
async def uncollect_restaurant(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):
    try:
        crud_rest.uncollect_restaurant(db, user.userId, place_id)
    except Exception as e:  
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} uncollected place {place_id}"
    }


@router.post("/{place_id}/like", response_model=PostResponse, status_code=201)
async def like_restaurant(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):  
    try:
        crud_rest.like_restaurant(db, user.userId, place_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} liked restaurant number {place_id}"
    }

@router.delete("/{place_id}/like", response_model=PostResponse)
async def unlike_restaurant(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):  
    try:
        crud_rest.unlike_restaurant(db, user.userId, place_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} unlike restaurant number {place_id}"
    }

@router.post("/{place_id}/dislike", response_model=PostResponse, status_code=201)
async def dislike_restaurant(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):  
    try:
        crud_rest.dislike_restaurant(db, user.userId, place_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} disliked restaurant number {place_id}"
    }

@router.delete("/{place_id}/dislike", response_model=PostResponse)
async def undislike_restaurant(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):  
    try:
        crud_rest.undislike_restaurant(db, user.userId, place_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} undisliked restaurant number {place_id}"
    }

