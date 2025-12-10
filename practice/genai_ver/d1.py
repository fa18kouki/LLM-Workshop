"""
演習D1: 画像入力でマルチモーダルを体験しよう

【目標】
- マルチモーダル入力（テキスト + 画像）の方法を学ぶ
- Part.from_bytes を使った画像の送信

【実行方法】
uv run python practice/genai_ver/d1.py

【ヒント】
- types.Part.from_bytes で画像データをPartに変換
- contents にリストで複数のPartを渡せる
"""

from google import genai
from google.genai import types

client = genai.Client()


def describe_image(image_path: str) -> str:
    """画像の内容を説明する"""
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # ========================================
    # TODO: 画像とテキストを含むcontentsでLLMを呼び出す
    # ヒント:
    #   response = client.models.generate_content(
    #       model="gemini-2.5-flash",
    #       contents=[
    #           types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
    #           "画像の内容を説明してください",
    #       ],
    #   )
    # ========================================
    response = None  # ← ここを修正

    return response.text


if __name__ == "__main__":
    image_path = "data/sample_image.png"

    print("=" * 60)
    print("画像認識（マルチモーダル）")
    print("=" * 60)

    result = describe_image(image_path)
    print(f"\n画像パス: {image_path}")
    print(f"\n説明:\n{result}")
