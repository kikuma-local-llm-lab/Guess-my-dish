import streamlit as st
from game.llm_client import ask_llm
from game.game_core import pick_random_dish, match_score

st.set_page_config(page_title="材料ヒントゲーム", page_icon="🍳")

# セッションにお題を保持
if "dish" not in st.session_state:
    st.session_state.dish, st.session_state.ingredients = pick_random_dish()

st.title("🍳 材料ヒントで料理名を当てるゲーム")
st.markdown(f"### 🎯 お題の料理名：**{st.session_state.dish}**")

ings = [st.text_input(f"材料 {i+1}", key=f"ing{i}") for i in range(5)]

if st.button("LLMに推測させる"):
    filtered = [i for i in ings if i.strip()]
    if not filtered:
        st.warning("1つ以上材料を入力してください。")
    else:
        guess = ask_llm(filtered)
        st.markdown(f"### 🤖 AIの予想: **{guess}**")
        if match_score(guess, st.session_state.dish) > 0.8:
            st.success("🎉 正解！")
            st.balloons()
        else:
            st.error(f"❌ 不正解。正解は「{st.session_state.dish}」でした。")

if st.button("🔄 新しいお題に挑戦！"):
    st.session_state.dish, st.session_state.ingredients = pick_random_dish()
    st.rerun()
