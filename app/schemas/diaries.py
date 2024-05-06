from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class Reply(BaseModel):
    id: int
    authorId: int
    username: str
    avatarUrl: str = Field(None)
    content: str
    createdAt: datetime

class DiaryDisplay(BaseModel):
    id: int
    username: str
    userId: int
    avatarUrl: str = Field(None)
    restaurantId: str
    restaurantName: str
    photos: list[HttpUrl]
    content: str
    replies: list[Reply] = [] 
    items: list[str] = []
    favCount: int = Field(..., ge=0) 
    collectCount: int = Field(..., ge=0)
    createdAt: datetime
    hasFavorited: bool = Field(False, description="Flag indicating if the user is currently being favorited by the authenticated user")
    hasCollected: bool = Field(False, description="Flag indicating if the user has collected this diary")

DiaryDisplay_Ex = {
    "id": 1,
    "username": "foodieJane",
    "userId": 1, 
    "restaurantId": "ChIJrUiM4v6pQjQRF5fxVizXryo",
    "restaurantName": "JJ Poke",
    "avatarUrl": "https://picsum.photos/200",
    "photos": ["https://picsum.photos/200", "https://picsum.photos/200"],
    "content": "Tried this amazing boba place today!",
    "items": ["boba", "milk tea", "taro milk tea"],
    "replies": [
        {
            "id": 1,
            "authorId": 1,
            "username": "bobaLover",     
            "avatarUrl": "https://picsum.photos/200",
            "content": "Looks delicious!",
            "createdAt": 1711987663
        }
    ],
    "favCount": 25,
    "collectCount": 25,
    "createdAt": 1711987662,
    "hasFavorited": False,
    "hasCollected": False
}

class DiaryCreate(BaseModel):
    restaurantId: str
    photos: list[str]
    content: str
    items: list[str] = Field(None)

class DiaryUpdate(BaseModel):
    photos: list[str] = Field(None)
    content: str = Field(None)
    items: list[str] = Field(None)

class DiaryResponse(BaseModel):
    success: bool
    message: str

class SimplifiedDiary(BaseModel):
    id: int
    imageUrl: HttpUrl
    restaurantName: str

SimplifiedDiary_Ex = [
    {
        "id": 1,
        "imageUrl": "https://picsum.photos/200",
        "restaurantName": "JJ Poke"
    },
    {
        "id": 2,
        "imageUrl": "https://picsum.photos/200",
        "restaurantName": "Boba Guys"
    },
    {
        "id": 3,
        "imageUrl": "https://picsum.photos/200",
        "restaurantName": "Happy Lemon"
    }
]