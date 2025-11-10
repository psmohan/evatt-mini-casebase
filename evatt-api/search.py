import os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

MODEL_NAME = "all-MiniLM-L6-v2"
EMBED_MODEL = SentenceTransformer(MODEL_NAME)

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
COLLECTION_NAME = "legal_cases"


def search_query(query: str, top_k: int = 5):
    q_emb = EMBED_MODEL.encode(query).tolist()
    hits = qdrant.search(
        collection_name=COLLECTION_NAME, query_vector=q_emb, limit=top_k
    )
    results = []
    for h in hits:
        payload = h.payload or {}
        results.append(
            {
                "id": h.id,
                "score": h.score,
                "text": (payload.get("text") or "")[:800],
                "source": payload.get("source"),
                "chunk_index": payload.get("chunk_index"),
            }
        )
    return results
