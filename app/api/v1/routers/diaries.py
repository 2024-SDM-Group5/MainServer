from fastapi import APIRouter, Depends, Path, Query, HTTPException
from typing import List, Optional 

from app.schemas.diaries import (
    DiaryCreate, DiaryUpdate, DiaryDisplay, DiaryResponse, SimplifiedDiary)
from app.dependencies.auth import get_current_user, get_optional_user
from app.schemas.users import UserLoginInfo
from app.dependencies.db import get_db
import app.crud.diaries as crud_diary 
router = APIRouter(prefix="/api/v1/diaries", tags=["diaries"])


@router.get("", response_model=List[SimplifiedDiary])
async def get_diaries(
    orderBy: str = Query("collectCount", enum=["collectCount", "createTime"]),
    tags: Optional[List[str]] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    q: Optional[str] = Query(None),
    following: Optional[bool] = Query(False),
    user: Optional[UserLoginInfo] = Depends(get_optional_user),
    db = Depends(get_db)
):  
    query_params = {
        "orderBy": orderBy,
        "offset": offset,
        "limit": limit,
        "q": q,
        "following": following 
    }
    if following and not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id = user.userId if user else -1
    count, diaries = crud_diary.get_diaries(db, user_id, query_params)
    return diaries


# --- Diary_Create ---
@router.post("", response_model=DiaryResponse, status_code=201)
async def create_diary(
    diary_data: DiaryCreate, 
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):  
    new_diary = crud_diary.create_diary(db, diary_data, user.userId)
    return {
        "success": True, 
        "message": f"User {user.userId} created diary number {new_diary.diary_id}"
    }



# --- Single_Diary ---
@router.get("/{id}", response_model=DiaryDisplay)
async def get_single_diary(
    id: int = Path(...), 
    user: Optional[UserLoginInfo] = Depends(get_optional_user),
    db = Depends(get_db)
):
    userId = user.userId if user else -1
    diary = crud_diary.get_diary(db, id, userId)
    return diary

# --- Diary_Update ---
@router.put("/{id}", response_model=DiaryResponse)
async def update_diary(
    diary_data: DiaryUpdate, 
    id: int = Path(...), 
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):
    new_diary = crud_diary.update_diary(db, id, user.userId, diary_data)
    if not new_diary:
        raise HTTPException(status_code=500, detail="Server error on diary update")
    return {
        "success": True, 
        "message": f"User {user.userId} updated diary number {id}"
    }

# --- Diary_Delete ---
@router.delete("/{id}", response_model=DiaryResponse)
async def delete_diary(
    id: int = Path(...), 
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):
    crud_diary.delete_diary(db, id, user.userId)
    return {
        "success": True, 
        "message": f"User {user.userId} deleted diary number {id}"
    }

@router.post("/{id}/favorite", response_model=DiaryResponse, status_code=201)
async def favorite_diary(
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):  
    crud_diary.favorite_diary(db, user.userId, id)
    return {
        "success": True, 
        "message": f"User {user.userId} favorited diary number {id}"
    }

@router.delete("/{id}/favorite", response_model=DiaryResponse)
async def unfavorite_diary(
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):  
    crud_diary.unfavorite_diary(db, user.userId, id)
    return {
        "success": True, 
        "message": f"User {user.userId} unfavorited diary number {id}"
    }

@router.post("/{id}/collect", response_model=DiaryResponse, status_code=201)
async def collect_diary(
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):  
    crud_diary.collect_diary(db, user.userId, id)
    return {
        "success": True, 
        "message": f"User {user.userId} collected diary number {id}"
    }

@router.delete("/{id}/collect", response_model=DiaryResponse)
async def uncollect_diary(
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):  
    crud_diary.uncollect_diary(db, user.userId, id)
    return {
        "success": True, 
        "message": f"User {user.userId} uncollected diary number {id}"
    }
