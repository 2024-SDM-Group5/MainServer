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
    system_prompt = f"你是一個美食推薦員，請根據用戶的需求以及附近餐廳的資訊，以繁體中文推薦一家餐廳給用戶，請勿在推薦中包括 placeId。"
    user_prompt = f"用戶需求：{req}\n附近餐廳資訊：{restaurants}。你的推薦："
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        response_content = completion.choices[0].message.content 
        return response_content, False
    except Exception as e:
        return "", True
    
def request_rewriting(req: str):
    """
    Rewrite the given request with the GPT-3.5 turbo model.
    """
    system_prompt = f"你是一個善解人意的助手，擅長判斷一個人想要吃什麼。請從以下使用者需求提取三個以內與食物種類的關鍵字並以,分隔。請只輸出關鍵字"
    user_prompt = f"{req}"
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        response_content = completion.choices[0].message.content 
        print(response_content)
        return response_content, False
    except Exception as e:
        return "", True
