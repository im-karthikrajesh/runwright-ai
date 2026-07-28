import re

SECRET_PATTERNS = (
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\b\s*[:=]\s*[^\s]+"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]+\b"),
)


def redact_secrets(text: str) -> str:
    """Replace likely secrets in CI logs before further processing."""

    redacted_text = text

    for pattern in SECRET_PATTERNS:
        redacted_text = pattern.sub("[REDACTED_SECRET]", redacted_text)

    return redacted_text