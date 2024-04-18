from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime 
from typing import List

from app.schemas.comments import CommentCreate, CommentUpdate, CommentResponse
from app.dependencies.auth import get_current_user
from app.schemas.users import UserLoginInfo

router = APIRouter(prefix="/api/v1/comments", tags=["comments"])


# --- Comment_Create ---
@router.post("", response_model=CommentResponse, status_code=201)
async def create_comment(
    comment_data: CommentCreate, 
    user: UserLoginInfo = Depends(get_current_user)
):
    comment_data.date = datetime.now()
    new_comment_id = 1
    return {
        "success": True,
        "message": f"User {user.userId} created map number {new_comment_id}",
    }


# --- Comment_Edit ---
@router.put("/{id}", response_model=CommentResponse)
async def edit_comment(
    comment_data: CommentUpdate,
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):
    return {
        "success": True,
        "message": f"User {user.userId} editted comment number {id}",
    }

# --- Comment_Delete ---
@router.delete("/{id}", response_model=CommentResponse)
async def delete_comment(
    id: int = Path(...), 
    user: UserLoginInfo = Depends(get_current_user)
):
    return {
        "success": True,
        "message": f"User {user.userId} deleted comment {id}",
    }

