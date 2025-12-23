from datetime import datetime
from zoneinfo import ZoneInfo
from app.core.config import settings

TZ = ZoneInfo(key=settings.timezone)

def now_taipei() -> datetime:
    return datetime.now(tz=TZ)