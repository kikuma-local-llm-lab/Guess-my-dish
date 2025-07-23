# game_core.py
import json, random
from difflib import SequenceMatcher

with open("data/dishes.json", encoding="utf-8") as f:
    DISHES = json.load(f)

def pick_random_dish():
    return random.choice(list(DISHES.items()))

def match_score(predicted, actual):
    return SequenceMatcher(None, predicted, actual).ratio()
