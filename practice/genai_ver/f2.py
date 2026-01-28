"""
演習F2: マルチツールエージェントのコードを読んで理解しよう

【目標】
- F1の2ツールから5ツールに拡張されたエージェントを読んで理解する
- ツールが増えても、エージェントループの実装が変わらないことを確認する
- LLMがどうやって5つのツールから適切なものを選択するかを理解する

【重要】
このコードは完成版です。実装する必要はありません。
F1のコードと比較しながら読んでください。

【実行方法】
uv run python practice/genai_ver/f2.py

【学習の進め方】
1. F1との違いを探しながらコードを読む
2. 実行して、ツールの自動選択を体験する
3. ファイル末尾の理解度チェックに答える
"""

import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

MEMO_DIR = Path("result/memos")
MEMO_DIR.mkdir(parents=True, exist_ok=True)


# ===========================================
# 既存ツール（F1と同じ）
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


# ===========================================
# 新しいツール: メモ管理（3つ追加）
#
# WHY: エージェントにツールを追加するとは、
#      「LLMができること」を増やすということです。
#      重要なのは、ツールを追加しても
#      エージェントループの実装は変わらないこと。
#      関数を定義してリストに追加するだけです。
#
# 注目: 各関数のdocstringが「LLMへの説明書」になります。
#       LLMはこれを読んで「いつこのツールを使うべきか」を判断します。
# ===========================================

def save_memo(title: str, content: str) -> dict[str, str]:
    """
    メモをファイルに保存する関数

    Args:
        title: メモのタイトル（ファイル名として使用）
        content: メモの内容

    Returns:
        保存結果を含む辞書
    """
    try:
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_"))
        if not safe_title:
            safe_title = "memo"
        file_path = MEMO_DIR / f"{safe_title}.txt"
        file_path.write_text(content, encoding="utf-8")
        return {"status": "success", "file_path": str(file_path), "title": title}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def read_memo(title: str) -> dict[str, str]:
    """
    保存されたメモを読み取る関数

    Args:
        title: メモのタイトル（ファイル名）

    Returns:
        メモの内容を含む辞書
    """
    try:
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_"))
        if not safe_title:
            return {"error": "タイトルが無効です", "content": None}
        file_path = MEMO_DIR / f"{safe_title}.txt"
        if not file_path.exists():
            return {"error": "メモが見つかりません", "content": None}
        content = file_path.read_text(encoding="utf-8")
        return {"content": content, "title": title}
    except Exception as e:
        return {"error": str(e), "content": None}


def list_memos() -> dict[str, list[str]]:
    """
    保存されているすべてのメモのタイトル一覧を取得する関数

    Returns:
        メモのタイトル一覧を含む辞書
    """
    try:
        memo_files = list(MEMO_DIR.glob("*.txt"))
        titles = [f.stem for f in memo_files]
        return {"titles": titles, "count": len(titles)}
    except Exception as e:
        return {"error": str(e), "titles": []}


def run_agent():
    """メモ機能付きエージェントを実行"""

    # ===========================================
    # 5つのツールをリストに追加
    #
    # WHY: F1では2つだったツールが5つに。
    #      しかし、ツールを増やすために必要な変更は
    #      「関数を定義してこのリストに追加する」だけです。
    #      エージェントループのコードは一切変わりません。
    #      これがエージェントの拡張性です。
    # ===========================================
    tools = [calculate, save_memo, read_memo, list_memos, get_current_datetime]

    history = []

    system_instruction = """あなたは親切なアシスタントです。
以下の機能を利用できます：
- 計算: 数式を計算できます
- メモ: メモを保存・読み取りできます
- 日時: 現在の日時を取得できます

ユーザーの要求に応じて、適切な機能を使用してください。
機能を使用した後は、結果をわかりやすく説明してください。"""

    print("=" * 60)
    print("メモ機能付きエージェント")
    print("=" * 60)
    print("\n利用可能な機能:")
    print("  - 計算（例: 「3 + 5 * 2を計算して」）")
    print("  - メモ保存（例: 「買い物リストをメモに保存: りんご、バナナ」）")
    print("  - メモ読み取り（例: 「買い物リストのメモを読んで」）")
    print("  - メモ一覧（例: 「保存されているメモの一覧を教えて」）")
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
            # --- STEP 1〜4はF1と全く同じ構造 ---
            # ツールが2個でも5個でも、このコードは変わりません。

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
# 理解度チェック（F1と比較しながら答えてください）
# ========================================
#
# Q1. F1とF2で、エージェントループの実装は変わりましたか？
#     変わった部分と変わらない部分を挙げてください。
#
# Q2. LLMはどうやって5つのツールから適切なものを選んでいますか？
#     save_memo と read_memo の docstring を見てみてください。
#     LLMはこれをどう活用していますか？
#
# Q3. 新しいツール delete_memo を追加したい場合、
#     何を変更すれば良いですか？
#     エージェントループの処理を変更する必要はありますか？
#
# Q4. 「買い物リストをメモして: りんご、バナナ」という入力から、
#     LLMはどうやって title="買い物リスト", content="りんご、バナナ"
#     と引数を分けていますか？
#
# Q5. 演習Cでは「評価→修正」の順序を我々が決めました。
#     F2では「メモ保存→メモ読み取り」の順序を誰が決めていますか？
#
# ========================================
# 実験してみよう
# ========================================
#
# 1. 「買い物リストをメモして: りんご、バナナ、牛乳」と入力
#    → どのツールが実行されますか？
#
# 2. 「買い物リストを読んで」と入力
#    → 別のツールが選ばれることを確認
#
# 3. 「保存されているメモは？」と入力
#    → さらに別のツールが選ばれることを確認
#
# 4. 「3 + 5を計算して」と入力
#    → メモとは無関係のツールが選ばれることを確認
#
# LLMが「入力内容に応じてツールを使い分けている」ことを
# 実感してください。
# ========================================
