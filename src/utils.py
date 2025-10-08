
import re
from datetime import datetime

def is_valid_email(email: str) -> bool:
    if not isinstance(email, str) or not email:
        return False
    return re.match(r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$", email) is not None

def slugify(title: str) -> str:
    if title is None:
        raise ValueError("title cannot be None")
    s = title.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def deadline_status(deadline_iso: str, now: datetime | None = None) -> str:
    if now is None:
        now = datetime.utcnow()
    try:
        deadline = datetime.fromisoformat(deadline_iso)
    except Exception as e:
        raise ValueError("invalid ISO datetime") from e
    today = now.date()
    dday = deadline.date()
    if dday < today:
        return "overdue"
    if dday == today:
        return "due-today"
    return "upcoming"
