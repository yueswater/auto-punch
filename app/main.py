from fastapi import FastAPI
from app.routers import punch

app = FastAPI(title="Auto Punch API")

app.include_router(router=punch.router)