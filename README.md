
# 🍳 材料ヒントで料理名を当てるゲーム（Guess Dish Game）

材料から料理名を推測する、LLM（大規模言語モデル）を活用したインタラクティブなクイズゲームです。  
ユーザーが材料を最大5つ入力すると、AIが料理名を予想し、文字列一致度と意味的な類似度で結果を可視化します。

---

## 🚀 起動方法（ローカル実行）

```bash
# 仮想環境を作成・アクティブ化
python -m venv .venv
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate

# 必要なライブラリをインストール
pip install -r requirements.txt

# アプリを起動
streamlit run streamlit_game.py
```

---

## 🧠 主な機能

- 材料をもとに LLM が料理名を推測
- 文字列一致度（RapidFuzz）と意味的類似スコア（BERT）で評価
- 類似料理名をランキング形式で表示（RAG風アプローチ）
- 正解・惜しい・不正解に応じて音声フィードバックを再生（PCのみ自動再生対応）
- 履歴表示と類似度の推移グラフ
- 入力欄はセッション制御付き、履歴からの自動補完無効化

---

## 📁 ディレクトリ構成

```
.
├── streamlit_game.py           # メインのStreamlitアプリ
├── game/
│   ├── game_core.py            # 推測ロジックと類似度計算
│   └── llm_client.py           # LLM問い合わせ部分
├── sounds/
│   ├── correct.mp3
│   ├── close.mp3
│   └── wrong.mp3               # 結果に応じた音声フィードバック
├── data/
│   └── dishes.json             # 料理名と材料の辞書データ
├── requirements.txt
└── README.md
```

---

## 📊 スコア評価方式

| 指標           | 内容                                       |
|----------------|--------------------------------------------|
| 一致度スコア   | RapidFuzz による文字列一致率               |
| 意味類似スコア | BERT 埋め込みベースのコサイン類似度         |

類似度の推移はグラフとして可視化されます。

---

## 🔊 サウンドについて

- `st.audio(..., autoplay=True)` により、PCブラウザでは自動再生されます
- モバイルブラウザでは制限により自動再生がブロックされる場合があります
- 音声バーは非表示にできません（ブラウザ仕様上の制限）

---

## 📦 使用ライブラリ

- `streamlit`
- `rapidfuzz`
- `sentence-transformers`
- `pandas`
- `matplotlib`

---

## 📝 ライセンス

MIT License  
© 2025 KikumaNetworkLab

---

## 🙌 コントリビュート歓迎

不具合の報告・機能改善・アイデア提案など、ぜひ [Issues](https://github.com/your-repo/issues) や Pull Request をお送りください！
