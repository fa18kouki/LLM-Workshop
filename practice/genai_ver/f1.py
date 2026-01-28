"""
演習F1: 基本エージェントのコードを読んで理解しよう

【目標】
- 動作するエージェントのコードを読んで、仕組みを理解する
- エージェントループ（判断 → 実行 → 返却 → 最終回答）がどこにあるか特定する
- なぜ generate_content を2回呼ぶのかを説明できるようになる

【重要】
このコードは完成版です。実装する必要はありません。
コードを読み、実行し、末尾の「理解度チェック」に答えてください。

【実行方法】
uv run python practice/genai_ver/f1.py

【学習の進め方】
1. コード全体を読む（特に「STEP 1〜4」のコメントに注目）
2. 実行して動作を確認する
3. ファイル末尾の理解度チェックに答える
"""

import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()


# ===========================================
# エージェントの構成要素: ツール関数
#
# WHY: LLMは「考える」ことはできますが、計算や日時取得など
#      外部の情報にアクセスすることはできません。
#      そこで、LLMの代わりに実行する「ツール」を関数として定義します。
#      LLMは関数名・引数・docstringを読んで
#      「このツールで何ができるか」を理解します。
# ===========================================

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
        # NOTE: 研修用の簡易実装。本番環境では安全な数式パーサーを使うこと
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

    # ===========================================
    # ツールのリスト
    # WHY: このリストをLLMに渡すことで、
    #      LLMは「自分が使えるツール」を把握します。
    #      我々は「どの入力でどのツールを使うか」を
    #      if文で書く必要はありません。LLMが自分で判断します。
    # ===========================================
    tools = [calculate, get_current_datetime]

    # ===========================================
    # 会話履歴
    # WHY: LLMは1回の呼び出しで前の会話を覚えていません。
    #      毎回、会話の全履歴を渡す必要があります。
    # ===========================================
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
            # ===========================================
            # STEP 1: LLMにツール情報を渡して呼び出す
            #
            # WHY: tools=tools を渡すことで、LLMは
            #      「calculate と get_current_datetime が使える」
            #      と知り、ユーザーの要求に応じて
            #      適切なツールを自分で選択できます。
            # ===========================================
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
                    # ===========================================
                    # STEP 2: LLMの判断を確認する
                    #
                    # WHY: LLMの応答には2種類あります:
                    #   a) function_call → 「このツールを使いたい」という判断
                    #   b) テキスト → 「ツール不要、直接回答する」という判断
                    #
                    # ここが演習Cとの決定的な違いです。
                    # 演習Cでは我々がif文で処理を分岐しましたが、
                    # エージェントではLLMが自律的に判断します。
                    # ===========================================
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

                        # ===========================================
                        # STEP 3: ツールを実行する
                        #
                        # WHY: LLMは「calculateを使いたい」と判断しますが、
                        #      実際に計算を実行することはできません。
                        #      我々のプログラムがツールを実行し、
                        #      結果をLLMに「報告」します。
                        # ===========================================
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

                # ===========================================
                # STEP 4: ツール実行結果をLLMに返し、最終回答を生成する
                #
                # WHY: ツール実行結果（例: {"result": "13"}）だけでは
                #      ユーザーに不親切です。
                #      LLMに結果を渡して「人間にわかりやすい回答」を
                #      作ってもらいます。
                #
                #      これが generate_content を2回呼ぶ理由です:
                #        1回目 → LLMが「どのツールを使うか」を判断
                #        2回目 → ツール結果を見て最終回答を生成
                # ===========================================
                if function_calls and function_results_list:
                    # LLMの判断（function_call）を履歴に記録
                    history.append(types.Content(
                        role="model",
                        parts=[types.Part(function_call=fc) for fc in function_calls],
                    ))
                    # ツール実行結果を履歴に追加
                    history.append(types.Content(
                        role="user",
                        parts=function_results_list,
                    ))
                    # 2回目のLLM呼び出し: 結果を見て最終回答を生成
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
                    # ツール不要の場合: LLMが直接テキストで回答
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
# 理解度チェック（コードを読んで答えてください）
# ========================================
#
# Q1. エージェントループの4ステップ（STEP 1〜4）は
#     それぞれ何をしていますか？自分の言葉で説明してください。
#
# Q2. なぜ generate_content を2回呼んでいますか？
#     1回目と2回目で、LLMに渡す情報はどう変わっていますか？
#
# Q3. 「3 + 5 * 2を計算して」と入力したとき、
#     LLMはどうやって calculate ツールを選んでいますか？
#     我々が if "計算" in user_input のような条件を書いていないのに、
#     なぜ正しく選べるのでしょうか？
#
# Q4. 「おはよう」と入力したとき、ツールは実行されますか？
#     実行して確認し、なぜそうなるか考えてください。
#
# Q5. もし tools=None にしたら何が起こりますか？
#     LLMは「ツールが使える」ことを知らないとどうなるでしょう？
#
# Q6. 演習Cでは処理の順番を我々が決めていました。
#     この演習Fでは、誰が「何をするか」を決めていますか？
#
# ========================================
# 実行して確認しよう
# ========================================
#
# 1. 「3 + 5 * 2を計算して」と入力
#    → [ツール実行] が表示されるか確認
#
# 2. 「今何時？」と入力
#    → 別のツールが選ばれることを確認
#
# 3. 「おはよう」と入力
#    → ツールを使わない応答を確認
#
# この3つの動作から「LLMが自律的に判断している」ことを
# 実感してください。
# ========================================
