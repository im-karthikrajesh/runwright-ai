ERROR_KEYWORDS = (
    "error",
    "failed",
    "failure",
    "exception",
    "traceback",
    "modulenotfounderror",
    "importerror",
    "permission denied",
    "timed out",
)


def extract_relevant_lines(
        log_text: str,
        *,
        max_lines: int = 25,
) -> list[tuple[int, str]]:
    """Extract likely failure related lines from a CI log."""

    relevant_lines: list[tuple[int, str]] = []

    for line_number, line in enumerate(log_text.splitlines(), start=1):
        stripped_line = line.strip()

        if not stripped_line:
            continue

        lowercase_line = stripped_line.lower()

        if any(keyword in lowercase_line for keyword in ERROR_KEYWORDS):
            relevant_lines.append((line_number, stripped_line))

        if len(relevant_lines) >= max_lines:
            break

    return relevant_lines