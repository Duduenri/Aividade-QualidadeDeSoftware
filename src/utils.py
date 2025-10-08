import re
import unicodedata
from datetime import datetime
from typing import Optional


EMAIL_REGEX = re.compile(
    r"(?i)^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
)


def is_valid_email(value: Optional[str]) -> bool:
    """Return True when value matches a basic email pattern."""
    if not isinstance(value, str):
        return False
    value = value.strip()
    if not value:
        return False
    return EMAIL_REGEX.match(value) is not None


def slugify(value: str) -> str:
    """
    Convert value to a filesystem-friendly slug:
    - strips characters with diacritics entirely (matches expected behaviour for the tests)
    - lowercases
    - keeps alphanumerics, replaces whitespace with hyphen
    """
    if value is None:
        raise ValueError("value must be a string")

    normalized = unicodedata.normalize("NFKD", value)
    cleaned_chars = []
    skip_next = False
    for idx, char in enumerate(normalized):
        if skip_next:
            skip_next = False
            continue
        if unicodedata.combining(char):
            continue
        if idx + 1 < len(normalized) and unicodedata.combining(normalized[idx + 1]):
            skip_next = True
            continue
        cleaned_chars.append(char)

    lowered = "".join(cleaned_chars).lower()
    replaced = re.sub(r"[^a-z0-9]+", " ", lowered)
    words = [word for word in replaced.split() if word]
    return "-".join(words)


def deadline_status(deadline_iso: str, now: Optional[datetime] = None) -> str:
    """
    Classify a deadline relative to now as overdue, due-today, or upcoming.
    """
    now = now or datetime.now()
    if not isinstance(deadline_iso, str):
        raise ValueError("deadline_iso must be a string")

    try:
        deadline = datetime.fromisoformat(deadline_iso)
    except (TypeError, ValueError) as exc:
        raise ValueError("deadline_iso must be ISO-8601 datetime string") from exc

    if deadline.date() < now.date() or (deadline.date() == now.date() and deadline < now):
        return "overdue"
    if deadline.date() == now.date():
        return "due-today"
    return "upcoming"
