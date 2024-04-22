from pydantic import BaseModel, Field 

class UserLogin(BaseModel):
    idToken: str = Field(..., description="Token received from Google OAuth2")

class UserLoginInfo(BaseModel):
    userId: int
    isNew: bool

class UserUpdate(BaseModel):
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
    postCount: int
    isFollowing: bool = Field(..., description="Flag indicating if the user is currently being followed by the authenticated user")

UserDisplays_Ex = [
    {
        "id": 1,
        "displayName": "John Doe",
        "avatarUrl": "https://picsum.photos/200",
        "following": 10,
        "followed": 20,
        "mapId": 123,
        "postCount": 50,
        "isFollowing": False
    },
    {
        "id": 2,
        "displayName": "xxx",
        "avatarUrl": "https://picsum.photos/200",
        "following": 11,
        "followed": 24,
        "mapId": 125,
        "postCount": 50,
        "isFollowing": True
    },
]

class UserFollow(BaseModel):
    userId: int = Field(..., description="ID of the user who is following")
    followId: int = Field(..., description="ID of the user being followed")

class UserUnfollow(BaseModel):
    userId: int = Field(..., description="ID of the user who is following")
    unfollowId: int = Field(..., description="ID of the user being unfollowed")
