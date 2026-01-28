"""
演習F1 解答: 基本エージェントの構築

【実行方法】
uv run python src/genai_ver/f1.py

【機能】
- 計算（四則演算）
- 現在の日時取得
- 対話履歴を保持しながら適切なツールを選択
"""

import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()


def calculate(expression: str) -> dict[str, str]:
    """
    数式を計算する関数

    Args:
        expression: 計算式（例: "2 + 3 * 4", "100 / 5"）

    Returns:
        計算結果を含む辞書
    """
    try:
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return {"error": "無効な文字が含まれています", "result": None}
        result = eval(expression)  # noqa: S307
        return {"result": str(result), "expression": expression}
    except Exception as e:
        return {"error": str(e), "result": None}


def get_current_datetime() -> dict[str, str]:
    """
    現在の日時を取得する関数

    Returns:
        現在の日時を含む辞書
    """
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "weekday": ["月", "火", "水", "木", "金", "土", "日"][now.weekday()],
    }


def run_agent():
    """基本エージェントを実行"""

    tools = [calculate, get_current_datetime]
    history = []

    system_instruction = """あなたは親切なアシスタントです。
以下の機能を利用できます：
- 計算: 数式を計算できます
- 日時: 現在の日時を取得できます

ユーザーの要求に応じて、適切な機能を使用してください。"""

    print("=" * 60)
    print("基本エージェント（計算 + 日時）")
    print("=" * 60)
    print("\n利用可能な機能:")
    print("  - 計算（例: 「3 + 5 * 2を計算して」）")
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
                        print("[ツール未使用] LLMが直接回答しました")
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
