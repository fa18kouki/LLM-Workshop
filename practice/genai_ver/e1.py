"""
演習E1: Embeddingで類似度を計算しよう

【目標】
- テキストのEmbedding（ベクトル化）を学ぶ
- コサイン類似度による類似性の計算

【実行方法】
uv run python practice/genai_ver/e1.py

【ヒント】
- client.models.embed_content でEmbeddingを取得
- numpy を使ってコサイン類似度を計算
"""

from google import genai
from google.genai import types
import numpy as np

client = genai.Client()


def get_embeddings(texts: list[str]) -> list[np.ndarray]:
    """テキストのEmbeddingを取得する"""
    # ========================================
    # TODO: Embeddingを取得してください
    # ヒント:
    #   result = client.models.embed_content(
    #       model="text-multilingual-embedding-002",
    #       contents=texts,
    #       config=types.EmbedContentConfig(
    #           task_type="SEMANTIC_SIMILARITY",
    #       ),
    #   )
    #   return [np.array(emb.values) for emb in result.embeddings]
    # ========================================
    result = None  # ← ここを修正
    return [np.array(emb.values) for emb in result.embeddings]


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """コサイン類似度を計算する"""
    # ========================================
    # TODO: コサイン類似度を計算してください
    # ヒント:
    #   normed1 = vec1 / np.linalg.norm(vec1)
    #   normed2 = vec2 / np.linalg.norm(vec2)
    #   return np.dot(normed1, normed2)
    # ========================================
    pass  # ← ここを修正


if __name__ == "__main__":
    target_texts = ["漫画", "アニメ", "サッカー"]

    print("=" * 60)
    print("Embedding（類似度計算）")
    print("=" * 60)

    embeddings = get_embeddings(target_texts)

    for i, (text, emb) in enumerate(zip(target_texts, embeddings)):
        print(f"{text}: {emb[:5]}...（{len(emb)}次元）")

    print("\n--- 類似度 ---")
    for i in range(len(target_texts)):
        for j in range(i + 1, len(target_texts)):
            similarity = cosine_similarity(embeddings[i], embeddings[j])
            print(f"{target_texts[i]} vs {target_texts[j]}: {similarity:.4f}")
