"""
Wrapper for `Literal` type annotations like `Literal['a', 'b']`
"""
from __future__ import annotations

from typing import Any
from typing_extensions import Literal

from mypy_boto3_builder.import_helpers.import_record import ImportRecord
from mypy_boto3_builder.type_annotations.fake_annotation import FakeAnnotation
from mypy_boto3_builder.type_annotations.type_annotation import TypeAnnotation


class TypeLiteral(FakeAnnotation):
    """
    Wrapper for `Literal` type annotations like `Literal['a', 'b']`

    Arguments:
        children -- Literal values.
    """

    def __init__(self, *children: Any) -> None:
        self.parent = TypeAnnotation(Literal)
        self.children = children

    def render(self) -> str:
        """
        Render type annotation to a valid Python code for local usage.

        Returns:
            A string with a valid type annotation.
        """
        children = ", ".join([repr(i) for i in self.children])
        return f"{self.parent.render()}[{children}]"

    def get_import_record(self) -> ImportRecord:
        """
        Get import record required for using type annotation.
        """
        return self.parent.get_import_record()

    def copy(self) -> TypeLiteral:
        """
        Create a copy of type annotation wrapper.
        """
        return TypeLiteral(*self.children)
