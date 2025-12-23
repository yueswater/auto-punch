from fastapi import APIRouter, HTTPException
from app.services.client import PunchClient
from app.services.workflow import start_work_day

router = APIRouter(prefix="/punch", tags=["punch"])

@router.post("/start-day")
def start_day():
    try:
        start_work_day()
        return {"status": "ok", "message": "Work day started"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))