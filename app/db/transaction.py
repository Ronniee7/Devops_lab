from collections.abc import Callable
from typing import TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")


def execute_transaction(
    db: Session,
    operation: Callable[[], T],
) -> T:
    """
    Execute a database operation within a transaction.

    Commit when successful and rollback when an error occurs.
    """

    try:
        result = operation()
        db.commit()
        return result

    except Exception:
        db.rollback()
        raise
