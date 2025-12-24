from fastapi import FastAPI
from app.routers import punch

app = FastAPI(title="Auto Punch API")

app.include_router(router=punch.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ping")
def ping():
    return "pong"