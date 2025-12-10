"""
演習B2: 構造化出力でより複雑なデータを抽出しよう（回答）

【実行方法】
uv run python src/genai_ver/b2.py
"""

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel, Field

load_dotenv()

client = genai.Client()


class CommentAnalysis(BaseModel):
    """コメントの詳細分析結果"""

    product_name: str = Field(description="商品名")
    positive_points: str = Field(description="ポジティブな点")
    negative_points: str = Field(description="ネガティブな点")
    score: int = Field(description="5段階のスコア", ge=1, le=5)


def analyze_comment(comment: str) -> CommentAnalysis:
    """コメントから詳細情報を抽出する"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""次のコメントを分析して、商品名、ポジティブな点、ネガティブな点、5段階のスコアを返してください。
# コメント
```
{comment}
```
""",
        config=GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CommentAnalysis,
            temperature=0.1,
        ),
    )
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
