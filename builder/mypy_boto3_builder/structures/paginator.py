"""
Boto3 client Paginator.
"""
from dataclasses import dataclass, field
from typing import List
from typing_extensions import overload

from botocore.paginate import Paginator as Boto3Paginator

from mypy_boto3_builder.import_helpers.internal_import_record import (
    InternalImportRecord,
)
from mypy_boto3_builder.enums.service_module_name import ServiceModuleName
from mypy_boto3_builder.type_annotations.fake_annotation import FakeAnnotation
from mypy_boto3_builder.type_annotations.type_annotation import TypeAnnotation
from mypy_boto3_builder.type_annotations.type_class import TypeClass
from mypy_boto3_builder.type_annotations.type_literal import TypeLiteral
from mypy_boto3_builder.type_annotations.internal_import import InternalImport
from mypy_boto3_builder.structures.class_record import ClassRecord
from mypy_boto3_builder.structures.method import Method
from mypy_boto3_builder.structures.argument import Argument


@dataclass
class Paginator(ClassRecord):
    """
    Boto3 client Paginator.
    """

    operation_name: str = "operation_name"
    boto3_paginator: Boto3Paginator = None
    bases: List[FakeAnnotation] = field(
        default_factory=lambda: [TypeClass(Boto3Paginator, alias="Boto3Paginator")]
    )

    def get_import_record(self) -> InternalImportRecord:
        return InternalImportRecord(
            source=ServiceModuleName.paginator.value, name=self.name,
        )

    def get_client_method(self) -> Method:
        return Method(
            name="get_paginator",
            docstring=f"Get Paginator for `{self.operation_name}` operation.",
            decorators=[TypeAnnotation(overload)],
            arguments=[
                Argument("self"),
                Argument("operation_name", TypeLiteral(self.operation_name)),
            ],
            return_type=InternalImport(
                self.name, module_name=ServiceModuleName.paginator
            ),
        )