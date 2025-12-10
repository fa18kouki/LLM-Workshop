"""
演習D2: Google検索ツールを使おう

【目標】
- Gemini の組み込みツール（Google Search）の使い方を学ぶ
- ツールを使った最新情報の取得

【実行方法】
uv run python practice/genai_ver/d2.py

【ヒント】
- types.Tool(google_search=types.GoogleSearch()) でツールを定義
- config の tools パラメータに渡す
"""

from google import genai
from google.genai import types

client = genai.Client()


def search_web(query: str) -> str:
    """Google検索を使って情報を取得する"""
    # ========================================
    # TODO: Google検索ツールを使ってLLMを呼び出す
    # ヒント:
    #   response = client.models.generate_content(
    #       model="gemini-2.5-flash",
    #       contents=query,
    #       config=types.GenerateContentConfig(
    #           tools=[types.Tool(google_search=types.GoogleSearch())]
    #       ),
    #   )
    # ========================================
    response = None  # ← ここを修正
    return response.text


if __name__ == "__main__":
    queries = [
        "東京の今日の天気を調べてください",
        "最新のPython 3.13の新機能について教えてください",
    ]

    print("=" * 60)
    print("Google検索ツール使用")
    print("=" * 60)

    for query in queries:
        print(f"\n質問: {query}")
        print("-" * 40)
        result = search_web(query)
        print(f"回答:\n{result}")
        print("=" * 60)
