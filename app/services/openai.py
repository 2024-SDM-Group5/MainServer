from app.core.config import Config
import openai

api_key = Config.OPENAI_API_KEY
if not api_key:
    raise ValueError("No OPENAI_API_KEY set for OpenAI API")

client = openai.OpenAI(
    api_key=api_key,
    timeout=60
)

def gpt_query(req: str, restaurants: list) -> (str, bool):
    """
    Query the GPT-3.5 turbo model with the given request.
    """
    if not restaurants:
        response_content = "對不起，附近沒有符合條件的餐廳，試試看其他關鍵字吧！"
        return response_content, True
    prompt = f"用戶需求：{req}\n附近餐廳資訊：{restaurants}，請推薦一家餐廳給用戶。"
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "你是一個美食推薦員，請根據用戶的需求以及附近餐廳的資訊，推薦一家餐廳給用戶。"},
                {"role": "user", "content": prompt}
            ]
        )
        response_content = completion.choices[0].message.content 
        return response_content, False
    except Exception as e:
        return "", True
