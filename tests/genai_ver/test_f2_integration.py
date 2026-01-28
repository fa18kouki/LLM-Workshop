"""演習F2 解答コードの統合テスト（API呼び出し含む）

メモ機能付きエージェントが正しくFunction Callingで
メモの保存・読み取りを行えるかを確認する。
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
from genai_ver.f2 import (
    calculate, get_current_datetime,
    save_memo, read_memo, list_memos,
    MEMO_DIR,
)

client = genai.Client()


@pytest.fixture(autouse=True)
def cleanup_test_memos():
    """テスト用メモを削除"""
    yield
    for f in MEMO_DIR.glob("*.txt"):
        if "integration" in f.stem.lower() or "test" in f.stem.lower():
            f.unlink(missing_ok=True)


def run_single_turn(user_input: str, tools: list) -> str:
    """エージェントの1ターンを実行"""
    system_instruction = """あなたは親切なアシスタントです。
以下の機能を利用できます：
- 計算: 数式を計算できます
- メモ: メモを保存・読み取りできます
- 日時: 現在の日時を取得できます
ユーザーの要求に応じて、適切な機能を使用してください。"""

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


class TestF2Integration:
    tools = [calculate, save_memo, read_memo, list_memos, get_current_datetime]

    def test_save_memo_via_agent(self):
        result = run_single_turn(
            "「integration test」というタイトルで「テスト内容です」とメモに保存して",
            self.tools,
        )
        assert len(result) > 0, "応答が空"
        # メモファイルが作成されたか確認
        memo_files = list(MEMO_DIR.glob("*integration*"))
        assert len(memo_files) >= 1, f"メモファイルが作成されていない: {list(MEMO_DIR.glob('*.txt'))}"

    def test_calculate_via_agent(self):
        result = run_single_turn("100 / 4 を計算して", self.tools)
        assert "25" in result, f"期待: '25' を含む応答, 実際: {result}"
