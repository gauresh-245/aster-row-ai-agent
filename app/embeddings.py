from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Converts text into semantic vectors.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(
            model_name,
            device="cpu",
        )

    def encode(self, texts: list[str]):
        """
        Convert text into normalized semantic embeddings.
        """
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )