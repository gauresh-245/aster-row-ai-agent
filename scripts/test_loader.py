from app.document_loader import load_documents


documents = load_documents("knowledge-base")

print("Documents loaded:", len(documents))

print("\n" + "=" * 70)

for document in documents:
    print("SOURCE:", document.source)
    print("TITLE:", document.metadata.get("title"))
    print("METADATA:", document.metadata)
    print("TEXT PREVIEW:", document.text[:200].replace("\n", " "))
    print("=" * 70)