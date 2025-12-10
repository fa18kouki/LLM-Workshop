"""
演習C1: 並列処理で記事を複数観点から評価しよう（回答）

【実行方法】
uv run python src/genai_ver/c1.py
"""

from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel, Field
import asyncio

client = genai.Client()


class Evaluation(BaseModel):
    """評価結果"""

    needs_revision: bool = Field(description="修正が必要かどうか")
    good_points: list[str] = Field(description="優れている点")
    bad_points: list[str] = Field(description="改善が必要な点")


class ArticleEvaluationResult(BaseModel):
    """記事の総合評価結果"""

    technical_accuracy: Evaluation = Field(description="技術的正確性の評価")
    clarity: Evaluation = Field(description="わかりやすさの評価")
    structure: Evaluation = Field(description="構成・論理展開の評価")
    seo: Evaluation = Field(description="SEO最適化の評価")


async def evaluate_aspect(system_prompt: str, article: str) -> Evaluation:
    """特定の観点で記事を評価"""
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=article,
        config=GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=Evaluation,
            temperature=0.1,
        ),
    )
    return Evaluation.model_validate_json(response.text)


# 各評価軸のプロンプト
TECHNICAL_ACCURACY_PROMPT = """与えられた技術記事の**技術的正確性**を評価してください。
- 評価観点: コードの妥当性、説明の正確さ、情報の完全性
- 判定基準: 重大な問題がある場合は修正が必要（needs_revision = true）
"""

CLARITY_PROMPT = """与えられた技術記事の**わかりやすさ**を評価してください。
- 評価観点: 初心者への配慮、説明の丁寧さ、可読性
- 判定基準: 説明が不十分で理解しづらい場合は修正が必要（needs_revision = true）
"""

STRUCTURE_PROMPT = """与えられた技術記事の**構成・論理展開**を評価してください。
- 評価観点: 目次構成、話の流れ、全体のバランス
- 判定基準: 構成に問題があり話の流れが悪い場合は修正が必要（needs_revision = true）
"""

SEO_PROMPT = """与えられた技術記事の**SEO最適化**を評価してください。
- 評価観点: タイトルの適切性、見出しの工夫、キーワードの使用
- 判定基準: SEO対策が不十分で改善の余地が大きい場合は修正が必要（needs_revision = true）
"""


async def evaluate_article(article: str) -> ArticleEvaluationResult:
    """記事を4つの評価軸で並列評価"""
    technical, clarity, structure, seo = await asyncio.gather(
        evaluate_aspect(TECHNICAL_ACCURACY_PROMPT, article),
        evaluate_aspect(CLARITY_PROMPT, article),
        evaluate_aspect(STRUCTURE_PROMPT, article),
        evaluate_aspect(SEO_PROMPT, article),
    )

    return ArticleEvaluationResult(
        technical_accuracy=technical,
        clarity=clarity,
        structure=structure,
        seo=seo,
    )


if __name__ == "__main__":
    # 評価対象の記事を読み込み
    with open("data/bad_quality_article.md") as f:
        article = f.read()

    # 並列評価を実行
    results = asyncio.run(evaluate_article(article))

    # 評価結果を表示
    print(results.model_dump_json(indent=2))
