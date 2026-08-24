def build_context(results) -> str:
    """
    Convert retrieved chunks into a structured context
    that can be supplied to the LLM.
    """

    sections = []

    for index, result in enumerate(
        results,
        start=1,
    ):

        chunk = result["chunk"]

        sections.append(
            f"""
SOURCE {index}
File: {chunk.source}
Heading: {chunk.heading}
Status: {chunk.metadata.get("status")}
Authority: {chunk.metadata.get("policy_authority")}

Content:
{chunk.text}
""".strip()
        )

    return "\n\n---\n\n".join(sections)