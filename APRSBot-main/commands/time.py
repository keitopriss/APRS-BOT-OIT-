from datetime import datetime, timezone


def handle_command():
    """Balas dengan waktu Zulu (UTC) saat ini."""
    zulu_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    return f"Current Zulu Time: {zulu_time}"