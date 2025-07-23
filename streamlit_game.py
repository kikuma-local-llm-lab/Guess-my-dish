import streamlit as st
from game.llm_client import ask_llm
from game.game_core import (
    find_most_similar_dish,
    pick_random_dish,
    match_score,
    compute_similarity,
    compute_bert_similarity,
)
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Meiryo'


def play_sound_hidden(file_path: str):
    # JavaScriptでオーディオ再生し、バー非表示
    st.markdown(
        f"""
        <script>
        var audio = new Audio('{file_path}');
        audio.play();
        </script>
        """,
        unsafe_allow_html=True,
    )

# 自動補完（入力履歴）を無効にするCSS
st.markdown(
    """
    <style>
    input[type="text"] {
        autocomplete: off;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="材料ヒントゲーム", page_icon="🍳")

# --- セッション初期化 ---
if "dish" not in st.session_state:
    st.session_state.dish, st.session_state.ingredients = pick_random_dish()

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🍳 材料ヒントで料理名を当てるゲーム")
st.markdown(f"### 🎯 お題の料理名：**{st.session_state.dish}**")

# 材料入力欄の作成（セッションキー利用）
ings = []
for i in range(5):
    key = f"ing{i}"
    if key not in st.session_state:
        st.session_state[key] = ""
    ings.append(st.text_input(f"材料 {i+1}", key=key))

# --- 入力リセット ---
if st.button("🧹 入力をリセット"):
    for i in range(5):
        key = f"ing{i}"
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# --- 推測処理 ---
if st.button("LLMに推測させる"):
    filtered = [i for i in ings if i.strip()]
    if not filtered:
        st.warning("1つ以上材料を入力してください。")
    else:
        guess = ask_llm(filtered)
        score = compute_similarity(guess, st.session_state.dish)
        bert_score = compute_bert_similarity(guess, st.session_state.dish)

        # 結果を履歴に保存
        st.session_state.history.append({
            "予想": guess,
            "正解": st.session_state.dish,
            "一致度": score,
            "意味類似": bert_score
        })

        st.markdown(f"### 🧠 AIの予想: **{guess}**")
        st.metric("一致度スコア（RapidFuzz）", f"{score*100:.1f}%")
        st.metric("意味類似スコア（BERT）", f"{bert_score*100:.1f}%")

        similar_dishes = find_most_similar_dish(guess, top_k=3)
        st.markdown("### 🔍 類似料理ランキング（RAG風）")
        for idx, item in enumerate(similar_dishes, 1):
            st.markdown(f"{idx}. **{item['dish']}**（スコア: {item['score']*100:.1f}%）")

        # 判定とサウンド
        if score == 1.0:
            st.success("🎉 正解！")
            st.balloons()
            st.audio("sounds/correct.mp3", autoplay=True)
        elif bert_score >= 0.85:
            st.info(f"🤔 かなり意味的に近い料理です！正解は「{st.session_state.dish}」でした。")
            st.audio("sounds/close.mp3", autoplay=True)
        elif score >= 0.75:
            st.info(f"⚠ 惜しい！かなり近い料理名です。正解は「{st.session_state.dish}」でした。")
            st.audio("sounds/close.mp3", autoplay=True)
        else:
            st.error(f"❌ 不正解。正解は「{st.session_state.dish}」でした。")
            st.audio("sounds/wrong.mp3", autoplay=True)

# --- 履歴とグラフ表示 ---
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.markdown("## 📊 過去の推測履歴")
    st.dataframe(df)

    st.markdown("### 🔎 類似度のスコア推移")
    fig, ax = plt.subplots()
    ax.plot(df.index+1, df["一致度"], label="一致度（RapidFuzz）", marker="o")
    ax.plot(df.index+1, df["意味類似"], label="意味類似（BERT）", marker="x")
    ax.set_xlabel("試行回数")
    ax.set_ylabel("スコア")
    ax.set_ylim(0,1.0)
    ax.legend()
    st.pyplot(fig)

# --- 新しいお題ボタン ---
if st.button("🔄 新しいお題に挑戦！"):
    st.session_state.dish, st.session_state.ingredients = pick_random_dish()
    # セッションの入力キーを削除し初期化
    for i in range(5):
        key = f"ing{i}"
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
