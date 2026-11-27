import logging
from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import Settings
from app.core.exceptions import handle_database_error
from app.db.session import get_db
from app.db.transaction import execute_transaction


def test_transaction_commits_and_returns_result():
    db = Mock()
    operation = Mock(return_value="success")

    result = execute_transaction(db, operation)

    assert result == "success"
    operation.assert_called_once()
    db.commit.assert_called_once()
    db.rollback.assert_not_called()


def test_transaction_rolls_back_and_reraises_error():
    db = Mock()
    operation = Mock(side_effect=RuntimeError("Operation failed"))

    with pytest.raises(RuntimeError, match="Operation failed"):
        execute_transaction(db, operation)

    db.rollback.assert_called_once()
    db.commit.assert_not_called()


def test_database_session_is_closed_after_use(monkeypatch):
    fake_session = Mock()

    monkeypatch.setattr(
        "app.db.session.SessionLocal",
        lambda: fake_session,
    )

    generator = get_db()

    session = next(generator)

    assert session is fake_session
    fake_session.close.assert_not_called()

    generator.close()

    fake_session.close.assert_called_once()


def test_database_error_returns_safe_http_exception(caplog):
    database_error = SQLAlchemyError("Internal database details")

    with caplog.at_level(
        logging.ERROR,
        logger="app.core.exceptions",
    ):
        response = handle_database_error(database_error)

    assert isinstance(response, HTTPException)
    assert response.status_code == 503
    assert response.detail == ("A database operation could not be completed.")
    assert "Internal database details" in caplog.text
    assert "Database operation failed" in caplog.text


def test_production_settings_accept_valid_configuration():
    settings = Settings(
        _env_file=None,
        APP_ENV="production",
        DEBUG=False,
        DB_PASSWORD="secure-test-password",
    )

    assert settings.APP_ENV == "production"
    assert settings.DEBUG is False
    assert settings.DB_PASSWORD.get_secret_value() == ("secure-test-password")


def test_production_settings_reject_debug_mode():
    with pytest.raises(ValidationError, match="DEBUG must be false"):
        Settings(
            _env_file=None,
            APP_ENV="production",
            DEBUG=True,
            DB_PASSWORD="secure-test-password",
        )


def test_production_settings_require_database_password():
    with pytest.raises(
        ValidationError,
        match="DB_PASSWORD is required in production",
    ):
        Settings(
            _env_file=None,
            APP_ENV="production",
            DEBUG=False,
            DB_PASSWORD="",
        )
