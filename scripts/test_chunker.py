from app.document_loader import load_documents
from app.chunker import create_all_chunks


documents = load_documents("knowledge-base")

chunks = create_all_chunks(documents)

print("Documents:", len(documents))
print("Chunks:", len(chunks))

print("\n" + "=" * 80)

for chunk in chunks[:10]:
    print("CHUNK ID:", chunk.chunk_id)
    print("SOURCE:", chunk.source)
    print("HEADING:", chunk.heading)
    print("TEXT:", chunk.text[:300].replace("\n", " "))
    print("STATUS:", chunk.metadata.get("status"))
    print("AUTHORITY:", chunk.metadata.get("policy_authority"))
    print("=" * 80)