"""
演習B1: 構造化出力（Structured Output）で感情分析しよう（回答）

【実行方法】
uv run python src/genai_ver/b1.py
"""

from typing import Literal

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel, Field

load_dotenv()

client = genai.Client()


class CommentAnalysis(BaseModel):
    """コメントの感情分析結果"""

    sentiment: Literal["positive", "very positive", "negative", "very negative", "neutral"] = Field(
        description="判定結果。positive: ポジティブ、very positive: 非常にポジティブ、negative: ネガティブ、very negative: 非常にネガティブ、neutral: ニュートラル"
    )


def analyze_sentiment(comment: str, temperature: float = 0.5) -> CommentAnalysis:
    """コメントの感情を分析する

    Args:
        comment: 分析対象のコメント
        temperature: 温度パラメータ（0.0-2.0）
                    低い値（0.0-0.5）: 一貫性のある決定的な出力
                    中程度の値（0.5-1.0）: バランスの取れた出力
                    高い値（1.0-2.0）: 多様で創造的な出力
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""次のコメントがポジティブかネガティブかニュートラルか判定してください。
# コメント
```
{comment}
```
""",
        config=GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CommentAnalysis,
            temperature=temperature,
        ),
    )
    return CommentAnalysis.model_validate_json(response.text)


if __name__ == "__main__":
    # テスト用コメント（ニュアンスが複雑で判断が難しいものを選ぶと違いがわかりやすい）
    test_comment = """この商品を使ってみた感想ですが、全体的に作りはしっかりしており、デザインも気に入っています。ただし、説明書が不親切で使い始めるまでに少し時間がかかりました。また、音も少し大きめなので、夜間の使用には向かないかもしれません。それでも価格に対して十分な価値はあると思いますし、友人にもおすすめできます。"""

    # 異なるtemperature値で比較
    temperature_values = [0.0, 0.5, 1.0, 1.5, 2.0]

    print("=" * 70)
    print("Temperatureパラメータによる出力の違いの比較")
    print("=" * 70)
    print(f"\n対象レビュー:")
    print("-" * 70)
    print(test_comment)
    print("-" * 70)

    results = {}
    for temp in temperature_values:
        # 同じ条件で5回ずつ実行して結果のばらつきを確認
        temp_results = []
        for i in range(5):
            result = analyze_sentiment(test_comment, temperature=temp)
            temp_results.append(result.sentiment)

        results[temp] = temp_results

        # 結果の統計を計算
        result_counts = {}
        for r in temp_results:
            result_counts[r] = result_counts.get(r, 0) + 1

        print(f"\nTemperature: {temp}")
        print(f"  説明: ", end="")
        if temp <= 0.3:
            print("非常に決定的（一貫性重視）")
        elif temp <= 0.7:
            print("やや決定的（バランス重視）")
        elif temp <= 1.2:
            print("標準（ある程度の多様性）")
        else:
            print("創造的（多様性重視）")

        print(f"  5回の実行結果: {', '.join(temp_results)}")
        print(f"  結果の分布: ", end="")
        print(", ".join([f"{k}: {v}回" for k, v in result_counts.items()]))
        print(f"  結果の一貫性: {'非常に高い' if len(set(temp_results)) == 1 else '高い' if len(set(temp_results)) == 2 else '中程度' if len(set(temp_results)) == 3 else '低い'}")
        print("-" * 70)

    # まとめ
    print("\n" + "=" * 60)
    print("まとめ")
    print("=" * 60)
    print("- Temperatureが低い（0.0-0.5）: 同じ入力に対して常に同じ結果が出やすい")
    print("- Temperatureが高い（1.0-2.0）: 同じ入力でも異なる結果が出やすい")
    print("- 感情分析のような分類タスクでは、低いTemperatureが推奨される")
    print("=" * 60)
