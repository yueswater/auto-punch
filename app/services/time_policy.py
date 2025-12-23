from datetime import time as dtime

def is_time_in_window(
    now: dtime,
    start: dtime,
    end: dtime
) -> bool:
    if start <= end:
        return start <= now <= end
    else:
        return now >= start or now <= end