"""演習F1 解答コードの統合テスト（API呼び出し含む）

エージェントループを1ターンだけ実行し、
Function Callingが正しく動作するかを確認する。
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from google import genai
from google.genai import types
from genai_ver.f1 import calculate, get_current_datetime


client = genai.Client()


def run_single_turn(user_input: str, tools: list) -> str:
    """エージェントの1ターンを実行し、最終テキスト応答を返す"""
    system_instruction = """あなたは親切なアシスタントです。
以下の機能を利用できます：
- 計算: 数式を計算できます
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


class TestF1Integration:
    tools = [calculate, get_current_datetime]

    def test_calculate_via_agent(self):
        result = run_single_turn("3 + 5 * 2を計算して", self.tools)
        assert "13" in result, f"期待: '13' を含む応答, 実際: {result}"

    def test_datetime_via_agent(self):
        result = run_single_turn("今日は何曜日？", self.tools)
        weekdays = ["月", "火", "水", "木", "金", "土", "日"]
        assert any(w in result for w in weekdays), f"曜日が含まれていない: {result}"

    def test_normal_chat(self):
        result = run_single_turn("こんにちは", self.tools)
        assert len(result) > 0, "応答が空"
