from dataclasses import dataclass
import re
from typing import Any

from app.document_loader import Document


@dataclass
class Chunk:
    """
    A retrievable piece of a knowledge-base document.
    """

    chunk_id: str
    text: str
    source: str
    heading: str
    metadata: dict[str, Any]


def split_markdown_sections(text: str) -> list[tuple[str, str]]:
    """
    Split Markdown into sections based on ## headings.

    Returns:
        [
            ("Heading 1", "section text..."),
            ("Heading 2", "section text...")
        ]
    """

    pattern = r"^##\s+(.+)$"

    matches = list(re.finditer(pattern, text, re.MULTILINE))

    if not matches:
        return [("General", text.strip())]

    sections: list[tuple[str, str]] = []

    for index, match in enumerate(matches):
        heading = match.group(1).strip()

        start = match.end()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(text)

        section_text = text[start:end].strip()

        if section_text:
            sections.append((heading, section_text))

    return sections


def create_chunks(
    document: Document,
    max_characters: int = 1800,
) -> list[Chunk]:
    """
    Convert one document into retrievable chunks.

    Each Markdown section becomes one or more chunks.
    """

    sections = split_markdown_sections(document.text)

    chunks: list[Chunk] = []

    for section_number, (heading, section_text) in enumerate(
        sections,
        start=1,
    ):

        if len(section_text) <= max_characters:
            pieces = [section_text]

        else:
            pieces = [
                section_text[i:i + max_characters]
                for i in range(
                    0,
                    len(section_text),
                    max_characters,
                )
            ]

        for piece_number, piece in enumerate(
            pieces,
            start=1,
        ):
            chunk_id = (
                f"{document.source}"
                f"::section-{section_number}"
                f"::chunk-{piece_number}"
            )

            metadata = dict(document.metadata)

            metadata["heading"] = heading
            metadata["section_number"] = section_number
            metadata["chunk_number"] = piece_number

            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    text=piece,
                    source=document.source,
                    heading=heading,
                    metadata=metadata,
                )
            )

    return chunks


def create_all_chunks(
    documents: list[Document],
    max_characters: int = 1800,
) -> list[Chunk]:
    """
    Create chunks for every knowledge-base document.
    """

    all_chunks: list[Chunk] = []

    for document in documents:
        all_chunks.extend(
            create_chunks(
                document,
                max_characters=max_characters,
            )
        )

    return all_chunks