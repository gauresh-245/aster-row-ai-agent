from app.document_loader import load_documents
from app.chunker import create_all_chunks
from app.vector_store import VectorStore
from app.rag import answer_question


print("Loading documents...")

documents = load_documents("knowledge-base")

print(f"Documents loaded: {len(documents)}")


print("\nCreating chunks...")

chunks = create_all_chunks(documents)

print(f"Chunks created: {len(chunks)}")


print("\nCreating vector store...")

store = VectorStore()

print("Building FAISS index...")

store.build(chunks)

print("Vector store ready.")


print("\n" + "=" * 70)
print("ASTER & ROW RAG SUPPORT AGENT")
print("=" * 70)
print("Ask a customer-support question.")
print("Type 'exit' to quit.")
print("=" * 70)


while True:

    question = input("\nCustomer: ").strip()

    if question.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break

    if not question:
        continue

    try:

        result = answer_question(
            store=store,
            question=question,
        )

        print("\nAgent:")
        print(result["answer"])

        print("\nRetrieved Sources:")

        for source in result["sources"]:

            print(
                f"- {source['source']} "
                f"(score={source['semantic_score']:.4f})"
            )

    except Exception as e:

        print("\nERROR:")
        print(type(e).__name__, str(e))