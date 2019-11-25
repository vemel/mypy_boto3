# pylint: disable=unused-argument,multiple-statements,super-init-not-called,no-self-use,no-self-argument
from __future__ import annotations

import logging
from typing import Any, Iterator, List

from botocore.hooks import HierarchicalEmitter

from boto3.resources.model import Collection
from boto3.resources.base import ServiceResource
from boto3.resources.factory import ResourceFactory
from boto3.resources.response import ResourceHandler
from boto3.utils import ServiceContext

logger: logging.Logger

class ResourceCollection:
    def __init__(
        self,
        model: Collection,
        parent: ServiceResource,
        handler: ResourceHandler,
        **kwargs: Any
    ) -> None: ...
    def __repr__(self) -> str: ...
    def __iter__(self) -> Iterator[Any]: ...
    def pages(self) -> List[ServiceResource]: ...
    def all(self) -> ResourceCollection: ...
    def filter(self, **kwargs: Any) -> ResourceCollection: ...
    def limit(self, count: int) -> ResourceCollection: ...
    def page_size(self, count: int) -> ResourceCollection: ...

class CollectionManager:
    _collection_cls = ResourceCollection
    def __init__(
        self,
        collection_model: Collection,
        parent: ServiceResource,
        factory: ResourceFactory,
        service_context: ServiceContext,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def iterator(self, **kwargs: Any) -> ResourceCollection: ...
    def all(self) -> ResourceCollection: ...
    def filter(self, **kwargs: Any) -> ResourceCollection: ...
    def limit(self, count: int) -> ResourceCollection: ...
    def page_size(self, count: InterruptedError) -> ResourceCollection: ...
    def pages(self) -> List[ServiceResource]: ...

class CollectionFactory:
    def load_from_definition(
        self,
        resource_name: str,
        collection_model: Collection,
        service_context: ServiceContext,
        event_emitter: HierarchicalEmitter,
    ) -> CollectionManager: ...
