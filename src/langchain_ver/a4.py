"""
演習A4: 連続的な対話の履歴を管理しよう（LangChain版 回答）

【実行方法】
uv run python src/langchain_ver/a4.py
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")


def chat():
    """対話型チャット"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "必ず日本語で応答してください。"),
            MessagesPlaceholder(variable_name="history"),
        ]
    )
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

        # ユーザーの入力を履歴に追加
        history.append(HumanMessage(content=user_input))

        # LLM に会話履歴を送信
        response = chain.invoke({"history": history})

        print(f"AI: {response}")

        # AI の応答を履歴に追加
        history.append(AIMessage(content=response))

        # デバッグ: 現在の履歴の長さを表示
        print(f"[デバッグ] 現在の履歴数: {len(history)} メッセージ")


if __name__ == "__main__":
    chat()
