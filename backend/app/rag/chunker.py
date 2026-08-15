from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parents[3]

PROCESSED_DIR = BASE_DIR / "knowledge_base" / "processed"

CHUNKS_FILE = PROCESSED_DIR / "chunks.json"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def create_chunks(text: str):
    """Split text into chunks with overlap."""

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + CHUNK_SIZE

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def process_text_files():

    txt_files = list(PROCESSED_DIR.glob("*.txt"))

    print(f"Found {len(txt_files)} text files.")

    all_chunks = []

    for txt_file in txt_files:

        print(f"\nProcessing: {txt_file.name}")

        text = txt_file.read_text(
            encoding="utf-8"
        )

        chunks = create_chunks(text)

        print(f"Created {len(chunks)} chunks.")

        source_name = txt_file.stem

        for index, chunk in enumerate(chunks, start=1):

            chunk_data = {
                "chunk_id": f"{source_name}_{index:03d}",
                "source": f"{source_name}.pdf",
                "text": chunk
            }

            all_chunks.append(chunk_data)

    # Save all chunks
    CHUNKS_FILE.write_text(
        json.dumps(
            all_chunks,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("\n-----------------------------")
    print(f"Total chunks saved: {len(all_chunks)}")
    print(f"Saved to: {CHUNKS_FILE}")
    print("-----------------------------")


if __name__ == "__main__":
    process_text_files()