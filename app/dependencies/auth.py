from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from app.schemas.users import UserLoginInfo
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


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserLoginInfo:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": token}
        )
        
        if response.status_code != 200:
            # For testing
            return UserLoginInfo(userId=-1, isNew=False)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token_data = response.json()
        email = token_data.get("email")
        ## TODO: Interact with database to fetch user info
        # user = fetch_or_create_user(email)
        # return user
        return UserLoginInfo(userId=1, isNew=False)

async def get_optional_user(token: str = Depends(get_optional_token)):
    try:
        return await get_current_user(token)
    except HTTPException as e:
        return None
