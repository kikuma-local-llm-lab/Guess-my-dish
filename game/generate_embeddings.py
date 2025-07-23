import json
import torch
from sentence_transformers import SentenceTransformer

# データ読み込み
with open("data/dishes.json", encoding="utf-8") as f:
    dishes = json.load(f)

# モデルの読み込み
model = SentenceTransformer("cl-tohoku/bert-base-japanese-v2")

# 全料理名のベクトル化
names = [item["dish"] for item in dishes]
embeddings = model.encode(names, convert_to_tensor=True)

# 保存
torch.save({"names": names, "embeddings": embeddings}, "data/dish_embeddings.pt")
print("✅ Embeddings 保存完了")
