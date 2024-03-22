from pydantic import BaseModel, Field 

class SimpleDiary(BaseModel):
    id: int
    imageUrl: str
