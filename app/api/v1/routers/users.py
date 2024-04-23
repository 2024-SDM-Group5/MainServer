from fastapi import APIRouter, Depends, Path, Query
from fastapi import UploadFile, File
from typing import Optional, List
from app.schemas.users import UserLogin, UserUpdate, UserPostResult, UserLoginInfo, UserDisplay, UserDisplays_Ex
from app.schemas.diaries import SimplifiedDiary, SimplifiedDiary_Ex
from app.dependencies.auth import get_current_user, get_optional_user, google_oauth2
from app.dependencies.db import get_db
from app.services.cloud_storage import save_file_to_gcs
from app.crud.users import create_user, get_user_by_email


router = APIRouter(prefix="/api/v1/users", tags=["user"])

@router.get("", response_model=List[UserDisplay])
async def get_users_detail(
    orderBy: str = Query("collectCount", enum=["collectCount", "createTime"]),
    tags: Optional[List[str]] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    reverse: bool = Query(False),
    q: Optional[str] = Query(None),
):
    user_list = UserDisplays_Ex

    if q:
        for index, user in enumerate(user_list):
            user_list[index]["displayName"] = q
    return user_list


@router.post("/login", response_model=UserLoginInfo)
async def login(user_data: UserLogin, db = Depends(get_db)):
    new_user = await google_oauth2(user_data.idToken)
    exist_user = get_user_by_email(db, new_user["email"])
    if exist_user:
        return UserLoginInfo(userId=exist_user.user_id, isNew=False)
    db_user = {
        "user_name": new_user["name"],
        "email": new_user["email"]
    }
    user = create_user(db, db_user)
    return UserLoginInfo(userId=user.user_id, isNew=True)

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

@router.post("/{id}/follow", response_model=UserPostResult, status_code=201)
async def follow_user(
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):
    return {
        "success": True,
        "message": f"User with ID {user.userId} is now \
              following user with ID {id}",
    }

@router.delete("/{id}/follow", response_model=UserPostResult)
async def unfollow_user(
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user)
):
    return {
        "success": True,
        "message": f"User with ID {user.userId} has unfollowed user with ID {id}",
    }


@router.get("/me", response_model=UserDisplay)
async def get_my_detail(user: UserLoginInfo = Depends(get_current_user)):
    fetched = UserDisplays_Ex[0]
    fetched["id"] = user.userId
    return fetched


@router.get("/{id}", response_model=UserDisplay)
async def get_user_detail(id: int = Path(...), user: Optional[UserLoginInfo] = Depends(get_optional_user)):
    user_detail = UserDisplays_Ex[0]
    if user:
        user_detail["isFollowing"] = True
    return user_detail


@router.get("/{id}/diaries", response_model=List[SimplifiedDiary])
async def get_user_diaries(id: int = Path(...)):
    diaries = SimplifiedDiary_Ex
    return diaries




