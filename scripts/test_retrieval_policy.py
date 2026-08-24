from app.vector_store import VectorStore
from app.retrieval import retrieve


store = VectorStore()
store.load()


queries = [
    "What is the current return window?",
    "What was the old return window before April 2026?",
    "Do you ship internationally?",
    "Can I return a final sale product?",
]


for query in queries:

    print("\n")
    print("=" * 80)
    print("QUERY:", query)
    print("=" * 80)

    results = retrieve(
        store,
        query,
        top_k=3,
    )

    for rank, result in enumerate(
        results,
        start=1,
    ):

        chunk = result["chunk"]

        print(f"\n#{rank}")

        print(
            "Final score:",
            round(result["final_score"], 4),
        )

        print(
            "Semantic:",
            round(result["semantic_score"], 4),
        )

        print(
            "Metadata:",
            round(result["metadata_score"], 4),
        )

        print("Source:", chunk.source)
        print("Heading:", chunk.heading)
        print("Status:", chunk.metadata.get("status"))
        print("Authority:", chunk.metadata.get("policy_authority"))