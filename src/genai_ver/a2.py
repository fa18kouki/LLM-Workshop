"""
演習A2: 温度（temperature）を調整して出力の差を感じよう（回答）

【実行方法】
uv run python src/genai_ver/a2.py
"""

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig

load_dotenv()

client = genai.Client()


def generate_introduction(keyword: str, temperature: float) -> str:
    """キーワードを含む自己紹介を生成する"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"「{keyword}」というキーワードを必ず含めて、3文程度の自己紹介文を書いてください。",
        config=GenerateContentConfig(temperature=temperature),
    )
    return response.text


def translate_text(text: str, temperature: float) -> str:
    """テキストを英語に翻訳する"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"次の文を英語に翻訳してください。\n{text}",
        config=GenerateContentConfig(temperature=temperature),
    )
    return response.text


if __name__ == "__main__":
    print("=" * 60)
    print("【自己紹介生成】温度による違いを確認")
    print("=" * 60)

    keyword = "プログラミング"

    for temp in [0, 0.1, 1.0, 1.5]:
        print(f"\n--- temperature={temp} ---")
        # 同じ温度で3回生成して違いを確認
        for i in range(3):
            result = generate_introduction(keyword, temp)
            print(f"[{i + 1}] {result[:100]}...")
            print()

    print("\n" + "=" * 60)
    print("【翻訳】温度による違いを確認")
    print("=" * 60)

    text = "私はフロントエンドエンジニアとして、Webアプリケーションの開発に携わっています。"

    for temp in [0, 0.1, 1.0]:
        print(f"\n--- temperature={temp} ---")
        for i in range(3):
            result = translate_text(text, temp)
            print(f"[{i + 1}] {result}")
