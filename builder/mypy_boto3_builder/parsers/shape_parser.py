from typing import Dict, List, Any

from boto3.session import Session
from botocore.exceptions import UnknownServiceError
from botocore import xform_name
from botocore.session import Session as BotocoreSession
from botocore.model import (
    Shape,
    OperationModel,
    ServiceModel,
    StructureShape,
    MapShape,
    ListShape,
    StringShape,
)

from mypy_boto3_builder.service_name import ServiceName, ServiceNameCatalog
from mypy_boto3_builder.structures.argument import Argument
from mypy_boto3_builder.structures.method import Method
from mypy_boto3_builder.import_helpers.import_string import ImportString
from mypy_boto3_builder.type_annotations.fake_annotation import FakeAnnotation
from mypy_boto3_builder.type_annotations.type import Type
from mypy_boto3_builder.type_annotations.type_subscript import TypeSubscript
from mypy_boto3_builder.type_annotations.type_literal import TypeLiteral
from mypy_boto3_builder.type_annotations.external_import import ExternalImport
from mypy_boto3_builder.type_annotations.internal_import import InternalImport
from mypy_boto3_builder.type_annotations.type_typed_dict import TypeTypedDict
from mypy_boto3_builder.logger import get_logger
from mypy_boto3_builder.type_maps.operation_type_map import get_argument_type_stub
from mypy_boto3_builder.type_maps.typed_dicts import (
    waiter_config_type,
    paginator_config_type,
)


class ShapeParserError(Exception):
    pass


