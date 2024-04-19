from pydantic import BaseModel, Field
from datetime import datetime

class CommentBase(BaseModel):
    userId: int 
    restaurantId: int
    content: str

class RestaurantComment(BaseModel):
    userId: int
    createdAt: int
    content: str

class CommentCreate(CommentBase):
    pass  

class CommentUpdate(CommentBase): 
    pass

class CommentResponse(BaseModel):
    success: bool
    message: str

class NewComment(BaseModel):
    id: int

