import re


def chunk_text(text: str, max_chars: int = 1000, overlap: int = 200):
    """Simple character-based chunking with overlap."""
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + max_chars, L)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == L:
            break
        start = end - overlap
    return chunks
