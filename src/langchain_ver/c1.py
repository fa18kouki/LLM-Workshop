"""
演習C1: 並列処理で記事を複数観点から評価しよう（LangChain版 回答）

【実行方法】
uv run python src/langchain_ver/c1.py
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)


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


def create_evaluation_chain(system_prompt: str):
    """プロンプトから評価チェーンを作成"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{article}"),
        ]
    )
    return prompt | llm.with_structured_output(Evaluation)


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


def evaluate_article(article: str) -> ArticleEvaluationResult:
    """記事を4つの評価軸で並列評価"""
    # RunnableParallelを使って並列実行
    parallel_chain = RunnableParallel(
        {
            "technical_accuracy": create_evaluation_chain(TECHNICAL_ACCURACY_PROMPT),
            "clarity": create_evaluation_chain(CLARITY_PROMPT),
            "structure": create_evaluation_chain(STRUCTURE_PROMPT),
            "seo": create_evaluation_chain(SEO_PROMPT),
        }
    )

    results = parallel_chain.invoke({"article": article})

    return ArticleEvaluationResult.model_validate(results)


if __name__ == "__main__":
    # 評価対象の記事を読み込み
    with open("data/bad_quality_article.md") as f:
        article = f.read()

    # 並列評価を実行
    results = evaluate_article(article)

    # 評価結果を表示
    print(results.model_dump_json(indent=2))
