from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional 

from app.schemas.diaries import (
    DiaryCreate, DiaryUpdate, DiaryDisplay, DiaryResponse)

router = APIRouter(prefix="/api/v1/diaries", tags=["diaries"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper function (replace with your actual authentication logic)
def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    # Replace with your authentication logic
    return 1  

# --- Diaries_Get  ---
@router.get("", response_model=List[DiaryDisplay])
async def get_diaries(
    offset: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=100)
):
    diaries = [
        {
            "id": 1,
            "username": "foodieJane",
            "avatarUrl": "https://myavatar.jpg",
            "photos": ["https://myphotos.com/diarypic1.jpg", "https://myphotos.com/diarypic2.jpg"],
            "content": "Tried this amazing boba place today!",
            "replies": [
                { 
                    "username": "bobaLover",     
                    "avatarUrl": "https://myavatar.jpg",
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
    user_id: int = Depends(get_current_user_id)
):  
    new_diary_id = 1
    return {
        "success": True, 
        "message": f"User {user_id} created diary number {new_diary_id}"
    }

# --- Single_Diary ---
@router.get("/{id}", response_model=DiaryDisplay)
async def get_single_diary(id: int = Path(...)):
    diary = {
        "id": 1,
        "username": "foodieJane",
        "avatarUrl": "https://myavatar.jpg",
        "photos": ["https://myphotos.com/diarypic1.jpg", "https://myphotos.com/diarypic2.jpg"],
        "content": "Tried this amazing boba place today!",
        "replies": [
        { 
            "username": "bobaLover",     
            "avatarUrl": "https://myavatar.jpg",
            "content": "Looks delicious!",
            "createdAt": 1711987663
        }
        ],
        "favCount": 25,
        "createdAt": 1711987662
    }
    return diary

# --- Diary_Update ---
@router.put("/{id}", response_model=DiaryResponse)
async def update_diary(
    diary_data: DiaryUpdate, 
    id: int = Path(...), 
    user_id: int = Depends(get_current_user_id)
):
    return {
        "success": True, 
        "message": f"User {user_id} updated diary number {id}"
    }

# --- Diary_Delete ---
@router.delete("/{id}", response_model=DiaryResponse)
async def delete_diary(
    id: int = Path(...), 
    user_id: int = Depends(get_current_user_id)
):
    return {
        "success": True, 
        "message": f"User {user_id} deleted diary number {id}"
    }
