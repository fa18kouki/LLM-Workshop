"""
演習A1: 入力された文から趣味を単語で抽出する

【目標】
- Google GenAI SDK を使って LLM を呼び出す基本を理解する
- プロンプトの書き方を体験する

【実行方法】
uv run python practice/genai_ver/a1.py

【ヒント】
- client.models.generate_content() を使う
- model は "gemini-2.5-flash" を使用
- contents にプロンプト（指示文 + 入力文）を渡す
"""

from google import genai

# ========================================
# TODO: Google AI クライアントを初期化してください
# ヒント: genai.Client()
# ========================================
client = None  # ← ここを修正


def extract_hobby(input_text: str) -> str:
    """入力文から趣味を抽出する"""
    # ========================================
    # TODO: LLM に趣味を抽出させてください
    # ヒント:
    #   response = client.models.generate_content(
    #       model="gemini-2.5-flash",
    #       contents="...",
    #   )
    # ========================================
    response = None  # ← ここを修正

    return response.text


if __name__ == "__main__":
    # テスト用の入力文
    test_inputs = [
        "私はサッカーを趣味にしています。",
        "休日はギターを弾いたり、映画を見たりしています。",
        "最近はプログラミングにハマっています。",
    ]

    for text in test_inputs:
        print(f"入力: {text}")
        result = extract_hobby(text)
        print(f"抽出結果: {result}")
        print("-" * 40)
