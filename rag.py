
import json
import numpy as np
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

DOCS_DIR = Path(__file__).resolve().parent / "maintenance_docs"
INDEX_PATH = Path(__file__).resolve().parent / "rag_index.json"

EMBEDDING_MODEL = "text-embedding-3-small"


def load_documents():
    documents = []

    for path in sorted(DOCS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")

        documents.append({
            "source": path.name,
            "text": text
        })

    return documents


def create_embedding(text):
    load_dotenv()
    response = OpenAI().embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


def build_index():
    documents = load_documents()
    indexed_documents = []

    for document in documents:
        embedding = create_embedding(document["text"])

        indexed_documents.append({
            "source": document["source"],
            "text": document["text"],
            "embedding": embedding
        })

        print(f"Indexed: {document['source']}")

    INDEX_PATH.write_text(
        json.dumps(indexed_documents),
        encoding="utf-8"
    )

    print(f"Saved {len(indexed_documents)} documents.")


def cosine_similarity(left, right):
    left = np.array(left, dtype=float)
    right = np.array(right, dtype=float)

    denominator = np.linalg.norm(left) * np.linalg.norm(right)

    if denominator == 0:
        return 0.0

    return float(np.dot(left, right) / denominator)


def search_maintenance_documents(query, top_k=3):
    if not INDEX_PATH.exists():
        raise FileNotFoundError(
            "RAG index missing. Run python rag.py first."
        )

    documents = json.loads(
        INDEX_PATH.read_text(encoding="utf-8")
    )

    query_embedding = create_embedding(query)

    results = []

    for document in documents:
        score = cosine_similarity(
            query_embedding,
            document["embedding"]
        )

        results.append({
            "source": document["source"],
            "score": round(score, 4),
            "text": document["text"]
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]


def get_maintenance_procedure(alarm_code):
    alarm_code = alarm_code.strip().upper()

    allowed_codes = {
        "TEMP_HIGH",
        "SENSOR_FAULT",
        "PRESSURE_LOW",
        "MOTOR_ERROR",
        "COMM_ERROR"
    }

    if alarm_code not in allowed_codes:
        return {
            "found": False,
            "message": "Unknown alarm code"
        }

    document_path = DOCS_DIR / f"{alarm_code}.md"

    if not document_path.exists():
        return {
            "found": False,
            "message": f"No SOP found for {alarm_code}"
        }

    return {
        "found": True,
        "source": document_path.name,
        "text": document_path.read_text(encoding="utf-8")
    }


if __name__ == "__main__":
    build_index()
