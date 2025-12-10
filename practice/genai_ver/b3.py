"""
演習B3: ネストした構造化出力でカテゴリ別フィードバックを抽出しよう

【目標】
- ネストしたPydanticモデルの定義方法を学ぶ
- list[Model] 型で複数のオブジェクトを返す

【実行方法】
uv run python practice/genai_ver/b3.py

【ヒント】
- 内側のモデル（CategoryFeedback）を先に定義
- 外側のモデル（CommentAnalysis）で list[CategoryFeedback] を使用
"""

from typing import Literal

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel, Field

load_dotenv()

client = genai.Client()


class CategoryFeedback(BaseModel):
    """カテゴリ別のフィードバック"""

    # ========================================
    # TODO: 以下のフィールドを定義してください
    # - category: Literal["機能", "品質", "価格", "デザイン", "使い勝手"]
    # - positive_points: str
    # - negative_points: str
    # ========================================
    pass  # ← ここを修正


class CommentAnalysis(BaseModel):
    """コメントの総合分析結果"""

    # ========================================
    # TODO: 以下のフィールドを定義してください
    # - product_name: str
    # - categories: list[CategoryFeedback]
    # - overall_score: int (ge=1, le=5)
    # ========================================
    pass  # ← ここを修正


def analyze_comment_by_category(comment: str) -> CommentAnalysis:
    """コメントをカテゴリ別に分析する"""
    # ========================================
    # TODO: 構造化出力を使ってLLMを呼び出してください
    # ========================================
    response = None  # ← ここを修正
    return CommentAnalysis.model_validate_json(response.text)


if __name__ == "__main__":
    comment = """
エアポッズプロ第2世代を先週購入しました！まず驚いたのがノイズキャンセリング機能で、
通勤の地下鉄で使ってみたら騒音がほぼ完全に消えてびっくり。映画見る時の空間オーディオも
めちゃくちゃ臨場感あって最高です。音質もクリアで低音がしっかり出てる感じがいいですね。
デザインもシンプルで気に入ってて、ケースが小さいからポケットに入れやすいのも便利。
装着感も快適で、一日中つけてても耳が痛くならないし、タッチ操作も直感的で使いやすいです。

ただ正直39,800円は高いなぁって思います。もうちょっと安かったら文句なしなんですが。
あとバッテリー持ちが前のモデルから大して良くなってないみたいで、長時間使う時は
こまめに充電しないといけないのが面倒。雨の日に使ったら音飛びもちょっとあったし、
白だから指紋とか汚れが目立つのも気になります。あとiPhoneとMacで使い分けてるんですが、
ペアリングの切り替えが時々不安定でイライラすることも。

まぁトータルで見れば満足してるんですけど、値段とバッテリーのこと考えると
5点満点で4点かなって感じです。
"""

    print("=" * 60)
    print("カテゴリ別フィードバック分析（ネスト構造使用）")
    print("=" * 60)

    result = analyze_comment_by_category(comment)

    print(f"\n商品名: {result.product_name}")
    print(f"総合スコア: {result.overall_score}/5")
    print("\n--- カテゴリ別フィードバック ---")

    for feedback in result.categories:
        print(f"\n【{feedback.category}】")
        print(f"  ポジティブ: {feedback.positive_points}")
        print(f"  ネガティブ: {feedback.negative_points}")
