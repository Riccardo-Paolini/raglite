"""Chunking sentence-aware per il laboratorio."""

from __future__ import annotations


def _split_sentences(text: str) -> list[str]:
    """Divide il testo in frasi senza spezzarle a metà."""
    text = text.strip()
    if not text:
        return []

    sentences: list[str] = []
    current: list[str] = []

    for char in text:
        current.append(char)
        if char in ".!?":
            sentence = "".join(current).strip()
            if sentence:
                sentences.append(sentence)
            current = []

    tail = "".join(current).strip()
    if tail:
        sentences.append(tail)

    return sentences

def chunk_text(text: str, size: int, overlap: int) -> list[tuple[int, str]]:
    """Restituisce chunk testuali con overlap in numero di frasi."""
    if size <= 0:
        raise ValueError("size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")

    sentences = _split_sentences(text)
    if not sentences:
        return []

    chunks: list[tuple[int, str]] = []
    chunk_id = 0
    i = 0

    while i < len(sentences):
        acc: list[str] = []
        char_count = 0
        j = i

        while j < len(sentences):
            sentence = sentences[j]
            sentence_len = len(sentence) + (1 if acc else 0)

            # Prima frase: sempre dentro
            if not acc:
                acc.append(sentence)
                char_count += sentence_len
                j += 1
                continue

            # Seconda frase: permettila anche se sfora (serve per overlap)
            if len(acc) == 1:
                acc.append(sentence)
                char_count += sentence_len
                j += 1
                continue

            # Dalla terza frase: rispetta size
            if char_count + sentence_len > size:
                break

            acc.append(sentence)
            char_count += sentence_len
            j += 1

        chunk_text_str = " ".join(acc)
        chunks.append((chunk_id, chunk_text_str))
        chunk_id += 1

        if j >= len(sentences):
            break

        # Avanza mantenendo overlap (numero di frasi)
        i = max(j - overlap, i + 1)

    return chunks