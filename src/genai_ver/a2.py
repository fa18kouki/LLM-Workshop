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


def generate_story(keyword: str, temperature: float) -> str:
    """キーワードから短い小説を生成する"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"「{keyword}」をテーマに、3文程度の短い小説を書いてください。",
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
    print("【小説生成】温度による違いを確認")
    print("=" * 60)

    keyword = "月明かり"

    for temp in [0.1, 1.0, 1.5]:
        print(f"\n--- temperature={temp} ---")
        # 同じ温度で3回生成して違いを確認
        for i in range(3):
            result = generate_story(keyword, temp)
            print(f"[{i + 1}] {result[:100]}...")
            print()

    print("\n" + "=" * 60)
    print("【翻訳】温度による違いを確認")
    print("=" * 60)

    text = "桜の花が満開で、公園はとても美しかった。"

    for temp in [0.1, 1.0]:
        print(f"\n--- temperature={temp} ---")
        for i in range(3):
            result = translate_text(text, temp)
            print(f"[{i + 1}] {result}")
