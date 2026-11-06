
import logging
from datetime import datetime, timezone
from time import perf_counter

from fastapi import FastAPI, Request

from app.core.config import settings
from app.core.logging import configure_logging


# Initialize logging before creating the application.
configure_logging(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.APP_NAME,
    description="A production-oriented API built through a 30-day DevOps challenge.",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log incoming HTTP requests, response status codes,
    and request processing time.
    """

    start_time = perf_counter()

    try:
        response = await call_next(request)

        duration = (perf_counter() - start_time) * 1000

        logger.info(
            "HTTP request | method=%s | path=%s | status=%s | duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        duration = (perf_counter() - start_time) * 1000

        logger.exception(
            "HTTP request failed | method=%s | path=%s | duration_ms=%.2f",
            request.method,
            request.url.path,
            duration,
        )

        raise


@app.on_event("startup")
async def application_startup():
    logger.info(
        "Application starting | name=%s | environment=%s",
        settings.APP_NAME,
        settings.APP_ENV,
    )


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")

    return {
        "message": "Welcome to DevOps Lab",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": settings.APP_ENV,
    }
