"""演習F3 解答コードの統合テスト（API呼び出し含む）

タスク管理エージェントがFunction Callingで
タスクの追加・一覧を行えるかを確認する。
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

import pytest
from google import genai
from google.genai import types
from genai_ver import f3
from genai_ver.f3 import add_task, complete_task, list_tasks, get_current_datetime

client = genai.Client()


@pytest.fixture(autouse=True)
def clear_tasks():
    f3.TASKS.clear()
    yield


def run_single_turn(user_input: str, tools: list) -> str:
    """エージェントの1ターンを実行"""
    system_instruction = """あなたはタスク管理アシスタントです。
以下の機能を利用できます：
- タスク追加: 新しいタスクを追加
- タスク完了: タスクを完了にする（番号で指定）
- タスク一覧: 現在のタスク一覧を表示
- 日時取得: 現在の日時を取得
ユーザーの要求に応じて適切な機能を使用してください。"""

    history = [types.Content(role="user", parts=[types.Part(text=user_input)])]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=tools,
        ),
    )

    if not response.candidates or not response.candidates[0].content:
        return response.text or ""

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
        return final_response.text or ""

    return response.text or ""


class TestF3Integration:
    tools = [add_task, complete_task, list_tasks, get_current_datetime]

    def test_add_task_via_agent(self):
        result = run_single_turn("「メール返信」をタスクに追加して", self.tools)
        assert len(result) > 0, "応答が空"
        assert len(f3.TASKS) >= 1, f"タスクが追加されていない: {f3.TASKS}"

    def test_list_tasks_via_agent(self):
        f3.add_task("テスト用タスク")
        result = run_single_turn("タスクの一覧を見せて", self.tools)
        assert len(result) > 0, "応答が空"
