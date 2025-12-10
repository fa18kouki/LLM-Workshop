"""
演習D1: 画像入力でマルチモーダルを体験しよう（LangChain版 回答）

【実行方法】
uv run python src/langchain_ver/d1.py
"""

import base64

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def describe_image(image_path: str) -> str:
    """画像の内容を説明する"""
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "human",
                [
                    {
                        "type": "text",
                        "text": "画像の内容を説明してください。",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": "data:{file_type};base64,{base64_data}"},
                    },
                ],
            ),
        ]
    )
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke(
        {
            "file_type": "image/png",
            "base64_data": base64.b64encode(image_bytes).decode("utf-8"),
        }
    )
    return result


if __name__ == "__main__":
    image_path = "data/sample_image.png"

    print("=" * 60)
    print("画像認識（マルチモーダル）")
    print("=" * 60)

    result = describe_image(image_path)
    print(f"\n画像パス: {image_path}")
    print(f"\n説明:\n{result}")
