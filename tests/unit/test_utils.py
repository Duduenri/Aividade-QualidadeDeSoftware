
import pytest
from src.utils import is_valid_email, slugify, deadline_status
from datetime import datetime

class TestIsValidEmail:
    @pytest.mark.parametrize("email", [
        "alice@example.com",
        "john.doe@corp.co",
        "a_b-c.d@sub.domain.org",
    ])
    def test_valid_emails(self, email):
        assert is_valid_email(email) is True

    @pytest.mark.parametrize("email", [
        "", None, "no-at.com", "bad@tld", "bad@domain.", "@nouser.com"
    ])
    def test_invalid_emails(self, email):
        assert is_valid_email(email) is False

class TestSlugify:
    @pytest.mark.parametrize("title, expected", [
        ("Olá Mundo", "ol-mundo"),
        (" Hello,   World!!! ", "hello-world"),
        ("Python & Testes Automatizados", "python-testes-automatizados"),
    ])
    def test_slugify_basic(self, title, expected):
        assert slugify(title) == expected

    def test_slugify_none_raises(self):
        with pytest.raises(ValueError):
            slugify(None)

class TestDeadlineStatus:
    def test_overdue(self):
        now = datetime(2024, 10, 15, 12, 0, 0)
        assert deadline_status("2024-10-10T00:00:00", now) == "overdue"

    def test_due_today(self):
        now = datetime(2024, 10, 15, 12, 0, 0)
        assert deadline_status("2024-10-15T23:59:59", now) == "due-today"

    def test_upcoming(self):
        now = datetime(2024, 10, 15, 12, 0, 0)
        assert deadline_status("2024-10-20T00:00:00", now) == "upcoming"

    def test_invalid_iso_raises(self):
        with pytest.raises(ValueError):
            deadline_status("20-10-2024")
