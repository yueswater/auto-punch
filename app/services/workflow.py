import logging
import time
from datetime import datetime, timedelta, time as dtime
from app.core.config import settings
from app.services.client import PunchClient
from app.services.time_provider import now_taipei
from app.services.time_policy import is_time_in_window
from app.services.form_logger import log_event, get_pending_events, mark_event_done
from app.utils.time_parser import parse_hhmm

logger = logging.getLogger(__name__)

def start_work_day() -> None:
    # Fetch now time
    now_dt: datetime = now_taipei()
    now_time: dtime = now_dt.time()

    # Work start window
    start_time: dtime = parse_hhmm(settings.work_start_earliest)
    end_time: dtime = parse_hhmm(settings.work_start_latest)

    # Validate clock-in window
    if not is_time_in_window(now_time, start_time, end_time):
        raise RuntimeError(
            f"Now time {now_time.strftime('%H:%M')} not in "
            f"{settings.work_start_earliest}~{settings.work_start_latest}"
        )

    # Clock-in
    client = PunchClient()
    client.login()
    client.clock_in()

    clock_in_time = now_taipei()

    # Calculate key timing
    break_start_time = clock_in_time + timedelta(hours=settings.first_shift)
    break_end_time = break_start_time + timedelta(hours=settings.breaktime)
    clock_out_time = break_end_time + timedelta(hours=settings.second_shift)

    # Logging
    log_event(date=clock_in_time.date(), action="clock_in", time=clock_in_time)
    log_event(date=clock_in_time.date(), action="break_start", time=break_start_time)
    log_event(date=clock_in_time.date(), action="break_end", time=break_end_time)
    log_event(date=clock_in_time.date(), action="clock_out", time=clock_out_time)

    logger.info("Work day registered")

def run_pending_events() -> None:
    now = now_taipei()
    pending_events = get_pending_events(now)

    if not pending_events:
        logger.info("No pending events")
        return

    client = PunchClient()
    client.login()

    for event in pending_events:
        action = event["action"]
        logger.info(f"Executing event: {action}")

        if action == "break_start":
            client.break_start()

        elif action == "break_end":
            client.break_cancel()

        elif action == "clock_out":
            client.clock_out()

        else:
            logger.warning(f"Unknown action: {action}")
            continue

        mark_event_done(event)