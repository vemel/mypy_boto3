"""
Parser that produces `structures.ServiceModule`.
"""

from boto3.session import Session
from botocore import xform_name

from mypy_boto3_builder.structures.waiter import Waiter
from mypy_boto3_builder.structures.paginator import Paginator
from mypy_boto3_builder.structures.service_package import ServicePackage
from mypy_boto3_builder.service_name import ServiceName
from mypy_boto3_builder.parsers.client import parse_client
from mypy_boto3_builder.parsers.service_resource import parse_service_resource
from mypy_boto3_builder.parsers.helpers import get_public_methods, parse_method
from mypy_boto3_builder.parsers.boto3_utils import get_boto3_client
from mypy_boto3_builder.parsers.shape_parser import ShapeParser
from mypy_boto3_builder.logger import get_logger


def parse_service_package(
    session: Session, service_name: ServiceName
) -> ServicePackage:
    """
    Extract all data from boto3 service package.

    Arguments:
        session -- boto3 session.
        service_name -- Target service name.

    Returns:
        ServiceModule structure.
    """
    logger = get_logger()
    session_loader = session._loader  # pylint: disable=protected-access
    service_shape = session_loader.load_service_model(
        service_name.boto3_name, "service-2"
    )
    logger.debug("Parsing Client")
    shape_parser = ShapeParser(service_shape)
    client = parse_client(session, service_name, shape_parser)
    service_resource = parse_service_resource(session, service_name)

    result = ServicePackage(
        name=service_name.module_name,
        pypi_name=service_name.pypi_name,
        service_name=service_name,
        client=client,
        service_resource=service_resource,
    )

    for waiter_name in client.boto3_client.waiter_names:
        logger.debug(f"Parsing Waiter {waiter_name}")
        waiter = client.boto3_client.get_waiter(waiter_name)
        waiter_record = Waiter(
            name=f"{waiter.name}Waiter",
            docstring=(
                f"[Waiter.{waiter.name} documentation]"
                f"({service_name.doc_link}.Waiter.{waiter.name})"
            ),
            waiter_name=waiter_name,
            boto3_waiter=waiter,
        )
        public_methods = get_public_methods(waiter)
        for method_name, public_method in public_methods.items():
            method = parse_method(waiter_name, method_name, public_method)
            method.docstring = (
                f"[{waiter.name}.{method_name} documentation]"
                f"({service_name.doc_link}.Waiter.{waiter.name}.{method_name})"
            )
            waiter_record.methods.append(method)
        result.waiters.append(waiter_record)

    if service_name.boto3_name in session_loader.list_available_services(
        "paginators-1"
    ):
        session_client = get_boto3_client(session, service_name)
        paginator_config = session_loader.load_service_model(
            service_name.boto3_name, "paginators-1", None
        )["pagination"]
        for paginator_name in sorted(paginator_config):
            logger.debug(f"Parsing Paginator {paginator_name}")
            operation_name = xform_name(paginator_name)
            paginator = session_client.get_paginator(operation_name)
            paginator_record = Paginator(
                name=f"{paginator_name}Paginator",
                operation_name=operation_name,
                boto3_paginator=paginator,
                docstring=(
                    f"[Paginator.{paginator_name} documentation]"
                    f"({service_name.doc_link}.Paginator.{paginator_name})"
                ),
            )
            public_methods = get_public_methods(paginator)
            for method_name, public_method in public_methods.items():
                method = parse_method(paginator_name, method_name, public_method)
                method.docstring = (
                    f"[{paginator_name}.{method_name} documentation]"
                    f"({service_name.doc_link}.Paginator.{paginator_name}.{method_name})"
                )
                paginator_record.methods.append(method)
            result.paginators.append(paginator_record)

    for paginator in result.paginators:
        method = paginator.get_client_method()
        result.client.methods.append(method)

    for waiter in result.waiters:
        method = waiter.get_client_method()
        result.client.methods.append(method)

    result.typed_dicts = result.extract_typed_dicts(result.get_types(), {})

    return result
