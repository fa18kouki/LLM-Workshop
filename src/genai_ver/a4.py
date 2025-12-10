"""
演習A4: 連続的な対話の履歴を管理しよう（回答）

【実行方法】
uv run python src/genai_ver/a4.py
"""

from google import genai
from google.genai import types

client = genai.Client()


def chat():
    """対話型チャット"""
    history = []

    print("=" * 60)
    print("対話型チャット（終了するには 'exit' と入力）")
    print("※ 会話履歴が正しく機能しているか確認してみよう")
    print("  例: 「私の名前は太郎です」→「私の名前は何ですか？」")
    print("=" * 60)

    while True:
        user_input = input("\nあなた: ")

        if user_input.lower() == "exit":
            print("チャットを終了します。")
            break

        # ユーザーの入力を履歴に追加
        history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))

        # LLM に会話履歴を送信
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction="必ず日本語で応答してください。"
            ),
        )

        print(f"AI: {response.text}")

        # AI の応答を履歴に追加
        history.append(types.Content(role="model", parts=[types.Part(text=response.text)]))

        # デバッグ: 現在の履歴の長さを表示
        print(f"[デバッグ] 現在の履歴数: {len(history)} メッセージ")


if __name__ == "__main__":
    chat()
