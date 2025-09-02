from datetime import datetime
from typing import Optional

def parse_date(value: Optional[str]) -> Optional[datetime]:
    """
    Parse date string from form (YYYY-MM-DD).
    Returns datetime object or None if empty/invalid.
    """
    if not value or value.strip() == "":
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None

def format_date(start: Optional[datetime], end: Optional[datetime]) -> str:
    """
    Format date range for resume display.
    If end is None, return 'Present'.
    Example: Jan 2022 – Present
    """
    fmt = "%b %Y"
    start_str = start.strftime(fmt) if start else ""
    end_str = end.strftime(fmt) if end else "Present"
    return f"{start_str} – {end_str}".strip(" –")
