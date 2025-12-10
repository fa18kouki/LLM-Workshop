"""
演習C3: 修正・評価のループを回そう（回答）

【実行方法】
uv run python src/genai_ver/c3.py
"""

import asyncio

from c1 import evaluate_article
from c2 import revise_article


async def revision_loop(article: str, max_iterations: int = 3):
    """修正・評価ループ"""

    print("=== 記事の修正・評価ループを開始 ===")

    current_article = article

    for iteration in range(1, max_iterations + 1):
        print(f"【第{iteration}回目の評価】")

        # 評価
        evaluation = await evaluate_article(current_article)
        print(evaluation.model_dump_json(indent=2))

        # いずれかの評価軸で修正が必要かチェック
        needs_revision = (
            evaluation.technical_accuracy.needs_revision
            or evaluation.clarity.needs_revision
            or evaluation.structure.needs_revision
            or evaluation.seo.needs_revision
        )

        print(f"総合判定: {'修正必要' if needs_revision else '修正不要'}")

        # 修正が不要ならループを抜ける
        if not needs_revision:
            print("記事の品質が十分なレベルに達しました。ループを終了します。")
            break

        # 修正が必要な場合
        print(f"  → 記事を修正します...")
        revision = revise_article(current_article, evaluation)

        print(f"【第{iteration}回目の修正完了】")
        print("  主な変更点:")
        for i, change in enumerate(revision.changes_summary, 1):
            print(f"    {i}. {change}")
        print()

        # 次の評価のために修正版を保存
        current_article = revision.revised_article

        # 各イテレーションの結果を保存（オプション）
        with open(f"result/revised_article_iter{iteration}.md", "w") as f:
            f.write(current_article)
    else:
        # forループが正常終了（breakせずに終了）した場合
        print(f"最大反復回数（{max_iterations}回）に達しました。")

    # 最終版を保存
    with open("result/revised_article_final.md", "w") as f:
        f.write(current_article)

    print(f"=== ループ完了 ===")
    print("最終版を result/revised_article_final.md に保存しました。")

    return current_article


if __name__ == "__main__":
    # 評価対象の記事を読み込み
    with open("data/bad_quality_article.md") as f:
        article = f.read()

    # 修正・評価ループを実行
    asyncio.run(revision_loop(article, max_iterations=3))
