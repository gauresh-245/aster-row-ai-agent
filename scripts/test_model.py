from sentence_transformers import SentenceTransformer


print("Loading model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device="cpu",
)

print("Model loaded successfully!")
print("Embedding dimension:", model.get_sentence_embedding_dimension())