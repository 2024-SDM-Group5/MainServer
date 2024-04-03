from pydantic import BaseModel, Field, HttpUrl

class Comment(BaseModel):
    userId: int
    date: str
    items: list[str]
    content: str
    rating: int = Field(None, ge=1, le=5)