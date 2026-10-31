# ARMAN UPDATE 10/31/2026


# Small helper functions shared by the whole project.
from datetime import datetime, timedelta

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def now_text(plus_minutes=0):
    """Return the current date and time as text (optionally some minutes later)."""
    moment = datetime.now() + timedelta(minutes=plus_minutes)
    return moment.strftime(DATETIME_FORMAT)
