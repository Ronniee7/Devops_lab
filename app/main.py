
import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

# --------------------------------------------------
# Configuration
# --------------------------------------------------

APP_NAME = "DevOps Lab API"
APP_VERSION = "0.2.0"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=APP_NAME,
    description=(
        "A production-oriented API built through "
        "a 30-day DevOps engineering challenge."
    ),
    version=APP_VERSION,
)

# Runtime metrics
app.state.started_at = time.time()
app.state.total_requests = 0
app.state.failed_requests = 0


# --------------------------------------------------
# Request Schemas
# --------------------------------------------------

class EchoRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Message to echo back",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


# --------------------------------------------------
# Middleware
# --------------------------------------------------

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    app.state.total_requests += 1

    try:
        response = await call_next(request)

        if response.status_code >= 500:
            app.state.failed_requests += 1

        response.headers["X-Request-ID"] = request_id

        return response

    except Exception:
        app.state.failed_requests += 1
        logger.exception("Request failed: %s", request_id)
        raise

    finally:
        duration = (time.perf_counter() - start_time) * 1000

        logger.info(
            "%s %s | Request ID: %s | Duration: %.2f ms",
            request.method,
            request.url.path,
            request_id,
            duration,
        )


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/", tags=["General"])
async def root():
    return {
        "message": "Welcome to DevOps Lab",
        "application": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "documentation": "/docs",
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health", tags=["Monitoring"])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# --------------------------------------------------
# Readiness Check
# --------------------------------------------------

@app.get("/ready", tags=["Monitoring"])
async def readiness_check():
    return {
        "status": "ready",
        "ready": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# --------------------------------------------------
# Application Information
# --------------------------------------------------

@app.get("/info", tags=["General"])
async def application_info():
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "description": app.description,
        "environment": "development",
        "documentation": "/docs",
        "openapi": "/openapi.json",
    }


# --------------------------------------------------
# Version Endpoint
# --------------------------------------------------

@app.get("/version", tags=["General"])
async def version():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
    }


# --------------------------------------------------
# Runtime Metrics
# --------------------------------------------------

@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    uptime = time.time() - app.state.started_at

    return {
        "application": APP_NAME,
        "uptime_seconds": round(uptime, 2),
        "total_requests": app.state.total_requests,
        "failed_requests": app.state.failed_requests,
        "successful_requests": (
            app.state.total_requests - app.state.failed_requests
        ),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# --------------------------------------------------
# Echo Endpoint
# --------------------------------------------------

@app.post("/echo", tags=["Utilities"])
async def echo(payload: EchoRequest):
    return {
        "message": payload.message,
        "metadata": payload.metadata,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }
