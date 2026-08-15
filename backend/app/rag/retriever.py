from pathlib import Path
import json

import numpy as np
from dotenv import load_dotenv
from google import genai


load_dotenv()


# Project root
BASE_DIR = Path(__file__).resolve().parents[3]

EMBEDDINGS_FILE = (
    BASE_DIR
    / "knowledge_base"
    / "embeddings"
    / "embeddings.json"
)


# Gemini client
import os

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors.
    """

    a = np.array(vector_a)
    b = np.array(vector_b)

    denominator = (
        np.linalg.norm(a)
        * np.linalg.norm(b)
    )

    if denominator == 0:
        return 0

    return np.dot(a, b) / denominator


def retrieve_relevant_chunks(
    query: str,
    top_k: int = 3
):
    """
    Find the most relevant knowledge-base chunks
    for a user query.
    """

    # Load embeddings
    if not EMBEDDINGS_FILE.exists():
        raise FileNotFoundError(
            "embeddings.json not found."
        )

    embedded_chunks = json.loads(
        EMBEDDINGS_FILE.read_text(
            encoding="utf-8"
        )
    )

    # Create embedding for user query
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )

    query_embedding = (
        result.embeddings[0].values
    )

    # Calculate similarity
    results = []

    for chunk in embedded_chunks:

        score = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        results.append({
            "chunk_id": chunk["chunk_id"],
            "source": chunk["source"],
            "text": chunk["text"],
            "score": float(score)
        })

    # Highest similarity first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":

    question = input(
        "\nAsk a question: "
    )

    results = retrieve_relevant_chunks(
        question,
        top_k=3
    )

    print("\n==============================")
    print("TOP RELEVANT CHUNKS")
    print("==============================")

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\nResult {index}"
        )

        print(
            f"Source: {result['source']}"
        )

        print(
            f"Score: {result['score']:.4f}"
        )

        print(
            f"Chunk ID: {result['chunk_id']}"
        )

        print(
            f"\n{result['text'][:1000]}"
        )