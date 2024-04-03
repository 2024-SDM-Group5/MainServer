from pydantic import BaseModel, Field
from datetime import datetime

class CommentBase(BaseModel):
    userId: int 
    restaurantId: int
    content: str
    date: datetime 
    items: list[str] = Field(default=[])
    rating: int = Field(None, ge=1, le=5)

class RestaurantComment(BaseModel):
    userId: int
    date: str
    items: list[str]
    content: str
    rating: int = Field(None, ge=1, le=5)

class CommentCreate(CommentBase):
    pass  

class CommentUpdate(CommentBase): 
    pass

class CommentResponse(BaseModel):
    success: bool
    message: str

