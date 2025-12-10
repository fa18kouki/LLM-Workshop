"""
演習A1: 入力された文から趣味を単語で抽出する（LangChain版）

【目標】
- LangChain を使って LLM を呼び出す基本を理解する
- PromptTemplate と Chain の概念を学ぶ

【実行方法】
uv run python practice/langchain_ver/a1.py

【ヒント】
- ChatGoogleGenerativeAI で Gemini モデルを使用
- PromptTemplate.from_template() でプロンプトテンプレートを作成
- chain = prompt | llm でチェーンを構築
"""

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# ========================================
# TODO: LLM を初期化してください
# ヒント: ChatGoogleGenerativeAI(model="gemini-2.5-flash")
# ========================================
llm = None  # ← ここを修正


def extract_hobby(input_text: str) -> str:
    """入力文から趣味を抽出する"""
    # ========================================
    # TODO: プロンプトテンプレートを作成してください
    # ヒント:
    #   PromptTemplate.from_template(
    #       "入力文から趣味を単語で抽出してください。\n入力文: {input_text}"
    #   )
    # ========================================
    prompt = None  # ← ここを修正

    # ========================================
    # TODO: チェーンを構築して実行してください
    # ヒント:
    #   chain = prompt | llm
    #   result = chain.invoke({"input_text": input_text})
    # ========================================
    chain = None  # ← ここを修正
    result = None  # ← ここを修正

    return result.content


if __name__ == "__main__":
    # テスト用の入力文
    test_inputs = [
        "私はサッカーを趣味にしています。",
        "休日はギターを弾いたり、映画を見たりしています。",
        "最近はプログラミングにハマっています。",
    ]

    for text in test_inputs:
        print(f"入力: {text}")
        result = extract_hobby(text)
        print(f"抽出結果: {result}")
        print("-" * 40)
