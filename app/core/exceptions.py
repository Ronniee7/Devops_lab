import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger(__name__)


def handle_database_error(
    exc: SQLAlchemyError,
) -> HTTPException:
    """
    Log database errors and return a safe HTTP response.
    """

    logger.exception(
        "Database operation failed",
        exc_info=exc,
    )

    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="A database operation could not be completed.",
    )
