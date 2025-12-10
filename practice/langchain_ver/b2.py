"""
演習B2: 構造化出力でより複雑なデータを抽出しよう（LangChain版）

【目標】
- 複数フィールドを持つスキーマの定義
- LangChain での構造化出力の活用

【実行方法】
uv run python practice/langchain_ver/b2.py

【ヒント】
- Pydantic の Field で制約を定義（ge, le など）
- with_structured_output で型安全な出力を取得
"""

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)


class CommentAnalysis(BaseModel):
    """コメントの詳細分析結果"""

    # ========================================
    # TODO: 以下のフィールドを定義してください
    # - product_name: str
    # - positive_points: str
    # - negative_points: str
    # - score: int (ge=1, le=5)
    # ========================================
    pass  # ← ここを修正


def analyze_comment(comment: str) -> CommentAnalysis:
    """コメントから詳細情報を抽出する"""
    prompt = PromptTemplate.from_template(
        """次のコメントを分析して、商品名、ポジティブな点、ネガティブな点、5段階のスコアを返してください。
# コメント
```
{comment}
```
"""
    )
    # ========================================
    # TODO: 構造化出力付きのチェーンを構築して実行
    # ========================================
    chain = None  # ← ここを修正
    return chain.invoke({"comment": comment})


if __name__ == "__main__":
    comment = "スマート加湿器を購入。静音性は期待通り。給水が面倒なのがマイナス。5点満点中3点といったところ。"

    print("=" * 60)
    print("コメント詳細分析（Structured Output使用）")
    print("=" * 60)

    result = analyze_comment(comment)

    print(f"\n元のコメント:\n{comment}")
    print("\n--- 分析結果 ---")
    print(f"商品名: {result.product_name}")
    print(f"ポジティブな点: {result.positive_points}")
    print(f"ネガティブな点: {result.negative_points}")
    print(f"スコア: {result.score}/5")
