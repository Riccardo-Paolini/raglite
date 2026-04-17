"""Embedding locale deterministico per il laboratorio."""

from __future__ import annotations

from array import array


def embed_text(text: str) -> list[float]:
    """Restituisce un embedding deterministico 4D."""
    b = text.encode("utf8")

    if not b:
        return [0.0, 0.0, 0.0, 0.0]

    length = float(len(b))
    total = float(sum(b))
    first = float(b[0])
    last = float(b[-1])

    return [length, total, first, last]


def vector_to_blob(vector: list[float]) -> bytes:
    """Serializza il vettore come BLOB SQLite."""
    return array("f", vector).tobytes()