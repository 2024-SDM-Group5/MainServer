from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from app.schemas.users import UserLoginInfo
from app.crud.users import get_user_by_email
from app.dependencies.db import get_db
from app.dependencies.redis import get_redis_client
from app.services.redis_query import get_token_cache, set_token_cache
import httpx

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_optional_token(authorization: str = Header(None)):
    try:
        if authorization:
            schema, _, token = authorization.partition(' ')
            if schema and token and schema.lower() == 'bearer':
                return token
    except Exception as e:
        return None
    

async def google_oauth2(token: str = Depends(oauth2_scheme)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": token}
        )
        
        if response.status_code != 200:
            # For testing
            # return {
            #     "name": "Testing",
            #     "email": "test@gmail.com"
            # }
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token_data = response.json()
        return token_data

async def get_current_user(
        token: str = Depends(get_optional_token), 
        db = Depends(get_db), 
        redis = Depends(get_redis_client)
    ) -> UserLoginInfo:
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    
    cached = get_token_cache(redis, token)
    if cached:
        return UserLoginInfo(userId=cached, isNew=False)
    
    user = await google_oauth2(token)
    exist = get_user_by_email(db, user["email"])
    if not exist:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        set_token_cache(redis, token, exist.user_id)
        return UserLoginInfo(userId=exist.user_id, isNew=False)
    

async def get_optional_user(
        token: str = Depends(get_optional_token), 
        db = Depends(get_db), 
        redis = Depends(get_redis_client)
    ):
    try:
        user = await get_current_user(token, db, redis)
        return user
    except HTTPException as e:
        return None
