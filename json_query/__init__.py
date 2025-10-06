"""json-query: jq-light CLI.

Экспорт высокоуровневого API для использования из кода.
"""

from .engine import execute_query

__all__ = ["execute_query"]


