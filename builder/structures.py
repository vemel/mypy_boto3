from typing import List, Union, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Attribute:
    name: str
    type: Union[type, Tuple, str]

    def get_types(self):
        types = set()
        if not isinstance(self.type, tuple):
            types.add(self.type)
        else:
            for t in self.type:
                types.add(t)
        return types


@dataclass
class Argument:
    name: str
    type: Union[type, Tuple, str]
    required: bool
    types = set()

    def get_types(self):
        types = set()
        if not self.required:
            types.add(Optional)
        if not isinstance(self.type, tuple):
            types.add(self.type)
        else:
            for t in self.type:
                types.add(t)
        return types


@dataclass
class Method:
    name: str
    arguments: List[Argument]
    docstring: str
    return_type: Union[type, Tuple, str]

    def get_types(self):
        types = set()
        for argument in self.arguments:
            types.update(argument.get_types())
        return types


class TypeCollector:
    def get_types(self):
        types = set()
        if hasattr(self, "methods"):
            for method in getattr(self, "methods"):
                types.update(method.get_types())
        if hasattr(self, "attributes"):
            for attribute in getattr(self, "attributes"):
                types.update(attribute.get_types())
        if hasattr(self, "sub_resources"):
            for sub_resource in getattr(self, "sub_resources"):
                types.update(sub_resource.get_types())
        if hasattr(self, "collections"):
            for collection in getattr(self, "collections"):
                types.update(collection.get_types())
        if hasattr(self, "waiters"):
            for waiter in getattr(self, "waiters"):
                types.update(waiter.get_types())
        if hasattr(self, "paginators"):
            for paginator in getattr(self, "paginators"):
                types.update(paginator.get_types())
        return types


@dataclass
class Collection(TypeCollector):
    name: str
    methods: List[Method]


@dataclass
class Resource(TypeCollector):
    name: str
    methods: List[Method]
    attributes: List[Attribute]
    collections: List[Collection]


@dataclass
class Waiter(TypeCollector):
    name: str
    methods: List[Method]


@dataclass
class Paginator(TypeCollector):
    name: str
    methods: List[Method]


@dataclass
class ServiceResource(TypeCollector):
    name: str
    methods: List[Method]
    attributes: List[Attribute]
    collections: List[Collection]
    sub_resources: List[Resource]


@dataclass
class Client(TypeCollector):
    name: str
    methods: List[Method]


@dataclass
class ServiceWaiter(TypeCollector):
    name: str
    waiters: List[Waiter]


@dataclass
class ServicePaginator(TypeCollector):
    name: str
    paginators: List[Paginator]


@dataclass
class Config:
    services: List
    with_docs: bool
    with_clients: bool
    with_service_resources: bool
    with_paginators: bool
    with_waiters: bool
    package_name: str
    module_name: str
