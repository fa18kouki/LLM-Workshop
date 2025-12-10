"""
演習C2: 評価結果に基づいて記事を修正しよう（回答）

【実行方法】
uv run python src/genai_ver/c2.py
"""

from google import genai
from google.genai import types
from pydantic import BaseModel, Field
import asyncio

# C1の評価クラスをインポート
from c1 import evaluate_article, ArticleEvaluationResult

client = genai.Client()


class ArticleRevision(BaseModel):
    """記事の修正版"""

    revised_article: str = Field(description="修正後の記事（マークダウン形式）")
    changes_summary: list[str] = Field(description="主な変更点のサマリー")


def revise_article(article: str, evaluation: ArticleEvaluationResult) -> ArticleRevision:
    """4つの評価結果を元に記事を修正"""

    # 評価結果をテキスト形式で整形
    technical = evaluation.technical_accuracy
    clarity = evaluation.clarity
    structure = evaluation.structure
    seo = evaluation.seo

    feedback = f"""
# 技術的正確性の評価
修正必要: {technical.needs_revision}
優れている点: {', '.join(technical.good_points)}
改善が必要な点: {', '.join(technical.bad_points)}

# わかりやすさの評価
修正必要: {clarity.needs_revision}
優れている点: {', '.join(clarity.good_points)}
改善が必要な点: {', '.join(clarity.bad_points)}

# 構成・論理展開の評価
修正必要: {structure.needs_revision}
優れている点: {', '.join(structure.good_points)}
改善が必要な点: {', '.join(structure.bad_points)}

# SEO最適化の評価
修正必要: {seo.needs_revision}
優れている点: {', '.join(seo.good_points)}
改善が必要な点: {', '.join(seo.bad_points)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=article,
        config=types.GenerateContentConfig(
            system_instruction=f"""与えられた技術記事を、提供された評価フィードバックに基づいて修正してください。
# 修正方針
- 技術的正確性: コードの問題を修正し、正確な説明に書き換える
- わかりやすさ: 初心者にも理解しやすいように説明を丁寧にする
- 構成・論理展開: 話の流れを改善し、適切な見出し構成にする
- SEO最適化: タイトルや見出しを改善し、キーワードを適切に配置する

# 評価フィードバック
{feedback}
""",
            response_mime_type="application/json",
            response_schema=ArticleRevision,
            temperature=0.3,
        ),
    )
    return ArticleRevision.model_validate_json(response.text)


async def main():
    # 評価対象の記事を読み込み
    with open("data/bad_quality_article.md") as f:
        article = f.read()

    print("=== 記事の評価を実行中 ===")
    # C1の並列評価を実行
    evaluation_results = await evaluate_article(article)
    print(evaluation_results.model_dump_json(indent=2))

    print("=== 評価結果に基づいて記事を修正中 ===")
    # 評価結果を元に記事を修正
    revision = revise_article(article, evaluation_results)

    print("=== 修正完了 ===")
    print("【主な変更点】")
    for i, change in enumerate(revision.changes_summary, 1):
        print(f"{i}. {change}")

    # 修正後の記事を保存
    output_path = "result/revised_article.md"
    with open(output_path, "w") as f:
        f.write(revision.revised_article)

    print(f"修正後の記事を {output_path} に保存しました。")


if __name__ == "__main__":
    asyncio.run(main())