class ShapeParser:
    SHAPE_TYPE_MAP = {
        "integer": Type.int,
        "long": Type.int,
        "boolean": Type.bool,
        "double": Type.float,
        "float": Type.float,
        "timestamp": ExternalImport(ImportString("datetime"), "datetime"),
        "blob": TypeSubscript(Type.Union, [Type.bytes, Type.IO]),
    }

    def _patch_service_model(self) -> None:
        if self.service_name is ServiceNameCatalog.cloudsearchdomain:
            operation = self._get_operation("Search")
            self._rename_input_member(operation, "return", "returnFields")
        if self.service_name is ServiceNameCatalog.logs:
            operation = self._get_operation("CreateExportTask")
            self._rename_input_member(operation, "from", "fromTime")
        if self.service_name is ServiceNameCatalog.ec2:
            for operation_name in self._get_operation_names():
                operation = self._get_operation(operation_name)
                try:
                    self._rename_input_member(operation, "Filter", "Filters")
                except KeyError:
                    continue
        if self.service_name is ServiceNameCatalog.s3:
            operation_names = [
                # "DeleteObjects",
                "PutBucketAcl",
                "PutBucketCors",
                "PutBucketLifecycle",
                "PutBucketLogging",
                "PutBucketNotification",
                "PutBucketPolicy",
                "PutBucketReplication",
                "PutBucketRequestPayment",
                "PutBucketTagging",
                "PutBucketVersioning",
                "PutBucketWebsite",
                "PutObjectAcl",
            ]
            for operation_name in operation_names:
                operation = self._get_operation(operation_name)
                self._delete_input_member(operation, "ContentMD5")

    def __init__(self, session: Session, service_name: ServiceName):
        loader = session._loader  # pylint: disable=protected-access
        botocore_session: BotocoreSession = session._session  # pylint: disable=protected-access
        service_data = botocore_session.get_service_data(service_name.boto3_name)
        self.service_name = service_name
        self.service_model = ServiceModel(service_data, service_name.boto3_name)
        self._typed_dict_map: Dict[str, TypeTypedDict] = {}
        self._patch_service_model()
        self._waiters_shape: Shape = {}
        try:
            self._waiters_shape = loader.load_service_model(
                service_name.boto3_name, "waiters-2"
            )
        except UnknownServiceError:
            pass
        self._paginators_shape: Shape = {}
        try:
            self._paginators_shape = loader.load_service_model(
                service_name.boto3_name, "paginators-1"
            )
        except UnknownServiceError:
            pass
        self._resources_shape: Shape = {}
        try:
            self._resources_shape = loader.load_service_model(
                service_name.boto3_name, "resources-1"
            )
        except UnknownServiceError:
            pass

        self.logger = get_logger()

    def _get_shape(self, name: str) -> Shape:
        return self.service_model.shape_for(name)

    def _get_operation(self, name: str) -> OperationModel:
        return self.service_model.operation_model(name)

    def _get_operation_names(self) -> List[str]:
        return list(
            self.service_model.operation_names
        )  # pylint: disable=not-an-iterable

    @staticmethod
    def _rename_input_member(
        operation: OperationModel, old_name: str, new_name: str
    ) -> None:
        members = operation.input_shape.members
        members[new_name] = members[old_name]
        del members[old_name]

    @staticmethod
    def _delete_input_member(operation: OperationModel, name: str) -> None:
        members = operation.input_shape.members
        del members[name]

    def _get_paginator(self, name: str) -> Shape:
        try:
            return self._paginators_shape["pagination"][name]
        except KeyError:
            raise ShapeParserError(f"Unknown paginator: {name}")

    def _get_service_resource(self) -> Shape:
        return self._resources_shape["service"]

    def _get_resource_shape(self, name: str) -> Shape:
        try:
            return self._resources_shape["resources"][name]
        except KeyError:
            raise ShapeParserError(f"Unknown resource: {name}")

    def _get_resource_collection_shape(self, resouce_name: str, name: str) -> Shape:
        try:
            return self._get_resource_shape(resouce_name)["hasMany"][name]
        except KeyError:
            raise ShapeParserError(
                f"Unknown resource collection: {resouce_name}.{name}"
            )

    def _get_resource_action_shape(self, resouce_name: str, name: str) -> Shape:
        try:
            return self._get_resource_shape(resouce_name)["actions"][name]
        except KeyError:
            raise ShapeParserError(f"Unknown resource action: {resouce_name}.{name}")

    def get_paginator_names(self) -> List[str]:
        result: List[str] = []
        for name in self._paginators_shape.get("pagination", []):
            result.append(name)
        result.sort()
        return result

    def _parse_arguments(self, shape: StructureShape) -> List[Argument]:
        operation_name = shape.name

        result: List[Argument] = []
        required = shape.required_members
        for argument_name, argument_shape in shape.members.items():
            argument_type_stub = get_argument_type_stub(operation_name, argument_name)
            if argument_type_stub is not None:
                argument_type = argument_type_stub
            else:
                argument_type = self._parse_shape(argument_shape)
            argument = Argument(argument_name, argument_type)
            if argument_name not in required:
                argument.default = Type.none
            result.append(argument)

        result.sort(key=lambda x: not x.required)
        return result

    def _parse_return_type(self, shape: Shape) -> FakeAnnotation:
        return self._parse_shape(shape)

    def get_client_method_map(self) -> Dict[str, Method]:
        result: Dict[str, Method] = {
            "can_paginate": Method(
                "can_paginate",
                [Argument("self", None), Argument("operation_name", Type.str)],
                Type.bool,
            )
        }
        for operation_name in self._get_operation_names():
            operation_model = self._get_operation(operation_name)
            return_type: FakeAnnotation = Type.none
            arguments: List[Argument] = [Argument("self", None)]

            if operation_model.input_shape is not None:
                arguments.extend(self._parse_arguments(operation_model.input_shape))

            if operation_model.output_shape is not None:
                return_type = self._parse_return_type(operation_model.output_shape)

            method_name = xform_name(operation_name)
            method = Method(
                name=method_name, arguments=arguments, return_type=return_type
            )
            result[method.name] = method

        return result

    @staticmethod
    def _parse_shape_string(shape: StringShape) -> FakeAnnotation:
        if not shape.enum:
            return Type.str

        type_literal = TypeLiteral()
        for option in shape.enum:
            type_literal.add_literal_child(option)

        return type_literal

    def _parse_shape_map(self, shape: MapShape) -> FakeAnnotation:
        type_subscript = TypeSubscript(Type.Dict)
        if shape.key:
            type_subscript.add_child(self._parse_shape(shape.key))
        else:
            type_subscript.add_child(Type.str)
        if shape.value:
            type_subscript.add_child(self._parse_shape(shape.value))
        else:
            type_subscript.add_child(Type.Any)
        return type_subscript

    def _parse_shape_structure(self, shape: StructureShape) -> FakeAnnotation:
        if not shape.members.items():
            return TypeSubscript(Type.Dict, [Type.str, Type.Any])

        required = shape.required_members
        typed_dict_name = f"{shape.name}TypeDef"
        if typed_dict_name in self._typed_dict_map:
            return self._typed_dict_map[typed_dict_name]
        typed_dict = TypeTypedDict(typed_dict_name)
        self._typed_dict_map[typed_dict_name] = typed_dict
        for attr_name, attr_shape in shape.members.items():
            typed_dict.add_attribute(
                attr_name, self._parse_shape(attr_shape), attr_name in required,
            )
        return typed_dict

    def _parse_shape_list(self, shape: ListShape) -> FakeAnnotation:
        type_subscript = TypeSubscript(Type.List)
        if shape.member:
            type_subscript.add_child(self._parse_shape(shape.member))
        else:
            type_subscript.add_child(Type.Any)
        return type_subscript

    def _parse_shape(self, shape: Shape) -> FakeAnnotation:
        if shape.type_name in self.SHAPE_TYPE_MAP:
            return self.SHAPE_TYPE_MAP[shape.type_name]

        if isinstance(shape, StringShape):
            return self._parse_shape_string(shape)

        if isinstance(shape, MapShape):
            return self._parse_shape_map(shape)

        if isinstance(shape, StructureShape):
            return self._parse_shape_structure(shape)

        if isinstance(shape, ListShape):
            return self._parse_shape_list(shape)

        if shape.type_name in self._resources_shape["resources"]:
            return InternalImport(shape.type_name)

        self.logger.warning(f"Unknown shape: {shape}")
        return Type.Any

    def get_paginate_method(self, paginator_name: str) -> Method:
        operation_name = paginator_name
        paginator_shape = self._get_paginator(paginator_name)
        operation_shape = self._get_operation(operation_name)
        skip_argument_names: List[str] = []
        input_token = paginator_shape["input_token"]
        if isinstance(input_token, list):
            skip_argument_names.extend(input_token)
        else:
            skip_argument_names.append(input_token)
        if "limit_key" in paginator_shape:
            skip_argument_names.append(paginator_shape["limit_key"])

        arguments: List[Argument] = [Argument("self", None)]

        if operation_shape.input_shape is not None:
            for argument in self._parse_arguments(operation_shape.input_shape):
                if argument.name in skip_argument_names:
                    continue
                arguments.append(argument)

        arguments.append(Argument("PaginationConfig", paginator_config_type, Type.none))

        return_type: FakeAnnotation = Type.none
        if operation_shape.output_shape is not None:
            return_type = self._parse_return_type(operation_shape.output_shape)

        return Method("paginate", arguments, return_type)

    def get_wait_method(self, waiter_name: str) -> Method:
        operation_name = self._waiters_shape["waiters"][waiter_name]["operation"]
        operation_shape = self._get_operation(operation_name)

        arguments: List[Argument] = [Argument("self", None)]

        if operation_shape.input_shape is not None:
            arguments.extend(self._parse_arguments(operation_shape.input_shape))

        arguments.append(Argument("WaiterConfig", waiter_config_type, Type.none))

        return Method(name="wait", arguments=arguments, return_type=Type.none)

    def get_service_resource_method_map(self) -> Dict[str, Method]:
        result: Dict[str, Method] = {}
        service_resource_shape = self._get_service_resource()
        for action_name, action_shape in service_resource_shape.get(
            "actions", {}
        ).items():
            method = self._get_resource_method(action_name, action_shape)
            result[method.name] = method

        return result

    def get_resource_method_map(self, resource_name: str) -> Dict[str, Method]:
        resource_shape = self._get_resource_shape(resource_name)
        result: Dict[str, Method] = {
            "get_available_subresources": Method(
                "get_available_subresources",
                [Argument("self", None)],
                TypeSubscript(Type.List, [Type.str]),
            ),
            "load": Method("load", [Argument("self", None)], Type.none),
            "reload": Method("reload", [Argument("self", None)], Type.none),
        }

        for action_name, action_shape in resource_shape.get("actions", {}).items():
            method = self._get_resource_method(action_name, action_shape)
            result[method.name] = method

        for waiter_name in resource_shape.get("waiters", {}):
            method = Method(
                f"wait_until_{xform_name(waiter_name)}",
                [Argument("self", None)],
                Type.none,
            )
            result[method.name] = method

        return result

    def _get_resource_method(
        self, action_name: str, action_shape: Dict[str, Any]
    ) -> Method:
        return_type: FakeAnnotation = Type.none
        arguments: List[Argument] = [Argument("self", None)]
        if "resource" in action_shape:
            return_type = self._parse_return_type(
                Shape("resource", action_shape["resource"])
            )

        if "request" in action_shape:
            operation_shape = self._get_operation(action_shape["request"]["operation"])
            skip_argument_names: List[str] = [
                i["target"]
                for i in action_shape["request"].get("params", {})
                if i["source"] == "identifier"
            ]
            if operation_shape.input_shape is not None:
                for argument in self._parse_arguments(operation_shape.input_shape):
                    if argument.name not in skip_argument_names:
                        arguments.append(argument)
            if operation_shape.output_shape is not None:
                return_type = self._parse_shape(operation_shape.output_shape)

        return Method(
            name=xform_name(action_name), arguments=arguments, return_type=return_type
        )