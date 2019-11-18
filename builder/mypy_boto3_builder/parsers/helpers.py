"""
Helpers for parsing methods and attributes.
"""
import inspect
from typing import List, Dict, Any
from types import FunctionType

from boto3.resources.base import ServiceResource as Boto3ServiceResource

from mypy_boto3_builder.structures.method import Method
from mypy_boto3_builder.structures.attribute import Attribute
from mypy_boto3_builder.docstring_parser import DocstringParser
from mypy_boto3_builder.utils.strings import clean_doc, get_class_prefix


def get_public_methods(inspect_class: Any) -> Dict[str, FunctionType]:
    """
    Extract public methods from any class.

    Arguments:
        inspect_class -- Inspect class.

    Returns:
        A dictionary of method name and method.
    """
    class_members = inspect.getmembers(inspect_class)
    methods: Dict[str, FunctionType] = {}
    for name, member in class_members:
        if not inspect.ismethod(member):
            continue

        if name.startswith("_"):
            continue

        methods[name] = member

    return methods


def parse_attributes(resource: Boto3ServiceResource) -> List[Attribute]:
    """
    Extract attributes from boto3 resource.

    Arguments:
        resource -- boto3 service resource.

    Returns:
        A list of Attribute structures.
    """
    result: List[Attribute] = []
    service_model = resource.meta.client.meta.service_model
    if resource.meta.resource_model.shape:
        shape = service_model.shape_for(resource.meta.resource_model.shape)
        attributes = resource.meta.resource_model.get_attributes(shape)
        for name, attribute in attributes.items():
            result.append(
                Attribute(name, DocstringParser.parse_type(attribute[1].type_name))
            )

    return result


def parse_method(parent_name: str, name: str, method: FunctionType) -> Method:
    """
    Parse method to a structure.

    Arguments:
        parent_name -- Parent class name.
        method -- Inspect method.

    Returns:
        Method structure.
    """
    prefix = f"{get_class_prefix(parent_name)}{get_class_prefix(name)}"
    docstring_parser = DocstringParser()
    doc = inspect.getdoc(method) or ""
    arguments = docstring_parser.get_function_arguments(method)
    return_type = docstring_parser.NONE_ANNOTATION
    if doc:
        doc = clean_doc(doc)
        docstring_parser.enrich_arguments(doc, arguments, prefix)
        return_type = docstring_parser.get_return_type(doc, prefix)
    else:
        docless_arguments = docstring_parser.get_docless_method_arguments(name)
        if docless_arguments:
            arguments = docless_arguments

    return Method(
        name=name, arguments=arguments, docstring=doc, return_type=return_type,
    )