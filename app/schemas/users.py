from pydantic import BaseModel, Field 

class UserLogin(BaseModel):
    idToken: str = Field(..., description="Token received from Google OAuth2")

class UserLoginInfo(BaseModel):
    id: int
    isNew: bool

class UserUpdate(BaseModel):
    id: int = Field(..., description="User's ID")
    displayName: str | None = Field(None, description="User's display name")
    avatarUrl: str | None = Field(None, description="URL of user's avatar")

class UserPostResult(BaseModel):
    success: bool
    message: str

class UserDisplay(BaseModel):
    id: int
    displayName: str
    avatarUrl: str | None
    following: int
    followed: int
    mapId: int | None = Field(None, description="ID of map created by user – if applicable")

class UserFollow(BaseModel):
    userId: int = Field(..., description="ID of the user who is following")
    followId: int = Field(..., description="ID of the user being followed")

class UserUnfollow(BaseModel):
    userId: int = Field(..., description="ID of the user who is following")
    unfollowId: int = Field(..., description="ID of the user being unfollowed")
