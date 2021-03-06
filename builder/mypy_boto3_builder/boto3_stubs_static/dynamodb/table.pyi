# pylint: disable=unused-argument,multiple-statements,no-self-use
from typing import Any, List, Optional, Dict, Type

# from types import TracebackType
import logging

from botocore.client import BaseClient

logger: logging.Logger

def register_table_methods(base_classes: List[type], **kwargs: Any) -> None: ...

class TableResource:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def batch_writer(
        self, overwrite_by_pkeys: Optional[List[str]] = None
    ) -> "BatchWriter": ...

class BatchWriter:
    def __init__(
        self,
        table_name: str,
        client: BaseClient,
        flush_amount: int = 25,
        overwrite_by_pkeys: Optional[List[str]] = None,
    ) -> None: ...
    def put_item(self, Item: Dict[str, Any]) -> None: ...
    def delete_item(self, Key: Dict[str, Any]) -> None: ...
    def __enter__(self) -> "BatchWriter": ...
    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        # tb: TracebackType,
        tb: Any,
    ) -> None: ...
