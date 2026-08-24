from app.document_loader import load_documents
from app.chunker import create_all_chunks
from app.vector_store import VectorStore
from app.agent import ask_agent
from app.memory import ConversationMemory


print("Loading documents...")

documents = load_documents("knowledge-base")

print(f"Documents loaded: {len(documents)}")


print("\nCreating chunks...")

chunks = create_all_chunks(documents)

print(f"Chunks created: {len(chunks)}")


print("\nCreating vector store...")

store = VectorStore()

store.build(chunks)

print("Vector store ready.")


print("\nCreating conversation memory...")

memory = ConversationMemory()

print("Memory ready.")


print("\n" + "=" * 70)
print("ASTER & ROW AI CUSTOMER SERVICE AGENT")
print("=" * 70)


questions = [
    "What is the status of order ORD-1001?",
    "Can I cancel it?",
    "What is the warranty period for bags?",
    "Do you ship to Canada?",
]


for question in questions:

    print(f"\nCustomer: {question}")

    try:

        answer = ask_agent(
            question=question,
            store=store,
            memory=memory,
        )

        print(f"Agent: {answer}")

    except Exception as e:

        print(
            f"ERROR: {type(e).__name__}: {e}"
        )