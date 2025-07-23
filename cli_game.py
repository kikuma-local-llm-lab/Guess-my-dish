from game.llm_client import ask_llm
from game.game_core import pick_random_dish, match_score

print("🍳 材料ヒントクイズゲーム（CLI） 🍳")
dish, ingredients = pick_random_dish()

print("5つの材料を想像して入力してください。")
user_ings = [input(f"{i+1}. ") for i in range(5)]

guess = ask_llm(user_ings)
print(f"\n🤖 LLMの推測: {guess}")

if match_score(guess, dish) > 0.8:
    print("🎉 正解！")
else:
    print(f"❌ 不正解。正解は「{dish}」でした。")
