"""
演習A4: 連続的な対話の履歴を管理しよう（LangChain版）

【目標】
- LangChain での会話履歴管理方法を学ぶ
- MessagesPlaceholder を使った履歴の渡し方

【実行方法】
uv run python practice/langchain_ver/a4.py

【ヒント】
- MessagesPlaceholder(variable_name="history") でプレースホルダー作成
- HumanMessage / AIMessage で履歴を構築
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")


def chat():
    """対話型チャット"""
    # ========================================
    # TODO: プロンプトテンプレートを作成
    # ヒント:
    #   prompt = ChatPromptTemplate.from_messages(
    #       [
    #           ("system", "必ず日本語で応答してください。"),
    #           MessagesPlaceholder(variable_name="history"),
    #       ]
    #   )
    # ========================================
    prompt = None  # ← ここを修正
    chain = prompt | llm | StrOutputParser()

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
        # ヒント: history.append(HumanMessage(content=user_input))
        # ========================================

        # ========================================
        # TODO: LLM に会話履歴を送信
        # ヒント: response = chain.invoke({"history": history})
        # ========================================
        response = None  # ← ここを修正

        print(f"AI: {response}")

        # ========================================
        # TODO: AI の応答を履歴に追加
        # ヒント: history.append(AIMessage(content=response))
        # ========================================

        # デバッグ: 現在の履歴の長さを表示
        print(f"[デバッグ] 現在の履歴数: {len(history)} メッセージ")


if __name__ == "__main__":
    chat()
