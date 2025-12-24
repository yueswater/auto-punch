
import requests
from datetime import datetime, date
from app.services.time_provider import now_taipei
from app.core.config import settings


FORM_URL = settings.google_form_url


def log_event(
    date_: date,
    action: str,
    time_: datetime,
) -> None:
    payload = {
        "entry.DATE": date_.isoformat(),
        "entry.ACTION": action,
        "entry.TIME_HOUR": time_.strftime("%H"),
        "entry.TIME_MINUTE": time_.strftime("%M"),
    }

    resp = requests.post(FORM_URL, data=payload, timeout=10)
    resp.raise_for_status()

def get_pending_events(now: datetime) -> list[dict]:
    resp = requests.get(settings.google_sheet_api_url, timeout=10)
    resp.raise_for_status()

    rows: list[dict] = resp.json()["data"]

    done_actions: set[str] = {
        row["action"]
        for row in rows
        if row["action"].endswith("_done")
    }

    pending: list[dict] = []

    for row in rows:
        action = row["action"]
        if action.endswith("_done"):
            continue
        if f"{action}_done" in done_actions:
            continue
        event_time = datetime.fromisoformat(
            f"{row['date']}T{row['time']}"
        )
        if event_time <= now:
            pending.append(row)

    return pending

def mark_event_done(event: dict) -> None:
    now = now_taipei()
    action_done = f"{event['action']}_done"

    payload = {
        settings.form_entry_date: event["date"],
        settings.form_entry_action: action_done,
        settings.form_entry_time_hour: now.strftime("%H"),
        settings.form_entry_time_minute: now.strftime("%M"),
    }

    resp = requests.post(
        settings.google_form_url,
        data=payload,
        timeout=10,
    )

    if resp.status_code not in (200, 302):
        raise RuntimeError(
            f"Failed to mark event done: {event['action']}"
        )