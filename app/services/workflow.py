import logging
import time
from datetime import datetime, timedelta, time as dtime
from app.core.config import settings
from app.services.client import PunchClient
from app.services.time_provider import now_taipei
from app.services.time_policy import is_time_in_window
from app.utils.time_parser import parse_hhmm

logging.basicConfig(level=logging.INFO)

def sleep_until(target: datetime) -> None:
    now = now_taipei()
    seconds = (target - now).total_seconds()

    if seconds <= 0:
        return
    
    time.sleep(seconds)

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
    first_shift_end = clock_in_time + timedelta(hours=settings.first_shift)
    break_end = first_shift_end + timedelta(hours=settings.breaktime)
    clock_out_time = break_end + timedelta(hours=settings.second_shift)

    # Logging
    logging.info(f"Clock-in: {clock_in_time}")
    logging.info(f"First shift end: {first_shift_end}")
    logging.info(f"Break end: {break_end}")
    logging.info(f"Clock-out: {clock_out_time}")

    # Wait & Clock-out
    sleep_until(clock_out_time)
    client.clock_out()