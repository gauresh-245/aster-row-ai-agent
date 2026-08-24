from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any


@dataclass
class Document:
    """
    Represents one complete Markdown knowledge-base document.
    """

    source: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


def parse_front_matter(content: str) -> tuple[dict[str, Any], str]:
    """
    Extract YAML-like front matter from the beginning of a Markdown file.

    Expected structure:

    ---
    key: value
    another_key: value
    ---

    document content...
    """

    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)

    if len(parts) != 3:
        return {}, content

    raw_metadata = parts[1].strip()
    body = parts[2].strip()

    metadata: dict[str, Any] = {}

    for line in raw_metadata.splitlines():
        line = line.strip()

        if not line or ":" not in line:
            continue

        key, value = line.split(":", 1)

        metadata[key.strip()] = value.strip().strip('"').strip("'")

    return metadata, body


def extract_title(text: str) -> str | None:
    """
    Extract the first Markdown H1 title.
    """

    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)

    if match:
        return match.group(1).strip()

    return None


def load_documents(knowledge_base_dir: str) -> list[Document]:
    """
    Load all Markdown files from the knowledge-base directory.
    """

    directory = Path(knowledge_base_dir)

    if not directory.exists():
        raise FileNotFoundError(
            f"Knowledge-base directory not found: {directory}"
        )

    documents: list[Document] = []

    for path in sorted(directory.glob("*.md")):
        content = path.read_text(
            encoding="utf-8"
        )

        metadata, body = parse_front_matter(content)

        title = extract_title(body)

        if title:
            metadata["title"] = title

        metadata["source"] = path.name

        documents.append(
            Document(
                source=path.name,
                text=body,
                metadata=metadata,
            )
        )

    return documents