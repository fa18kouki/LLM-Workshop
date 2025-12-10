"""
演習A3: 思考（Thinking）のON/OFFを切り替えてレイテンシの差を感じよう（LangChain版 回答）

【実行方法】
uv run python src/langchain_ver/a3.py
"""

import time

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


def solve_problem(problem: str, thinking_budget: int) -> dict:
    """問題を解く（思考設定付き）"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        thinking_budget=thinking_budget,
    )

    prompt = PromptTemplate.from_template("{problem}")
    chain = prompt | llm

    start_time = time.time()
    result = chain.invoke({"problem": problem})
    elapsed_time = time.time() - start_time

    return {
        "answer": result.content,
        "elapsed_time": elapsed_time,
    }


if __name__ == "__main__":
    # 推論が必要な問題
    problem = """
    次の問題を解いてください。

    AさんはBさんより5歳年上です。
    BさんはCさんより3歳年下です。
    Cさんは20歳です。
    Aさんは何歳ですか？
    """

    print("=" * 60)
    print("【思考なし】thinking_budget=0")
    print("=" * 60)
    result = solve_problem(problem, thinking_budget=0)
    print(f"回答: {result['answer']}")
    print(f"処理時間: {result['elapsed_time']:.2f}秒")

    print("\n" + "=" * 60)
    print("【思考あり】thinking_budget=1024")
    print("=" * 60)
    result = solve_problem(problem, thinking_budget=1024)
    print(f"回答: {result['answer']}")
    print(f"処理時間: {result['elapsed_time']:.2f}秒")
