from pydantic import BaseModel, Field 

class Position(BaseModel):
    lat: float = Field(..., description="Latitude of the user")
    lng: float = Field(..., description="Longitude of the user")
class BotRequest(BaseModel):
    req: str = Field(..., description="Request question from user")
    position: Position = Field(..., description="Position of the user")
class BotResponse(BaseModel):
    res: str = Field(..., description="Response from bot to user")
