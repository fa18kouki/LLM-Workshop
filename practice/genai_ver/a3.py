"""
演習A3: 思考（Thinking）のON/OFFを切り替えてレイテンシの差を感じよう

【目標】
- Reasoning/Thinking モデルの概念を理解する
- thinking_budget の設定方法を学ぶ
- 思考過程の表示方法を学ぶ

【実行方法】
uv run python practice/genai_ver/a3.py

【ヒント】
- ThinkingConfig で thinking_budget を設定
  - thinking_budget=0: 思考なし（高速）
  - thinking_budget>0: 思考あり（より深い推論）
- include_thoughts=True で思考過程を取得可能
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

    # ========================================
    # TODO: ThinkingConfig を設定してください
    # ヒント:
    #   thinking_config=ThinkingConfig(
    #       thinking_budget=thinking_budget,
    #       include_thoughts=include_thoughts
    #   )
    # ========================================
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=problem,
        # ← config を追加
    )

    elapsed_time = time.time() - start_time

    result = {
        "answer": response.text,
        "elapsed_time": elapsed_time,
        "thoughts": None,
    }

    # ========================================
    # TODO: 思考過程を取得してください（include_thoughts=True の場合）
    # ヒント:
    #   response.candidates[0].content.parts で parts を取得
    #   各 part に thought 属性があれば思考過程
    # ========================================

    return result


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
    result = solve_problem(problem, thinking_budget=1024, include_thoughts=True)
    print(f"回答: {result['answer']}")
    print(f"処理時間: {result['elapsed_time']:.2f}秒")

    if result["thoughts"]:
        print("\n--- 思考過程 ---")
        print(result["thoughts"])
