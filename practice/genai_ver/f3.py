"""
演習F3: エージェント設計の考え方を理解しよう（発展）

【目標】
- タスク管理エージェントの完成コードを読んで、設計の考え方を理解する
- なぜツール関数を複数に分けるのかを理解する
- 「どんなツールを定義すれば、どんなエージェントが作れるか」を考える力をつける

【重要】
このコードは完成版です。実装する必要はありません。
F1・F2で学んだ概念が、別のドメイン（タスク管理）でも
同じように適用されていることを確認してください。

【実行方法】
uv run python practice/genai_ver/f3.py

【学習の進め方】
1. ツール関数の設計を読む（なぜ3つに分けた？）
2. 実行してタスク管理を体験する
3. ファイル末尾のディスカッション課題を考える
"""

import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()


# ===========================================
# ツール設計: タスク管理
#
# WHY: エージェント開発の本質は「ツール設計」です。
#      タスク管理という1つの機能を
#      add_task / complete_task / list_tasks の3つに分けています。
#
#      1つの巨大な manage_task(action, ...) にすることもできますが、
#      分けることで:
#        - LLMが「何をしたいか」をより正確に判断できる
#        - 各ツールの責任が明確になる
#        - docstringが具体的に書ける
# ===========================================

TASKS: list[dict] = []


def add_task(task: str) -> dict[str, str]:
    """
    タスクを追加する関数

    Args:
        task: タスクの内容

    Returns:
        追加結果を含む辞書
    """
    TASKS.append({"task": task, "done": False, "created_at": datetime.now().strftime("%H:%M")})
    return {"status": "success", "task": task, "index": len(TASKS) - 1}


def complete_task(task_index: int) -> dict[str, str]:
    """
    タスクを完了にする関数

    Args:
        task_index: タスクの番号（0始まり）

    Returns:
        完了結果を含む辞書
    """
    if 0 <= task_index < len(TASKS):
        TASKS[task_index]["done"] = True
        return {"status": "success", "task": TASKS[task_index]["task"]}
    return {"error": "タスクが見つかりません"}


def list_tasks() -> dict:
    """
    タスク一覧を取得する関数

    Returns:
        タスクの一覧を含む辞書
    """
    return {
        "tasks": [
            {
                "index": i,
                "task": t["task"],
                "done": t["done"],
                "created_at": t["created_at"],
            }
            for i, t in enumerate(TASKS)
        ],
        "total": len(TASKS),
        "completed": sum(1 for t in TASKS if t["done"]),
    }


def get_current_datetime() -> dict[str, str]:
    """現在の日時を取得する関数"""
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": ["月", "火", "水", "木", "金", "土", "日"][now.weekday()],
    }


