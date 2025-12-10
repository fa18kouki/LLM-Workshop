"""
演習D3: コード実行ツールを使おう

【目標】
- Gemini の組み込みツール（Code Execution）の使い方を学ぶ
- LLMが生成・実行したコードと結果の取得

【実行方法】
uv run python practice/genai_ver/d3.py

【ヒント】
- types.Tool(code_execution=types.ToolCodeExecution) でツールを定義
- 実行されたコードと画像は response.candidates[0].content.parts から取得
"""

from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()


def execute_code_with_llm(prompt: str) -> str:
    """LLMにコードを生成・実行させる"""
    # ========================================
    # TODO: コード実行ツールを使ってLLMを呼び出す
    # ヒント:
    #   response = client.models.generate_content(
    #       model="gemini-2.5-flash",
    #       contents=prompt,
    #       config=types.GenerateContentConfig(
    #           tools=[types.Tool(code_execution=types.ToolCodeExecution)]
    #       ),
    #   )
    # ========================================
    response = None  # ← ここを修正
    return response


if __name__ == "__main__":
    prompt = "matplotlibを使ったPythonコードを生成して実行し、y=x^2のグラフを出力してください。"

    print("=" * 60)
    print("コード実行ツール使用")
    print("=" * 60)

    response = execute_code_with_llm(prompt)
    print(f"\n回答:\n{response.text}")

    # 画像とコードを保存
    result_dir = Path("result")
    result_dir.mkdir(parents=True, exist_ok=True)

    code_count = 0
    image_count = 0

    for candidate in response.candidates:
        for part in candidate.content.parts:
            # 実行されたコードを保存
            if hasattr(part, "executable_code") and part.executable_code:
                code = part.executable_code.code
                code_path = result_dir / f"code_{code_count:03d}.py"
                code_path.write_text(code, encoding="utf-8")
                print(f"\nコードを保存: {code_path}")
                code_count += 1

            # 画像を保存
            if hasattr(part, "inline_data") and part.inline_data:
                if part.inline_data.mime_type.startswith("image/"):
                    ext = part.inline_data.mime_type.split("/")[-1]
                    image_path = result_dir / f"image_{image_count:03d}.{ext}"
                    image_path.write_bytes(part.inline_data.data)
                    print(f"画像を保存: {image_path}")
                    image_count += 1
