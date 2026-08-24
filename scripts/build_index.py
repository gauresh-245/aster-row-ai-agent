from app.document_loader import load_documents
from app.chunker import create_all_chunks
from app.vector_store import VectorStore


print("Loading documents...")

documents = load_documents("knowledge-base")

print(f"Loaded {len(documents)} documents.")

print("Creating chunks...")

chunks = create_all_chunks(documents)

print(f"Created {len(chunks)} chunks.")

print("Generating embeddings and building FAISS index...")

store = VectorStore()

store.build(chunks)

store.save()

print("Vector store created successfully.")