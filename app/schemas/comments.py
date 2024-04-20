from pydantic import BaseModel, Field
from datetime import datetime

class CommentBase(BaseModel):
    diaryId: int
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

