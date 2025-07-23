from game.llm_client import ask_llm
from game.game_core import pick_random_dish, match_score

def main():
    print("🍳 材料ヒントクイズゲーム（CLI） 🍳")

    # お題の料理と正解材料を取得
    dish, _ = pick_random_dish()
    print(f"🎯 今日のお題は：『{dish}』")
    print("📝 この料理に使われていそうな材料を5つ入力してください：")

    user_ings = [input(f"{i+1}. ") for i in range(5)]

    print("\n🤖 LLMが料理を推測中...")
    guess = ask_llm(user_ings)
    print(f"🔎 LLMの予想: {guess}")

    if match_score(guess, dish) > 0.8:
        print("🎉 正解！お見事です！")
    else:
        print(f"❌ 不正解。正解は「{dish}」でした。")

if __name__ == "__main__":
    main()
