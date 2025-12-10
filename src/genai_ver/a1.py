"""
演習A1: 入力された文から趣味を単語で抽出する（回答）

【実行方法】
uv run python src/genai_ver/a1.py
"""

from google import genai

# Google AI クライアントを初期化
client = genai.Client()


def extract_hobby(input_text: str) -> str:
    """入力文から趣味を抽出する"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"入力文から趣味を単語で抽出してください。\n入力文: {input_text}",
    )
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
