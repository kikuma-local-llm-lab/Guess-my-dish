import os
import re
import requests
from dotenv import load_dotenv
load_dotenv()

API_URL = "http://localhost:3000/api/chat/completions"
MODEL_NAME = os.getenv("MODEL_NAME", "gemma3")
API_KEY = os.getenv("OPENWEBUI_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 材料の表記ゆれを正規化する辞書
NORMALIZE = {
    "玉ねぎ": "たまねぎ",
    "豚バラ": "ぶたにく",
    "牛バラ": "ぎゅうにく",
    "ミンチ": "ひきにく",
    "ひき肉": "ひきにく",
    "卵": "たまご",
    "たまご": "たまご",
    "ご飯": "ごはん",
    "キャベツ": "きゃべつ",
    # 必要に応じて追加
}

def normalize_ingredients(ingredients):
    return [NORMALIZE.get(i.strip(), i.strip()) for i in ingredients]

def extract_dish_name(text):
    """
    出力から日本語料理名（2文字以上のひらがな/カタカナ/漢字）を抽出
    """
    match = re.search(r'[\u3040-\u30FF\u4E00-\u9FFF]{2,}', text)
    return match.group() if match else text.strip()

def ask_llm(ingredients):
    ingredients = normalize_ingredients(ingredients)

    # few-shotでLLMに答え方の文脈を示す
    messages = [
        {"role": "system", "content": (
            "あなたはプロの料理研究家です。\n"
            "ユーザーが入力する材料リストから、最も該当しそうな日本語の料理名を **一語だけ** 推測してください。\n"
            "・出力は料理名のみ（例：カレーライス、ピザ、味噌汁）\n"
            "・説明や前置き、余計な語句は出力しない\n"
            "・曖昧でも最も一般的な料理名を推測してください"
        )},
        {"role": "user", "content": "材料: じゃがいも, にんじん, カレールー, たまねぎ, 豚肉"},
        {"role": "assistant", "content": "カレーライス"},
        {"role": "user", "content": "材料: 小麦粉, チーズ, トマトソース, ピーマン, サラミ"},
        {"role": "assistant", "content": "ピザ"},
        {"role": "user", "content": f"材料: {', '.join(ingredients)}"}
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.2,
        "stream": False
    }

    res = requests.post(API_URL, headers=HEADERS, json=payload)
    res.raise_for_status()

    raw_output = res.json()["choices"][0]["message"]["content"]
    return extract_dish_name(raw_output)
