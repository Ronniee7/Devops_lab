
from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="DevOps Lab API",
    description="A production-oriented API built through a 30-day DevOps engineering challenge.",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to DevOps Lab",
        "application": "DevOps Lab API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
