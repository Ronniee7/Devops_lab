
from fastapi import FastAPI
from datetime import datetime, timezone
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="A production-oriented API built through a 30 day DEVOPS Challenge.",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Devops Lab",
        "application": settings.APP_NAME,
        "version":settings.APP_VERSION,
        "environment":settings.APP_ENV,
        "status": "running",
    
    }
@app.get("/health")
async def health_check():
    return {
        "status": "health",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": settings.APP_ENV,        
    }
