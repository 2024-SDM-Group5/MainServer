from fastapi import APIRouter, Depends, Path

from app.schemas.comments import CommentCreate, CommentUpdate, CommentResponse, NewComment
from app.dependencies.auth import get_current_user
from app.schemas.users import UserLoginInfo

router = APIRouter(prefix="/api/v1/comments", tags=["comments"])

# --- Comment_Create ---
@router.post("", response_model=NewComment, status_code=201)
async def create_comment(
    comment_data: CommentCreate, 
    user: UserLoginInfo = Depends(get_current_user)
):
    new_comment_id = 1
    return {
        "id": new_comment_id,
    }


# --- Comment_Edit ---
@router.put("/{id}", response_model=NewComment)
async def edit_comment(
    comment_data: CommentUpdate,
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):
    return {
        "id": id
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

