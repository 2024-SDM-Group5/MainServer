from fastapi import APIRouter, Path, Depends, HTTPException, Query
from app.schemas.restaurants import Restaurant, PaginatedRestaurantResponse, PostResponse, SimplifiedRestaurant_Ex
from app.services.places_api import get_place_details
from app.schemas.users import UserLoginInfo
from typing import Optional, List
from app.dependencies.auth import get_optional_user, get_current_user
from app.services.places_api import search_nearby_restaurants
import app.crud.restaurants as crud_rest 

router = APIRouter(prefix="/api/v1/restaurants", tags=["restaurants"])

@router.get("", response_model=PaginatedRestaurantResponse)
async def get_restaurants(
    orderBy: str = Query("collectCount", enum=["collectCount", "createTime"]),
    tags: Optional[List[str]] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    reverse: bool = Query(False),
    q: Optional[str] = Query(None),
):
    restaurants = SimplifiedRestaurant_Ex
    total = len(restaurants)
    restaurants = restaurants[offset:offset+limit]
    return PaginatedRestaurantResponse(total=total, restaurants=restaurants, limit=limit, offset=offset)

@router.get("/{place_id}", response_model=Restaurant)
async def get_single_restaurant(place_id: str = Path(...), user: Optional[UserLoginInfo] = Depends(get_optional_user)):
    try:
        restaurant = await get_place_details(place_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if user:
        restaurant["hasCollected"] = True
        restaurant["hasLiked"] = True
    else:
        restaurant["hasDisliked"] = True
    return Restaurant(**restaurant, 
                      viewCount=0, 
                      favCount=0, 
                      collectCount=0, 
                      likeCount=0, 
                      dislikeCount=0,
                      diaries=[])
 
@router.post("/{place_id}/collect", response_model=PostResponse, status_code=201)
async def collect_restaurant(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):  
    try:
        crud_rest.collect_restaurant(user.userId, place_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} collected place {place_id}"
    }

@router.delete("/{place_id}/collect", response_model=PostResponse)
async def uncollect_restaurant(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):
    try:
        crud_rest.uncollect_restaurant(user.userId, place_id)
    except Exception as e:  
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} uncollected place {place_id}"
    }


@router.post("/{place_id}/like", response_model=PostResponse, status_code=201)
async def like_restaurant(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):  
    try:
        crud_rest.like_restaurant(user.userId, place_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} liked restaurant number {place_id}"
    }

@router.delete("/{place_id}/like", response_model=PostResponse)
async def unlike_restaurant(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):  
    try:
        crud_rest.unlike_restaurant(user.userId, place_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} unlike restaurant number {place_id}"
    }

@router.post("/{place_id}/dislike", response_model=PostResponse, status_code=201)
async def dislike_restaurant(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):  
    try:
        crud_rest.dislike_restaurant(user.userId, place_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} disliked restaurant number {place_id}"
    }

@router.delete("/{place_id}/dislike", response_model=PostResponse)
async def undislike_restaurant(
    place_id: str = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):  
    try:
        crud_rest.undislike_restaurant(user.userId, place_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "success": True, 
        "message": f"User {user.userId} undisliked restaurant number {place_id}"
    }


