from fastapi import APIRouter, Depends, Path, Query, HTTPException
from fastapi import UploadFile, File
from typing import Optional, List
from app.schemas.users import UserLogin, UserUpdate, UserPostResult, UserLoginInfo, UserDisplay
from app.schemas.diaries import SimplifiedDiary, SimplifiedDiary_Ex
from app.dependencies.auth import get_current_user, get_optional_user, google_oauth2
from app.dependencies.db import get_db
from app.services.cloud_storage import save_file_to_gcs
import app.crud.users as crud_user
import app.crud.follow as crud_follow

router = APIRouter(prefix="/api/v1/users", tags=["user"])

@router.get("", response_model=List[UserDisplay])
async def get_users_detail(
    orderBy: str = Query("createTime", enum=["following", "createTime"]),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    reverse: bool = Query(False),
    q: Optional[str] = Query(None),
    user: Optional[UserLoginInfo] = Depends(get_optional_user),
    db = Depends(get_db)
):
    query_params = {
        "orderBy": orderBy,
        "offset": offset,
        "limit": limit,
        "q": q,
        "auth_user_id": user.userId if user else -1 
    }
    user_list = crud_user.get_users(db, query_params)
    if reverse:
        user_list = user_list[::-1]
    return user_list


@router.post("/login", response_model=UserLoginInfo)
async def login(user_data: UserLogin, db = Depends(get_db)):
    new_user = await google_oauth2(user_data.idToken)
    exist_user = crud_user.get_user_by_email(db, new_user["email"])
    if exist_user:
        return UserLoginInfo(userId=exist_user.user_id, isNew=False)
    db_user = {
        "user_name": new_user["name"],
        "email": new_user["email"]
    }
    created_user = crud_user.create_user(db, db_user)
    return UserLoginInfo(userId=created_user.user_id, isNew=True)

@router.put("/{id}", response_model=UserPostResult)
async def update_user(
    user_update: UserUpdate, 
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):
    if not user or user.userId != id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db_user = {}
    if user_update.displayName is not None:
        db_user["user_name"] = user_update.displayName
    if user_update.avatarUrl is not None:
        db_user["avatar_url"] = user_update.avatarUrl
    modified_user = crud_user.update_user(db, id, db_user)

    if modified_user is None:
        return {
            "success": False,
            "message": f"User {id} not found",
        }
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
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):  
    if id == user.userId:
        raise HTTPException(status_code=403, detail="You cannot follow yourself")
    follow = crud_follow.create_follow(db, user.userId, id)
    if not follow:
        return HTTPException(status_code=500, detail="Server Error")
    return {
        "success": True,
        "message": f"User with ID {user.userId} is now following user with ID {id}",
    }

@router.delete("/{id}/follow", response_model=UserPostResult)
async def unfollow_user(
    id: int = Path(...),
    user: UserLoginInfo = Depends(get_current_user),
    db = Depends(get_db)
):  
    if id == user.userId:
        raise HTTPException(status_code=403, detail="You cannot unfollow yourself")
    follow = crud_follow.delete_follow(db, user.userId, id)
    if not follow:
        return HTTPException(status_code=500, detail="Server Error")
    return {
        "success": True,
        "message": f"User with ID {user.userId} has unfollowed user with ID {id}",
    }


@router.get("/me", response_model=UserDisplay)
async def get_my_detail(user: UserLoginInfo = Depends(get_current_user), db = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    fetched = crud_user.get_user(db, user.userId, -1)
    if not fetched:
        raise HTTPException(status_code=404, detail="User not found")
    return fetched


@router.get("/{id}", response_model=UserDisplay)
async def get_user_detail(id: int = Path(...), user: Optional[UserLoginInfo] = Depends(get_optional_user), db = Depends(get_db)):
    auth_user_id = -1
    if user:
        auth_user_id = user.userId
    fetched = crud_user.get_user(db, id, auth_user_id)
    if not fetched:
        raise HTTPException(status_code=404, detail="User not found")
    return fetched


@router.get("/{id}/diaries", response_model=List[SimplifiedDiary])
async def get_user_diaries(
    id: int = Path(...),
    db = Depends(get_db)
):
    diaries = crud_user.get_user_diaries(db, user_id=id)
    return diaries




