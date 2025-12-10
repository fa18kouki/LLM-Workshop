"""
演習C2: 評価結果に基づいて記事を修正しよう（LangChain版）

【目標】
- 評価結果を元に別のLLM呼び出しを行う
- システムプロンプトに動的にフィードバックを埋め込む

【実行方法】
uv run python practice/langchain_ver/c2.py

【ヒント】
- c1.py の evaluate_article を使って評価を取得
- ChatPromptTemplate で system と human を組み合わせる
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# C1の評価クラスとevaluate_articleをインポート
from c1 import evaluate_article, ArticleEvaluationResult

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)


class ArticleRevision(BaseModel):
    """記事の修正版"""

    revised_article: str = Field(description="修正後の記事（マークダウン形式）")
    changes_summary: list[str] = Field(description="主な変更点のサマリー")


revision_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """与えられた技術記事を、提供された評価フィードバックに基づいて修正してください。
# 修正方針
- 技術的正確性: コードの問題を修正し、正確な説明に書き換える
- わかりやすさ: 初心者にも理解しやすいように説明を丁寧にする
- 構成・論理展開: 話の流れを改善し、適切な見出し構成にする
- SEO最適化: タイトルや見出しを改善し、キーワードを適切に配置する

# 評価フィードバック
{feedback}
""",
        ),
        ("human", "{article}"),
    ]
)

revision_chain = revision_prompt | llm.with_structured_output(ArticleRevision)


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

    # ========================================
    # TODO: revision_chain を使って記事を修正
    # ヒント:
    #   return revision_chain.invoke({"article": article, "feedback": feedback})
    # ========================================
    return None  # ← ここを修正


def main():
    # 評価対象の記事を読み込み
    with open("data/bad_quality_article.md") as f:
        article = f.read()

    print("=== 記事の評価を実行中 ===")
    # C1の並列評価を実行
    evaluation_results = evaluate_article(article)
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
    main()
