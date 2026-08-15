from pathlib import Path
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[3]

CHUNKS_FILE = (
    BASE_DIR
    / "knowledge_base"
    / "processed"
    / "chunks.json"
)

EMBEDDINGS_DIR = (
    BASE_DIR
    / "knowledge_base"
    / "embeddings"
)

EMBEDDINGS_FILE = (
    EMBEDDINGS_DIR
    / "embeddings.json"
)


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def generate_embeddings():

    EMBEDDINGS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Load all chunks
    chunks = json.loads(
        CHUNKS_FILE.read_text(
            encoding="utf-8"
        )
    )

    # Load already completed embeddings
    if EMBEDDINGS_FILE.exists():

        embedded_chunks = json.loads(
            EMBEDDINGS_FILE.read_text(
                encoding="utf-8"
            )
        )

    else:

        embedded_chunks = []

    completed_ids = {
        item["chunk_id"]
        for item in embedded_chunks
    }

    remaining_chunks = [
        chunk
        for chunk in chunks
        if chunk["chunk_id"] not in completed_ids
    ]

    print(f"Total chunks: {len(chunks)}")
    print(
        f"Already embedded: "
        f"{len(completed_ids)}"
    )
    print(
        f"Remaining: "
        f"{len(remaining_chunks)}"
    )

    for chunk in remaining_chunks:

        print(
            f"\nEmbedding: "
            f"{chunk['chunk_id']}"
        )

        try:

            result = client.models.embed_content(
                model="gemini-embedding-001",
                contents=chunk["text"],
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT"
                )
            )

            embedding = result.embeddings[0].values

            embedded_chunks.append({
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "text": chunk["text"],
                "embedding": embedding
            })

            # Save immediately
            EMBEDDINGS_FILE.write_text(
                json.dumps(
                    embedded_chunks,
                    ensure_ascii=False
                ),
                encoding="utf-8"
            )

            print("Saved successfully.")

        except Exception as e:

            print("\nEmbedding failed.")
            print(f"Error: {e}")

            print(
                "\nAlready completed embeddings "
                "have been safely saved."
            )

            break

    print("\n-----------------------------")
    print(
        f"Embeddings saved: "
        f"{len(embedded_chunks)}"
    )
    print(
        f"Remaining: "
        f"{len(chunks) - len(embedded_chunks)}"
    )
    print("-----------------------------")


if __name__ == "__main__":
    generate_embeddings()