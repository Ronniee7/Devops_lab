import logging
import logging.config


def configure_logging(log_level: str = "INFO") -> None:
    """
    Configure centralized application logging.

    Logs are written to stdout so that container platforms
    such as Docker can collect them.
    """

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": ("%(asctime)s | %(levelname)s | %(name)s | %(message)s"),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "stream": "ext://sys.stdout",
                }
            },
            "root": {
                "level": log_level.upper(),
                "handlers": ["console"],
            },
        }
    )
