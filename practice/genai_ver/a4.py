"""
演習A4: 連続的な対話の履歴を管理しよう

【目標】
- 会話履歴（コンテキスト）の管理方法を理解する
- LLMには毎回全ての会話履歴が送られていることを体験する
- システムプロンプトの役割を理解する

【実行方法】
uv run python practice/genai_ver/a4.py

【ヒント】
- types.Content で役割（role）と内容（parts）を指定
- role: "user" または "model"
- system_instruction でシステムプロンプトを設定
"""

from google import genai
from google.genai import types

client = genai.Client()


def chat():
    """対話型チャット"""
    # ========================================
    # TODO: 会話履歴を保持するリストを作成
    # ========================================
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

        # ========================================
        # TODO: ユーザーの入力を履歴に追加
        # ヒント:
        #   types.Content(role="user", parts=[types.Part(text=user_input)])
        # ========================================

        # ========================================
        # TODO: LLM に会話履歴を送信して応答を取得
        # ヒント:
        #   client.models.generate_content(
        #       model="gemini-2.5-flash-lite",
        #       contents=history,
        #       config=types.GenerateContentConfig(
        #           system_instruction="必ず日本語で応答してください。"
        #       ),
        #   )
        # ========================================
        response = None  # ← ここを修正

        print(f"AI: {response.text}")

        # ========================================
        # TODO: AI の応答を履歴に追加
        # ヒント:
        #   types.Content(role="model", parts=[types.Part(text=response.text)])
        # ========================================

        # デバッグ: 現在の履歴の長さを表示
        print(f"[デバッグ] 現在の履歴数: {len(history)} メッセージ")


if __name__ == "__main__":
    chat()
