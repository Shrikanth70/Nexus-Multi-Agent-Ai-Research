"""
Observability Foundation.

Configures structured logging using `structlog`.
Per OBSERVABILITY.md, every agent execution, tool call, and state transition
must be logged as a parseable JSON object with bound context (e.g., session_id).
"""

import logging
import sys
from typing import Any

import structlog

def setup_logging(log_format: str = "console", log_level: str = "INFO") -> None:
    """
    Configures structlog and the standard library logging.
    
    Args:
        log_format: "json" for production (easily parseable), "console" for local development.
        log_level: Standard logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure the standard library logging first
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )
    
    # Structlog processors
    processors = [
        structlog.contextvars.merge_contextvars,          # Allows binding context globally via contextvars
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    if log_format == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        # Development console formatting
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
def get_logger(name: str) -> Any:
    """
    Helper to get a structured logger.
    
    Args:
        name: Usually __name__ of the calling module.
        
    Returns:
        A structlog BoundLogger instance.
    """
    return structlog.get_logger(name)
