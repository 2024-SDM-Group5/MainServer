from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi import UploadFile, File
from typing import Optional
from app.schemas.users import UserLogin, UserUpdate, UserPostResult, UserLoginInfo, UserFollow, UserUnfollow, UserDisplay  # Import Pydantic models
from app.schemas.diaries import SimpleDiary
from typing import List
from app.dependencies.auth import get_current_user, get_optional_user
from app.services.cloud_storage import save_file_to_gcs

# from app.models import User as UserModel

router = APIRouter(prefix="/api/v1/users", tags=["user"])

@router.post("/login", response_model=UserLoginInfo)
async def login(user_data: UserLogin):
    user = await get_current_user(user_data.idToken)
    return user

@router.put("/{id}", response_model=UserPostResult)
async def update_user(
    user_update: UserUpdate, 
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
):
    return {
        "success": True,
        "message": f"User {id} updated successfully",
    }

@router.post("/avatar")
async def upload_avatar(avatar: UploadFile = File(...)):
    avatar_url = await save_file_to_gcs(avatar)
    return {
        "avatarUrl": avatar_url,
    }

@router.post("/follow", response_model=UserPostResult)
async def follow_user(
    user_follow: UserFollow, 
    user: UserLoginInfo = Depends(get_current_user)
):
    return {
        "success": True,
        "message": f"User with ID {user_follow.userId} is now \
              following user with ID {user_follow.followId}",
    }

@router.post("/unfollow", response_model=UserPostResult)
async def unfollow_user(
    user_unfollow: UserUnfollow, 
    user: UserLoginInfo = Depends(get_current_user)
):
    return {
        "success": True,
        "message": f"User with ID {user_unfollow.userId} has unfollowed user with ID {user_unfollow.followId}",
    }


@router.get("/me", response_model=UserDisplay)
async def get_my_detail(user: UserLoginInfo = Depends(get_current_user)):
    return {
        "id": 1,
        "displayName": "John Doe",
        "avatarUrl": "https://picsum.photos/200",
        "following": 10,
        "followed": 20,
        "mapId": 123,
        "postCount": 50
    }


@router.get("/{id}", response_model=UserDisplay)
async def get_user_detail(id: int = Path(...), user: Optional[UserLoginInfo] = Depends(get_optional_user)):
    user_detail = {
        "id": id,
        "displayName": "John Doe",
        "avatarUrl": "https://picsum.photos/200",
        "following": 10,
        "followed": 20,
        "mapId": 123,
        "postCount": 50,
        "isFollowing": False
    }
    if user:
        user_detail["isFollowing"] = True
    return user_detail


@router.get("/{id}/diaries", response_model=List[SimpleDiary])
async def get_user_diaries(id: int = Path(...)):
    diaries = [
        {"id": 1, "imageUrl": "https://picsum.photos/200"},
        {"id": 2, "imageUrl": "https://picsum.photos/200"},
    ]
    return diaries




