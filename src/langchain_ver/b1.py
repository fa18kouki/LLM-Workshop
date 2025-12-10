"""
演習B1: 構造化出力（Structured Output）で感情分析しよう（LangChain版 回答）

【実行方法】
uv run python src/langchain_ver/b1.py
"""

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Literal

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)


class CommentAnalysis(BaseModel):
    """コメントの感情分析結果"""

    sentiment: Literal["positive", "negative", "neutral"] = Field(
        description="判定結果。positive: ポジティブ、negative: ネガティブ、neutral: ニュートラル"
    )


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
    chain = prompt | llm.with_structured_output(CommentAnalysis)
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
