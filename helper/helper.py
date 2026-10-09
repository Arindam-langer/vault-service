from datetime import timezone, datetime


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
