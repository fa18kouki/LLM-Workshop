"""
演習F3 解答例: タスク管理エージェント

【実行方法】
uv run python src/genai_ver/f3.py

【機能】
- タスクの追加・完了・一覧
- 現在の日時取得

※ これは一つの例です。自由に別のツールを作ってOK！
"""

import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

# タスクリスト（メモリ上で管理）
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

    tools = [add_task, complete_task, list_tasks, get_current_datetime]
    history = []

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
