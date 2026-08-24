from pathlib import Path
import json

import faiss
import numpy as np

from app.chunker import Chunk
from app.embeddings import EmbeddingModel


class VectorStore:
    """
    Stores chunk embeddings and performs similarity search.
    """

    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.index = None
        self.chunks: list[Chunk] = []

    def build(self, chunks: list[Chunk]):
        """
        Generate embeddings for all chunks and build a FAISS index.
        """

        self.chunks = chunks

        texts = [
    f"""
    Source: {chunk.source}
    Heading: {chunk.heading}
    Title: {chunk.metadata.get("title", "")}

    {chunk.text}
    """
    for chunk in chunks
]

        embeddings = self.embedding_model.encode(texts)

        embeddings = np.asarray(
            embeddings,
            dtype="float32",
        )

        dimension = embeddings.shape[1]

        # Inner product + normalized embeddings
        # = cosine similarity
        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Retrieve the most semantically similar chunks.
        """

        if self.index is None:
            raise RuntimeError("Vector store has not been built.")

        query_embedding = self.embedding_model.encode([query])

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32",
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):
            if index == -1:
                continue

            results.append(
                {
                    "score": float(score),
                    "chunk": self.chunks[index],
                }
            )

        return results

    def save(
        self,
        index_path: str = "data/vector.index",
        metadata_path: str = "data/chunks.json",
    ):
        """
        Save the FAISS index and chunk metadata.
        """

        if self.index is None:
            raise RuntimeError("Vector store has not been built.")

        Path(index_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            index_path,
        )

        serialized_chunks = []

        for chunk in self.chunks:
            serialized_chunks.append(
                {
                    "chunk_id": chunk.chunk_id,
                    "text": chunk.text,
                    "source": chunk.source,
                    "heading": chunk.heading,
                    "metadata": chunk.metadata,
                }
            )

        Path(metadata_path).write_text(
            json.dumps(
                serialized_chunks,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def load(
        self,
        index_path: str = "data/vector.index",
        metadata_path: str = "data/chunks.json",
    ):
        """
        Load an existing vector store.
        """

        self.index = faiss.read_index(index_path)

        raw_chunks = json.loads(
            Path(metadata_path).read_text(
                encoding="utf-8"
            )
        )

        self.chunks = []

        for item in raw_chunks:
            self.chunks.append(
                Chunk(
                    chunk_id=item["chunk_id"],
                    text=item["text"],
                    source=item["source"],
                    heading=item["heading"],
                    metadata=item["metadata"],
                )
            )