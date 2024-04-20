from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class Reply(BaseModel):
    id: int
    authorId: int
    username: str
    avatarUrl: HttpUrl = Field(None)
    content: str
    createdAt: datetime

class DiaryDisplay(BaseModel):
    username: str
    avatarUrl: HttpUrl = Field(None)
    photos: list[HttpUrl]
    content: str
    replies: list[Reply] = [] 
    favCount: int = Field(0, ge=0) 
    createdAt: datetime
    hasFavorited: bool = Field(..., description="Flag indicating if the user is currently being favorited by the authenticated user")

class DiaryCreate(BaseModel):
    restaurantId: int
    photos: list[HttpUrl]
    content: str

class DiaryUpdate(BaseModel): 
    photos: list[HttpUrl] = Field(None)
    content: str = Field(None)

class DiaryResponse(BaseModel):
    success: bool
    message: str

class SimpleDiary(BaseModel):
    id: int
    imageUrl: HttpUrl
