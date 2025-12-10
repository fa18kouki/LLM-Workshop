"""
演習E3: LangChainのエージェントを使おう（回答）

【実行方法】
uv run python src/langchain_ver/e3.py
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool


@tool
def func_bird(input_str: str) -> str:
    """鳥に関する質問に答える"""
    print("called func_bird")
    return "それは鳥です。"


@tool
def func_add(a: int, b: int) -> int:
    """足し算をする"""
    print("called func_add")
    return a + b


@tool
def func_mul(a: int, b: int) -> int:
    """掛け算をする"""
    print("called func_mul")
    return a * b


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
tools = [func_bird, func_add, func_mul]

# プロンプトテンプレートを作成
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "あなたは親切なアシスタントです。"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# エージェントを作成
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


if __name__ == "__main__":
    print("=" * 60)
    print("LangChain エージェント")
    print("=" * 60)

    print("\n--- 質問1: 鳥について ---")
    result = agent_executor.invoke({"input": "ハトについて教えて"})
    print(f"回答: {result['output']}")

    print("\n--- 質問2: 計算 ---")
    result = agent_executor.invoke(
        {"input": "3と4を足した値に1+3を足した値同士を掛け算するとどうなる？"}
    )
    print(f"回答: {result['output']}")
