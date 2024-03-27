from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import UploadFile, File
from typing import List

from app.schemas.bots import BotRequest, BotResponse

router = APIRouter(prefix="/api/v1/bot", tags=["bot"])

@router.post("/question", response_model=BotResponse)
async def question(user_data: BotRequest):
    return {
        
    }

