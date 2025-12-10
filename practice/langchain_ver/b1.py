"""
演習B1: 構造化出力（Structured Output）で感情分析しよう（LangChain版）

【目標】
- LangChain の with_structured_output を使った構造化出力を学ぶ
- Pydantic モデルとの連携

【実行方法】
uv run python practice/langchain_ver/b1.py

【ヒント】
- llm.with_structured_output(Model) でチェーンを構築
- chain = prompt | llm.with_structured_output(CommentAnalysis)
"""

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Literal

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)


class CommentAnalysis(BaseModel):
    """コメントの感情分析結果"""

    # ========================================
    # TODO: sentiment フィールドを定義してください
    # ヒント:
    #   sentiment: Literal["positive", "negative", "neutral"] = Field(
    #       description="判定結果"
    #   )
    # ========================================
    pass  # ← ここを修正


def analyze_sentiment(comment: str) -> CommentAnalysis:
    """コメントの感情を分析する"""
    prompt = PromptTemplate.from_template(
        """次のコメントがポジティブかネガティブかニュートラルか判定してください。
# コメント
```
{comment}
```
"""
    )
    # ========================================
    # TODO: 構造化出力付きのチェーンを構築
    # ヒント:
    #   chain = prompt | llm.with_structured_output(CommentAnalysis)
    #   return chain.invoke({"comment": comment})
    # ========================================
    chain = None  # ← ここを修正
    return chain.invoke({"comment": comment})


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
