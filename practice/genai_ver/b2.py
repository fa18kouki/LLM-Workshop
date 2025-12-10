"""
演習B2: 構造化出力でより複雑なデータを抽出しよう

【目標】
- 複数フィールドを持つスキーマの定義方法を学ぶ
- ge/le などの制約を使ったバリデーションを体験

【実行方法】
uv run python practice/genai_ver/b2.py

【ヒント】
- Field の ge/le で数値の範囲を制限できる
- 複数のフィールドを定義して情報を構造化
"""

from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel, Field

client = genai.Client()


class CommentAnalysis(BaseModel):
    """コメントの詳細分析結果"""

    # ========================================
    # TODO: 以下のフィールドを定義してください
    # - product_name: str = Field(description="商品名")
    # - positive_points: str = Field(description="ポジティブな点")
    # - negative_points: str = Field(description="ネガティブな点")
    # - score: int = Field(description="5段階のスコア", ge=1, le=5)
    # ========================================
    pass  # ← ここを修正


def analyze_comment(comment: str) -> CommentAnalysis:
    """コメントから詳細情報を抽出する"""
    # ========================================
    # TODO: 構造化出力を使ってLLMを呼び出してください
    # ========================================
    response = None  # ← ここを修正
    return CommentAnalysis.model_validate_json(response.text)


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
