"""
演習D4: Function Callingで独自関数を呼び出そう（回答）

【実行方法】
uv run python src/genai_ver/d4.py
"""

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()


# 関数を定義
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
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config=types.GenerateContentConfig(
            tools=[get_current_temperature, get_current_humidity]
        ),
    )
    return response.text


if __name__ == "__main__":
    query = "今日の東京の気温と湿度を調べてください"

    print("=" * 60)
    print("Function Calling（独自関数）")
    print("=" * 60)

    print(f"\n質問: {query}")
    result = call_with_tools(query)
    print(f"\n回答:\n{result}")
