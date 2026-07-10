"""Standard structlog configuration for vault automation scripts."""

import os
import sys

import structlog
from structlog.contextvars import merge_contextvars, clear_contextvars, bind_contextvars


def configure_logging():
    """Configure structlog with JSON output for production, colored console for dev."""
    is_dev = os.environ.get("VAULT_LOG_FORMAT", "dev") == "dev"

    if is_dev:
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[
            merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(0),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )


def get_logger(name):
    """Return a bound logger for the given module name."""
    return structlog.get_logger(logger_name=name)


def clear_and_bind(**context):
    """Clear all contextvars and bind new ones."""
    clear_contextvars()
    bind_contextvars(**context)
