"""
Boto3 client Waiter.
"""
from dataclasses import dataclass, field
from typing import List
from typing_extensions import overload

from botocore.waiter import Waiter as Boto3Waiter

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
class Waiter(ClassRecord):
    """
    Boto3 client Waiter.
    """

    waiter_name: str = "waiter_name"
    boto3_waiter: Boto3Waiter = None
    bases: List[FakeAnnotation] = field(
        default_factory=lambda: [TypeClass(Boto3Waiter, alias="Boto3Waiter")]
    )

    def get_import_record(self) -> InternalImportRecord:
        return InternalImportRecord(
            source=ServiceModuleName.waiter.value, name=self.name,
        )

    def get_client_method(self) -> Method:
        return Method(
            name="get_waiter",
            docstring=f"Get Waiter `{self.waiter_name}`.",
            decorators=[TypeAnnotation(overload)],
            arguments=[
                Argument("self"),
                Argument("waiter_name", TypeLiteral(self.waiter_name)),
            ],
            return_type=InternalImport(self.name, module_name=ServiceModuleName.waiter),
        )