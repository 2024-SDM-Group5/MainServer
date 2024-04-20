from fastapi import APIRouter, Depends, Path, Query
from typing import List, Optional 

from app.schemas.diaries import (
    DiaryCreate, DiaryUpdate, DiaryDisplay, DiaryResponse)
from app.dependencies.auth import get_current_user, get_optional_user
from app.schemas.users import UserLoginInfo
router = APIRouter(prefix="/api/v1/diaries", tags=["diaries"])


@router.get("", response_model=List[DiaryDisplay])
async def get_diaries(
    offset: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=100)
):
    diaries = [
        {
            "id": 1,
            "username": "foodieJane",
            "restaurantId": "ChIJrUiM4v6pQjQRF5fxVizXryo",
            "restaurantName": "JJ Poke",
            "avatarUrl": "https://picsum.photos/200",
            "photos": ["https://picsum.photos/200", "https://picsum.photos/200"],
            "content": "Tried this amazing boba place today!",
            "replies": [
                { 
                    "id": 1,
                    "authorId": 1,
                    "username": "bobaLover",     
                    "avatarUrl": "https://picsum.photos/200",
                    "content": "Looks delicious!",
                    "createdAt": 1711987663
                }
            ],
            "favCount": 25,
            "createdAt": 1711987662
        }
    ]

    return diaries


# --- Diary_Create ---
@router.post("", response_model=DiaryResponse, status_code=201)
async def create_diary(
    diary_data: DiaryCreate, 
    user: UserLoginInfo = Depends(get_current_user)
):  
    new_diary_id = 1
    return {
        "success": True, 
        "message": f"User {user.userId} created diary number {new_diary_id}"
    }



# --- Single_Diary ---
@router.get("/{id}", response_model=DiaryDisplay)
async def get_single_diary(id: int = Path(...), user: Optional[UserLoginInfo] = Depends(get_optional_user)):
    diary = {
        "id": 1,
        "username": "foodieJane",
        "restaurantId": "ChIJrUiM4v6pQjQRF5fxVizXryo",
        "restaurantName": "JJ Poke",
        "avatarUrl": "https://picsum.photos/200",
        "photos": ["https://picsum.photos/200", "https://picsum.photos/200"],
        "content": "Tried this amazing boba place today!",
        "replies": [
            {
                "id": 1,
                "authorId": 1,
                "username": "bobaLover",     
                "avatarUrl": "https://picsum.photos/200",
                "content": "Looks delicious!",
                "createdAt": 1711987663
            }
        ],
        "favCount": 25,
        "createdAt": 1711987662,
        "hasFavorited": False,
        "hasCollected": False
    }
    if user:
        diary["hasFavorited"] = True
    return diary

# --- Diary_Update ---
@router.put("/{id}", response_model=DiaryResponse)
async def update_diary(
    diary_data: DiaryUpdate, 
    id: int = Path(...), 
    user: UserLoginInfo = Depends(get_current_user)
):
    return {
        "success": True, 
        "message": f"User {user.userId} updated diary number {id}"
    }

# --- Diary_Delete ---
@router.delete("/{id}", response_model=DiaryResponse)
async def delete_diary(
    id: int = Path(...), 
    user: UserLoginInfo = Depends(get_current_user)
):
    return {
        "success": True, 
        "message": f"User {user.userId} deleted diary number {id}"
    }

@router.post("/{id}/favorite", response_model=DiaryResponse, status_code=201)
async def favorite_diary(
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):  
    return {
        "success": True, 
        "message": f"User {user.userId} favorited diary number {id}"
    }

@router.delete("/{id}/favorite", response_model=DiaryResponse)
async def unfavorite_diary(
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):  
    return {
        "success": True, 
        "message": f"User {user.userId} unfavorited diary number {id}"
    }

@router.post("/{id}/collect", response_model=DiaryResponse, status_code=201)
async def collect_diary(
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):  
    return {
        "success": True, 
        "message": f"User {user.userId} collected diary number {id}"
    }

@router.delete("/{id}/collect", response_model=DiaryResponse)
async def uncollect_diary(
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):  
    return {
        "success": True, 
        "message": f"User {user.userId} uncollected diary number {id}"
    }



