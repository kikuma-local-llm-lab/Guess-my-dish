# game_core.py
import json, random
from difflib import SequenceMatcher

with open("data/dishes.json", encoding="utf-8") as f:
    DISHES = json.load(f)

def pick_random_dish():
    item = random.choice(DISHES)
    return item["dish"], item["ingredients"]


def match_score(predicted, actual):
    return SequenceMatcher(None, predicted, actual).ratio()
