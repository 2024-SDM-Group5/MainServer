from pydantic import BaseModel, Field 

class BotRequest(BaseModel):
    req: str = Field(..., description="Request question from user")

class BotResponse(BaseModel):
    res: str = Field(..., description="Response from bot to user")
