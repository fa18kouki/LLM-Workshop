"""
演習D4: Function Callingで独自関数を呼び出そう

【目標】
- 独自の Python 関数をツールとしてLLMに渡す方法を学ぶ
- Function Calling の仕組みを理解する

【実行方法】
uv run python practice/genai_ver/d4.py

【ヒント】
- Python 関数を直接 tools リストに渡せる
- 関数の docstring が説明として使われる
"""

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()


# ========================================
# TODO: 以下の関数を定義してください
# ========================================


def get_current_temperature(location: str) -> dict[str, str]:
    """今日の気温を調べる関数"""
    # 実際の実装ではAPIを呼び出すなど
    return {"気温": "25℃"}


def get_current_humidity(location: str) -> dict[str, str]:
    """今日の湿度を調べる関数"""
    # 実際の実装ではAPIを呼び出すなど
    return {"湿度": "50%"}


def call_with_tools(query: str) -> str:
    """ツール付きでLLMを呼び出す"""
    # ========================================
    # TODO: 独自関数をツールとしてLLMに渡す
    # ヒント:
    #   response = client.models.generate_content(
    #       model="gemini-2.5-flash",
    #       contents=query,
    #       config=types.GenerateContentConfig(
    #           tools=[get_current_temperature, get_current_humidity]
    #       ),
    #   )
    # ========================================
    response = None  # ← ここを修正
    return response.text


if __name__ == "__main__":
    query = "今日の東京の気温と湿度を調べてください"

    print("=" * 60)
    print("Function Calling（独自関数）")
    print("=" * 60)

    print(f"\n質問: {query}")
    result = call_with_tools(query)
    print(f"\n回答:\n{result}")
