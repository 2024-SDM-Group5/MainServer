from fastapi import APIRouter, HTTPException
from typing import List
import openai
from app.schemas.bots import BotRequest, BotResponse

client = openai.OpenAI(
    base_url="http://llama-server-service:5278/v1",
    api_key="sk-no-key-required",
    timeout=60
)

router = APIRouter(prefix="/api/v1/bots", tags=["bots"])

@router.post("/question", response_model=BotResponse)
async def question(user_data: BotRequest):
    try:
        completion = client.chat.completions.create(
            model="Taiwan-Llama",
            messages=[
                {"role": "system", "content": "你是一個實用的問答助手，請根據使用者問題來回答"},
                {"role": "user", "content": user_data.req}
            ]
        )
        response_content = completion.choices[0].message.content 
        if completion.choices:
            return BotResponse(res=response_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
