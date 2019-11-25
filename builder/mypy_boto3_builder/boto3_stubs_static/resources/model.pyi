# pylint: disable=unused-argument,multiple-statements,super-init-not-called,no-self-use,unused-import
from __future__ import annotations

import logging
from typing import Optional, Dict, Any, List, Union, Tuple
from typing_extensions import Literal, TypedDict

from botocore import xform_name
from botocore.model import Shape

logger: logging.Logger

ActionDefinition = TypedDict(
    "ActionDefinition", {"request": Dict, "resource": Dict, "path": str}, total=False
)
DefinitionWithParamsDefinition = TypedDict(
    "DefinitionWithParamsDefinition", {"params": List[Dict]}, total=False
)
RequestDefinition = TypedDict("RequestDefinition", {"operation": str}, total=False)
WaiterDefinition = TypedDict("WaiterDefinition", {"waiterName": str}, total=False)
ResponseResourceDefinition = TypedDict(
    "ResponseResourceDefinition", {"type": str, "path": str}, total=False
)
ResourceModelDefinition = TypedDict(
    "ResourceModelDefinition", {"shape": str}, total=False
)

class Identifier:
    def __init__(self, name: str, member_name: Optional[str] = None) -> None: ...

class Action:
    def __init__(
        self, name: str, definition: ActionDefinition, resource_defs: Dict[str, Dict]
    ) -> None: ...

class DefinitionWithParams:
    def __init__(self, definition: DefinitionWithParamsDefinition) -> None: ...
    @property
    def params(self) -> List[Parameter]: ...

class Parameter:
    def __init__(
        self,
        target: str,
        source: str,
        name: str = None,
        path: str = None,
        value: Union[str, int, float, bool] = None,
        **kwargs: Any
    ) -> None: ...

class Request(DefinitionWithParams):
    def __init__(self, definition: RequestDefinition) -> None: ...

class Waiter(DefinitionWithParams):
    PREFIX: Literal["WaitUntil"]
    def __init__(self, name: str, definition: WaiterDefinition) -> None: ...

class ResponseResource:
    def __init__(
        self, definition: ResponseResourceDefinition, resource_defs: Dict[str, Dict]
    ) -> None: ...
    @property
    def identifiers(self) -> List[Identifier]: ...
    @property
    def model(self) -> ResourceModel: ...

class Collection(Action):
    @property
    def batch_actions(self) -> List[Action]: ...

class ResourceModel(object):
    def __init__(
        self,
        name: str,
        definition: ResourceModelDefinition,
        resource_defs: Dict[str, Dict],
    ) -> None: ...
    def load_rename_map(self, shape: Optional[Shape] = None) -> None: ...
    def get_attributes(self, shape: Shape) -> Dict[str, Tuple[str, Any]]: ...
    @property
    def identifiers(self) -> List[Identifier]: ...
    @property
    def load(self) -> Optional[Action]: ...
    @property
    def actions(self) -> List[Action]: ...
    @property
    def batch_actions(self) -> List[Action]: ...
    @property
    def subresources(self) -> List[ResponseResource]: ...
    @property
    def references(self) -> List[ResponseResource]: ...
    @property
    def collections(self) -> List[Collection]: ...
    @property
    def waiters(self) -> List[Waiter]: ...
