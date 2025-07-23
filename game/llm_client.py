import os, requests
from dotenv import load_dotenv
load_dotenv()

API_URL = "http://localhost:3000/api/chat/completions"
MODEL_NAME = os.getenv("MODEL_NAME", "mistral")
API_KEY = os.getenv("OPENWEBUI_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def ask_llm(ingredients):
    system_prompt = (
    "あなたはプロの料理研究家です。\n"
    "ユーザーが入力する材料リストから、最も該当しそうな日本語の料理名を **一語だけ** 推測してください。\n"
    "以下のルールを守ってください：\n"
    "・出力は料理名のみ（例：カレーライス、ピザ、味噌汁）\n"
    "・曖昧な場合でも、最も一般的で確率の高い料理名を一語で出してください\n"
    "・説明や前置き、余計な語句は出力しないでください\n"
    )
    user_prompt = f"材料: {', '.join(ingredients)}"
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2,
        "stream": False
    }
    res = requests.post(API_URL, headers=HEADERS, json=payload)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"].strip()
