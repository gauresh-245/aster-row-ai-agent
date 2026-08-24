from app.document_loader import load_documents
from app.chunker import create_all_chunks
from app.vector_store import VectorStore
from app.retrieval import retrieve


documents = load_documents("knowledge-base")
chunks = create_all_chunks(documents)

store = VectorStore()
store.build(chunks)


questions = [
    "My TrailPlus membership was active when I ordered. What is my return window?",
    "What about shipping to Canada and how long does it take?",
    "Can you ship an Atlas Weekender to Germany?",
    "Do all Aster & Row products have a lifetime warranty?",
    "Can I put the entire Breeze Tumbler in the dishwasher?",
]


for question in questions:

    print("\n" + "=" * 70)
    print(question)
    print("=" * 70)

    results = retrieve(
        store=store,
        query=question,
        top_k=5,
        candidate_k=30,
    )

    for result in results:
        chunk = result["chunk"]

        print(
            f"{chunk.source} | "
            f"{chunk.heading} | "
            f"{result['final_score']:.4f}"
        )