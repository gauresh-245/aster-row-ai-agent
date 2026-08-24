from app.embeddings import EmbeddingModel


model = EmbeddingModel()

texts = [
    "How long do I have to return an item?",
    "What is the return policy?",
    "Do you ship to Canada?",
]

embeddings = model.encode(texts)

print("Number of texts:", len(texts))
print("Embedding shape:", embeddings.shape)

print("First embedding:")
print(embeddings[0])