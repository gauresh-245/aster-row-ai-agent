import re
from collections import defaultdict

from app.vector_store import VectorStore


STOPWORDS = {
    "a", "an", "the", "is", "are", "am", "was", "were",
    "be", "been", "being", "do", "does", "did",
    "can", "could", "would", "should", "will",
    "i", "me", "my", "we", "our", "you", "your",
    "what", "when", "where", "who", "why", "how",
    "about", "for", "to", "of", "in", "on", "at",
    "and", "or", "but", "if", "with", "from",
    "it", "this", "that", "these", "those",
    "have", "has", "had",
}


def tokenize(text: str) -> set[str]:
    tokens = re.findall(
        r"[a-z0-9]+",
        text.lower(),
    )

    return {
        token
        for token in tokens
        if token not in STOPWORDS
        and len(token) > 1
    }


def authority_score(metadata: dict) -> float:
    score = 0.0

    status = metadata.get("status")
    authority = metadata.get("policy_authority")
    audience = metadata.get("audience")

    if status == "active":
        score += 3.0
    elif status == "superseded":
        score -= 4.0
    elif status == "draft":
        score -= 5.0

    if authority == "official":
        score += 3.0
    elif authority == "none":
        score -= 3.0

    if audience == "customer":
        score += 1.0
    elif audience == "internal":
        score -= 2.0

    return score


def is_customer_safe(metadata: dict) -> bool:

    if metadata.get("status") in {
        "draft",
        "superseded",
    }:
        return False

    if metadata.get("audience") == "internal":
        return False

    if metadata.get("policy_authority") == "none":
        return False

    if metadata.get("customer_answering") == "false":
        return False

    return True


def lexical_score(
    query_tokens: set[str],
    text: str,
) -> float:

    if not query_tokens:
        return 0.0

    text_tokens = tokenize(text)

    overlap = query_tokens.intersection(
        text_tokens
    )

    return len(overlap) / len(query_tokens)


def retrieve(
    store: VectorStore,
    query: str,
    top_k: int = 8,
    candidate_k: int = 50,
):
    """
    Hybrid retrieval.

    Retrieval signals:

    1. Semantic similarity
    2. Lexical overlap
    3. Document authority
    4. Source diversity

    The important difference from the previous version is that
    we deliberately keep evidence from multiple authoritative
    sources instead of allowing one document to dominate.
    """

    candidates = store.search(
        query,
        top_k=candidate_k,
    )

    if not candidates:
        return []

    query_tokens = tokenize(query)

    scored_results = []

    for result in candidates:

        chunk = result["chunk"]
        metadata = chunk.metadata or {}

        if not is_customer_safe(metadata):
            continue

        semantic_score = float(
            result["score"]
        )

        searchable_text = " ".join(
            [
                chunk.source or "",
                chunk.heading or "",
                chunk.text or "",
            ]
        )

        lexical = lexical_score(
            query_tokens,
            searchable_text,
        )

        metadata_score = authority_score(
            metadata
        )

        final_score = (
            semantic_score
            + (0.35 * lexical)
            + (0.12 * metadata_score)
        )

        scored_results.append(
            {
                "chunk": chunk,
                "semantic_score": semantic_score,
                "lexical_score": lexical,
                "metadata_score": metadata_score,
                "final_score": final_score,
            }
        )

    scored_results.sort(
        key=lambda item: item["final_score"],
        reverse=True,
    )

    # ---------------------------------------------------------
    # SOURCE-AWARE SELECTION
    # ---------------------------------------------------------
    #
    # First collect the strongest chunk from every source.
    # This prevents one document from hiding another relevant
    # authoritative document.
    #

    by_source = defaultdict(list)

    for item in scored_results:
        source = item["chunk"].source
        by_source[source].append(item)

    source_best = []

    for source, items in by_source.items():

        items.sort(
            key=lambda item: item["final_score"],
            reverse=True,
        )

        source_best.append(
            items[0]
        )

    source_best.sort(
        key=lambda item: item["final_score"],
        reverse=True,
    )

    selected = []

    # Give every strong source a chance to appear.
    for item in source_best:

        selected.append(item)

        if len(selected) >= top_k:
            break

    # ---------------------------------------------------------
    # FILL REMAINING SLOTS
    # ---------------------------------------------------------

    selected_ids = {
        item["chunk"].chunk_id
        for item in selected
    }

    for item in scored_results:

        chunk_id = item["chunk"].chunk_id

        if chunk_id in selected_ids:
            continue

        selected.append(item)
        selected_ids.add(chunk_id)

        if len(selected) >= top_k:
            break

    return selected[:top_k]