"""
演習D1: 画像入力でマルチモーダルを体験しよう（回答）

【実行方法】
uv run python src/genai_ver/d1.py
"""

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()


def describe_image(image_path: str) -> str:
    """画像の内容を説明する"""
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            "画像の内容を説明してください",
        ],
    )

    return response.text


if __name__ == "__main__":
    image_path = "data/sample_image.png"

    print("=" * 60)
    print("画像認識（マルチモーダル）")
    print("=" * 60)

    result = describe_image(image_path)
    print(f"\n画像パス: {image_path}")
    print(f"\n説明:\n{result}")
