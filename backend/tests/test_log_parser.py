from runwright.services.log_parser import extract_relevant_lines


def test_extract_relevant_lines_finds_error_messages() -> None:
    log_text = """Installing dependencies
Running tests
ModuleNotFoundError: No module named 'runwright'
Error: Process completed with exit code 1
Cleaning up
"""

    result = extract_relevant_lines(log_text)

    assert result == [
        (3, "ModuleNotFoundError: No module named 'runwright'"),
        (4, "Error: Process completed with exit code 1"),
    ]


def test_extract_relevant_lines_ignores_normal_output() -> None:
    log_text = """Checking out repository
Installing dependencies
Running tests
All tests passed
"""

    assert extract_relevant_lines(log_text) == []


def test_extract_relevant_lines_respects_max_lines() -> None:
    log_text = """Error: first
Error: second
Error: third
"""

    result = extract_relevant_lines(log_text, max_lines=2)

    assert result == [
        (1, "Error: first"),
        (2, "Error: second"),
    ]