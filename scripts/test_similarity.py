import numpy as np

from app.embeddings import EmbeddingModel


embedding_model = EmbeddingModel()

texts = [
    "You can return unused merchandise within 30 calendar days of delivery.",
    "Customers have 30 days to send an unused item back.",
    "We currently ship to Canada.",
    "Orders are usually delivered within five business days.",
]

query = "How long do I have to send something back?"

vectors = embedding_model.encode(texts)
query_vector = embedding_model.encode([query])[0]

scores = vectors @ query_vector

for text, score in sorted(
    zip(texts, scores),
    key=lambda x: x[1],
    reverse=True,
):
    print(f"{score:.4f} -> {text}")