def run_agent():
    """タスク管理エージェントを実行"""

    # ===========================================
    # ツールリスト
    # F1: 2個、F2: 5個、F3: 4個
    # 数は違えど、エージェントループは全て同じです。
    # ===========================================
    tools = [add_task, complete_task, list_tasks, get_current_datetime]

    history = []

    # ===========================================
    # システムプロンプト
    # WHY: エージェントの「性格」と「できること」を定義します。
    #      tools でツールの技術仕様を、
    #      system_instruction で使い方の方針を伝えます。
    # ===========================================
    system_instruction = """あなたはタスク管理アシスタントです。
以下の機能を利用できます：
- タスク追加: 新しいタスクを追加
- タスク完了: タスクを完了にする（番号で指定）
- タスク一覧: 現在のタスク一覧を表示
- 日時取得: 現在の日時を取得

ユーザーの要求に応じて適切な機能を使用し、結果をわかりやすく説明してください。"""

    print("=" * 60)
    print("タスク管理エージェント")
    print("=" * 60)
    print("\n利用可能な機能:")
    print("  - タスク追加（例: 「メール返信をタスクに追加して」）")
    print("  - タスク完了（例: 「タスク0を完了にして」）")
    print("  - タスク一覧（例: 「タスクの一覧を見せて」）")
    print("  - 日時取得（例: 「今何時？」）")
    print("\n終了するには 'exit' と入力してください")
    print("=" * 60)

    while True:
        user_input = input("\nあなた: ")

        if user_input.lower() in ("exit", "終了", "quit"):
            print("エージェントを終了します。")
            break

        history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))

        try:
            # エージェントループ（F1・F2と同じ構造）
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=history,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=tools,
                ),
            )

            if response.candidates and response.candidates[0].content:
                candidate = response.candidates[0]
                function_calls = []
                function_results_list = []

                for part in candidate.content.parts:
                    if hasattr(part, "function_call") and part.function_call:
                        func_name = part.function_call.name
                        func_args = {}
                        if hasattr(part.function_call, "args"):
                            args_value = part.function_call.args
                            if isinstance(args_value, str):
                                try:
                                    func_args = json.loads(args_value)
                                except json.JSONDecodeError:
                                    func_args = {}
                            elif isinstance(args_value, dict):
                                func_args = args_value

                        for tool in tools:
                            if tool.__name__ == func_name:
                                print(f"[ツール実行] {func_name}({func_args})")
                                result = tool(**func_args)
                                function_calls.append(part.function_call)
                                function_results_list.append(
                                    types.Part(function_response=types.FunctionResponse(
                                        name=func_name, response=result,
                                    ))
                                )
                                break

                if function_calls and function_results_list:
                    history.append(types.Content(
                        role="model",
                        parts=[types.Part(function_call=fc) for fc in function_calls],
                    ))
                    history.append(types.Content(
                        role="user",
                        parts=function_results_list,
                    ))
                    final_response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=history,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            tools=tools,
                        ),
                    )
                    if final_response.text:
                        print(f"AI: {final_response.text}")
                        history.append(types.Content(
                            role="model",
                            parts=[types.Part(text=final_response.text)],
                        ))
                    else:
                        print("AI: 応答を取得できませんでした。")
                else:
                    if response.text:
                        print(f"AI: {response.text}")
                        history.append(types.Content(
                            role="model",
                            parts=[types.Part(text=response.text)],
                        ))
                    else:
                        print("AI: 応答を取得できませんでした。")

        except Exception as e:
            print(f"[エラー] {e}")


if __name__ == "__main__":
    run_agent()


# ========================================
# 設計理解チェック
# ========================================
#
# Q1. タスク管理を add_task / complete_task / list_tasks の
#     3つの関数に分けています。
#     もし1つの manage_task(action, ...) にまとめたら
#     何が起こりそうですか？
#
# Q2. add_task の docstring を変更すると、
#     LLMの動作は変わりますか？
#     （例: docstring を空にしたらどうなる？）
#
# Q3. もし「タスクの編集」機能を追加したい場合:
#     a) 新しい関数 edit_task を作る必要がありますか？
#     b) エージェントループの処理を変更する必要がありますか？
#     c) tools リストに何を追加すれば良いですか？
#
# Q4. F1・F2・F3のエージェントループのコードを比較してください。
#     3つの間で何が違いますか？何が同じですか？
#
# ========================================
# ディスカッション: あなたの業務で使えるエージェントは？
# ========================================
#
# エージェント = 「ツール関数を定義するだけ」で作れます。
# エージェントループは毎回同じです。
#
# あなたの業務で役立ちそうなエージェントを考えてみましょう:
#
# 例1: 顧客管理エージェント
#   - search_customer(name)  → 顧客を検索
#   - get_customer_info(id)  → 詳細を取得
#   - update_customer(id, field, value) → 情報を更新
#
# 例2: レポート生成エージェント
#   - fetch_sales_data(period) → 売上データ取得
#   - calculate_summary(data)  → 集計
#   - format_report(summary)   → レポート整形
#
# 例3: 翻訳エージェント
#   - detect_language(text)      → 言語検出
#   - translate(text, target)    → 翻訳
#   - proofread(text)            → 校正
#
# あなたならどんなツール関数を定義しますか？
# ========================================
