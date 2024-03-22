from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import UploadFile, File
from app.schemas.users import UserLogin, UserUpdate, UserPostResult, UserLoginInfo, UserFollow, UserUnfollow, UserDisplay  # Import Pydantic models
from app.schemas.diaries import SimpleDiary
from typing import List

# from app.models import User as UserModel

router = APIRouter(prefix="/api/v1/users", tags=["user"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login", response_model=UserLoginInfo)
async def login(user_data: UserLogin):
    return {
        "id": 1,
        "isNew": False
    }

@router.put("/update", response_model=UserPostResult)
async def update_user(
    user_update: UserUpdate, 
    token: str = Depends(oauth2_scheme),
):
    return {
        "success": True,
        "message": "User data updated successfully",
    }

@router.post("/avatar")
async def upload_avatar(avatar: UploadFile = File(...)):
    return {
        "avatarUrl": "https://testing.img",
    }

@router.post("/follow", response_model=UserPostResult)
async def follow_user(
    user_follow: UserFollow, 
    token: str = Depends(oauth2_scheme),
):
    return {
        "success": True,
        "message": f"User with ID {user_follow.userId} is now \
              following user with ID {user_follow.followId}",
    }

@router.post("/unfollow", response_model=UserPostResult)
async def unfollow_user(
    user_unfollow: UserUnfollow, 
    token: str = Depends(oauth2_scheme),
):
    return {
        "success": True,
        "message": f"User with ID {user_unfollow.userId} has unfollowed user with ID {user_unfollow.followId}",
    }


@router.get("/me", response_model=UserDisplay)
async def get_my_detail(token: str = Depends(oauth2_scheme)):
    return {
        "id": 1,
        "displayName": "John Doe",
        "avatarUrl": "https://example.com/avatar.jpg",
        "following": 10,
        "followed": 20,
        "mapId": 123,
        "postCount": 50
    }

@router.get("/{id}", response_model=UserDisplay)
async def get_user_detail(id: int):
    return {
        "id": 1,
        "displayName": "John Doe",
        "avatarUrl": "https://example.com/avatar.jpg",
        "following": 10,
        "followed": 20,
        "mapId": 123,
        "postCount": 50
    }


@router.get("/{id}/diaries", response_model=List[SimpleDiary])
async def get_user_diaries(id: int):
    diaries = [
        {"id": 1, "imageUrl": "https://example.com/diary1.jpg"},
        {"id": 2, "imageUrl": "https://example.com/diary2.jpg"},
    ]
    return diaries
