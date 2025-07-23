# streamlit_game.py
import streamlit as st
from game.llm_client import ask_llm
from game.game_core import pick_random_dish, match_score

if "dish" not in st.session_state:
    st.session_state.dish, st.session_state.ingredients = pick_random_dish()

st.title("🧪 材料ヒントで料理名を当てるゲーム")
ings = [st.text_input(f"材料 {i+1}") for i in range(5)]

if st.button("LLMに推測させる"):
    guess = ask_llm([i for i in ings if i])
    st.markdown(f"### 🤖 AIの予想: **{guess}**")
    if match_score(guess, st.session_state.dish) > 0.8:
        st.success("🎉 正解！")
        st.balloons()
    else:
        st.error(f"❌ 不正解。正解は「{st.session_state.dish}」でした。")

    if st.button("もう一回"):
        st.session_state.dish, st.session_state.ingredients = pick_random_dish()
        st.experimental_rerun()
