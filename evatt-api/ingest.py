import io
import hashlib
import os
import uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import pdfplumber
from utils import chunk_text

MODEL_NAME = "all-MiniLM-L6-v2"
EMBED_MODEL = SentenceTransformer(MODEL_NAME)

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
COLLECTION_NAME = "legal_cases"

try:
    qdrant.get_collection(COLLECTION_NAME)
except Exception:
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            "size": EMBED_MODEL.get_sentence_embedding_dimension(),
            "distance": "Cosine",
        },
    )


def pdf_to_text_bytes(b: bytes) -> str:
    text = []
    with pdfplumber.open(io.BytesIO(b)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def ingest_file(filename: str, content: bytes) -> int:
    """Extracts text, chunks it, embeds, and upserts into Qdrant."""
    if filename.lower().endswith(".pdf"):
        text = pdf_to_text_bytes(content)
    else:
        try:
            text = content.decode("utf-8")
        except Exception:
            text = content.decode("latin-1")

    chunks = chunk_text(text, max_chars=1000)
    points = []
    for i, chunk in enumerate(chunks):
        uid = uuid.uuid5(uuid.NAMESPACE_DNS, filename + str(i))
        emb = EMBED_MODEL.encode(chunk).tolist()
        payload = {"text": chunk, "source": filename, "chunk_index": i}
        points.append(PointStruct(id=str(uid), vector=emb, payload=payload))

    BATCH = 64
    for i in range(0, len(points), BATCH):
        qdrant.upsert(collection_name=COLLECTION_NAME, points=points[i : i + BATCH])

    return len(points)
