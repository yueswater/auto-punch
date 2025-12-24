from fastapi import APIRouter, HTTPException
from app.services.client import PunchClient
from app.services.workflow import start_work_day, run_pending_events

router = APIRouter(prefix="/punch", tags=["punch"])

@router.post("/start-day")
def start_day():
    try:
        start_work_day()
        return {"status": "ok", "message": "Work day started"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/run-pending")
def run_pending():
    try:
        run_pending_events()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
