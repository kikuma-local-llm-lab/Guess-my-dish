import json, random
import torch
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer, util
from rapidfuzz.fuzz import ratio

# --- モデルの読み込み ---
_bert_model = SentenceTransformer("cl-tohoku/bert-base-japanese-v2")
_dish_data = torch.load("data/dish_embeddings.pt")
_dish_names = _dish_data["names"]
_dish_embeddings = _dish_data["embeddings"]

# --- データの読み込み ---
with open("data/dishes.json", encoding="utf-8") as f:
    DISHES = json.load(f)

# --- お題の選択 ---
def pick_random_dish():
    item = random.choice(DISHES)
    return item["dish"], item["ingredients"]

# --- 単純な文字列類似度（difflib） ---
def match_score(predicted, actual):
    return SequenceMatcher(None, predicted, actual).ratio()

# --- RapidFuzzによる文字列類似度 ---
def compute_similarity(llm_answer: str, correct_answer: str) -> float:
    return ratio(llm_answer.strip(), correct_answer.strip()) / 100

# --- BERTベースの意味類似度（Embedding） ---
def compute_bert_similarity(llm_answer: str, correct_answer: str) -> float:
    emb1 = _bert_model.encode(llm_answer.strip(), convert_to_tensor=True)
    emb2 = _bert_model.encode(correct_answer.strip(), convert_to_tensor=True)
    sim = util.cos_sim(emb1, emb2).item()
    return round(sim, 4)

def find_most_similar_dish(llm_guess: str, top_k=3):
    query_emb = _bert_model.encode(llm_guess.strip(), convert_to_tensor=True)
    cos_scores = util.cos_sim(query_emb, _dish_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    results = [
        {"dish": _dish_names[idx], "score": round(cos_scores[idx].item(), 4)}
        for idx in top_results.indices
    ]
    return results