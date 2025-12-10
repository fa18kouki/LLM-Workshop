"""
演習E1: Embeddingで類似度を計算しよう（LangChain版 回答）

【実行方法】
uv run python src/langchain_ver/e1.py
"""

import numpy as np
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def get_embeddings(texts: list[str]) -> list[np.ndarray]:
    """テキストのEmbeddingを取得する"""
    model = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
    )
    results = model.embed_documents(texts)
    return [np.array(emb) for emb in results]


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """コサイン類似度を計算する"""
    normed1 = vec1 / np.linalg.norm(vec1)
    normed2 = vec2 / np.linalg.norm(vec2)
    return np.dot(normed1, normed2)


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
