"""
演習A3: 思考（Thinking）のON/OFFを切り替えてレイテンシの差を感じよう（回答）

【実行方法】
uv run python src/genai_ver/a3.py
"""

import time

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig, ThinkingConfig

load_dotenv()

client = genai.Client()


def solve_problem(problem: str, thinking_budget: int, include_thoughts: bool = False) -> dict:
    """問題を解く（思考設定付き）"""
    start_time = time.time()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=problem,
        config=GenerateContentConfig(
            thinking_config=ThinkingConfig(
                thinking_budget=thinking_budget,
                include_thoughts=include_thoughts,
            )
        ),
    )

    elapsed_time = time.time() - start_time

    result = {
        "answer": response.text,
        "elapsed_time": elapsed_time,
        "thoughts": None,
    }

    # 思考過程を取得
    if include_thoughts and response.candidates:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "thought") and part.thought:
                result["thoughts"] = part.text
                break

    return result


if __name__ == "__main__":
    # 推論が必要な問題
    problem = """
    次の論理パズルを解いてください。

    5人の学生（A、B、C、D、E）は数学、物理、化学、生物、地学の5つの科目をそれぞれ異なる科目で優秀賞を取りました。
    以下の手がかりから、誰がどの科目で優秀賞を取ったかを特定してください。

    1. Aさんは数学か物理のどちらかで優秀賞を取りましたが、数学はCさんが取りました。
    2. Bさんは生物を取りました。
    3. Dさんは地学を取りましたが、Eさんは地学を取りませんでした。
    4. Cさんは物理より、数学を取りました。
    5. 化学はAさんかEさんのどちらかが取りました。

    全員の科目を特定してください。
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
    result = solve_problem(problem, thinking_budget=1024, include_thoughts=True)
    print(f"回答: {result['answer']}")
    print(f"処理時間: {result['elapsed_time']:.2f}秒")

    if result["thoughts"]:
        print("\n--- 思考過程 ---")
        print(result["thoughts"])
