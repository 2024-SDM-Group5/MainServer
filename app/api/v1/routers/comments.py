from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime 
from typing import List

from app.schemas.comments import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter(prefix="/api/v1/comments", tags=["comments"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper function (replace with your actual authentication logic)
def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    # Replace with your authentication logic
    return 1  

# --- Comment_Create ---
@router.post("", response_model=CommentResponse, status_code=201)
async def create_comment(
    comment_data: CommentCreate, 
    user_id: int = Depends(get_current_user_id)
):
    comment_data.date = datetime.now()
    new_comment_id = 1
    return {
        "success": True,
        "message": f"User {user_id} created map number {new_comment_id}",
    }


# --- Comment_Edit ---
@router.put("/{id}", response_model=CommentResponse)
async def edit_comment(
    comment_data: CommentUpdate,
    id: int = Path(...),
    user_id: int = Depends(get_current_user_id)
):
    return {
        "success": True,
        "message": f"User {user_id} editted comment number {id}",
    }

# --- Comment_Delete ---
@router.delete("/{id}", response_model=CommentResponse)
async def delete_comment(
    id: int = Path(...), 
    user_id: int = Depends(get_current_user_id)
):
    return {
        "success": True,
        "message": f"User {user_id} deleted comment {id}",
    }

