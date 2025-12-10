"""
演習B1: 構造化出力（Structured Output）で感情分析しよう

【目標】
- LLMの出力をPydanticモデルで構造化する方法を学ぶ
- response_schema を使った型安全な出力を体験する

【実行方法】
uv run python practice/genai_ver/b1.py

【ヒント】
- GenerateContentConfig で response_mime_type と response_schema を設定
- Pydantic の BaseModel で出力スキーマを定義
- Literal 型で選択肢を制限できる
"""

from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel, Field
from typing import Literal

client = genai.Client()


class CommentAnalysis(BaseModel):
    """コメントの感情分析結果"""

    # ========================================
    # TODO: sentiment フィールドを定義してください
    # ヒント:
    #   sentiment: Literal["positive", "negative", "neutral"] = Field(
    #       description="判定結果。positive: ポジティブ、negative: ネガティブ、neutral: ニュートラル"
    #   )
    # ========================================
    pass  # ← ここを修正


def analyze_sentiment(comment: str) -> CommentAnalysis:
    """コメントの感情を分析する"""
    # ========================================
    # TODO: 構造化出力を使ってLLMを呼び出してください
    # ヒント:
    #   response = client.models.generate_content(
    #       model="gemini-2.5-flash",
    #       contents="...",
    #       config=GenerateContentConfig(
    #           response_mime_type="application/json",
    #           response_schema=CommentAnalysis,
    #           temperature=0.1,
    #       ),
    #   )
    #   return CommentAnalysis.model_validate_json(response.text)
    # ========================================
    response = None  # ← ここを修正
    return CommentAnalysis.model_validate_json(response.text)


if __name__ == "__main__":
    test_comments = [
        "スマート加湿器を購入。静音性は期待通り。給水が面倒なのがマイナス。5点満点中3点といったところ。",
        "この商品は本当に素晴らしい！大満足です！",
        "期待はずれでした。二度と買いません。",
        "普通の商品です。可もなく不可もなく。",
    ]

    print("=" * 60)
    print("感情分析（Structured Output使用）")
    print("=" * 60)

    for comment in test_comments:
        result = analyze_sentiment(comment)
        print(f"\nコメント: {comment[:30]}...")
        print(f"感情: {result.sentiment}")
        print("-" * 40)
