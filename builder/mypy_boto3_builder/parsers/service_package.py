"""
Parser that produces `structures.ServiceModule`.
"""
import inspect
from typing import Iterable, Union
from typing_extensions import Literal

from boto3.session import Session
from botocore import xform_name
from botocore.paginate import Paginator as Boto3Paginator
from botocore.waiter import Waiter as Boto3Waiter
from botocore.config import Config as Boto3Config

from mypy_boto3_builder.structures.method import Method
from mypy_boto3_builder.structures.function import Function
from mypy_boto3_builder.structures.waiter import Waiter
from mypy_boto3_builder.structures.paginator import Paginator
from mypy_boto3_builder.structures.service_package import ServicePackage
from mypy_boto3_builder.structures.argument import Argument
from mypy_boto3_builder.enums.service_name import ServiceName
from mypy_boto3_builder.enums.service_module_name import ServiceModuleName
from mypy_boto3_builder.type_annotations.type_class import TypeClass
from mypy_boto3_builder.type_annotations.external_import import ExternalImport
from mypy_boto3_builder.type_annotations.type_constant import TypeConstant
from mypy_boto3_builder.type_annotations.type_subscript import TypeSubscript
from mypy_boto3_builder.import_helpers.import_string import ImportString
from mypy_boto3_builder.utils.strings import clean_doc
from mypy_boto3_builder.parsers.client import parse_client
from mypy_boto3_builder.parsers.service_resource import parse_service_resource
from mypy_boto3_builder.parsers.helpers import get_public_methods, parse_method
from mypy_boto3_builder.parsers.boto3_utils import get_boto3_client


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
    client = parse_client(session, service_name)
    result = ServicePackage(
        name=service_name.module_name,
        pypi_name=service_name.pypi_name,
        service_name=service_name,
        client=client,
        service_resource=parse_service_resource(session, service_name),
    )

    for waiter_name in client.boto3_client.waiter_names:
        waiter = client.boto3_client.get_waiter(waiter_name)
        public_methods = get_public_methods(waiter)
        methods = [
            parse_method(waiter_name, method_name, method)
            for method_name, method in public_methods.items()
        ]
        result.waiters.append(
            Waiter(
                name=f"{waiter.name}Waiter",
                waiter_name=waiter_name,
                boto3_waiter=waiter,
                docstring=f"Waiter for `{waiter_name}` name.",
                methods=methods,
            )
        )

    session_loader = session._loader  # pylint: disable=protected-access
    if service_name.boto3_name in session_loader.list_available_services(
        "paginators-1"
    ):
        session_client = get_boto3_client(session, service_name)

        botocore_session = session._session  # pylint: disable=protected-access
        service_paginator_model = botocore_session.get_paginator_model(
            service_name.boto3_name
        )
        paginator_config = (
            service_paginator_model._paginator_config  # pylint: disable=protected-access
        )
        for paginator_name in sorted(paginator_config):
            operation_name = xform_name(paginator_name)
            paginator = session_client.get_paginator(operation_name)
            public_methods = get_public_methods(paginator)
            methods = [
                parse_method(paginator_name, method_name, method)
                for method_name, method in public_methods.items()
            ]
            paginator_model = paginator._model  # pylint: disable=protected-access
            result.paginators.append(
                Paginator(
                    name=f"{paginator_model.name}Paginator",
                    operation_name=operation_name,
                    boto3_paginator=paginator,
                    docstring=f"Paginator for `{operation_name}`",
                    methods=methods,
                )
            )

    if result.paginators:
        for paginator in result.paginators:
            result.client.methods.append(paginator.get_client_method())
        result.client.methods.append(
            Method(
                name="get_paginator",
                docstring=clean_doc(inspect.getdoc(client.boto3_client.get_paginator)),
                arguments=[
                    Argument("self", None),
                    Argument("operation_name", TypeClass(str)),
                ],
                return_type=TypeClass(Boto3Paginator, alias="Boto3Paginator"),
            )
        )

    if result.waiters:
        for waiter in result.waiters:
            result.client.methods.append(waiter.get_client_method())
        result.client.methods.append(
            Method(
                name="get_waiter",
                docstring=clean_doc(inspect.getdoc(client.boto3_client.get_waiter)),
                arguments=[
                    Argument("self", None),
                    Argument("waiter_name", TypeClass(str)),
                ],
                return_type=TypeClass(Boto3Waiter, alias="Boto3Waiter"),
            )
        )

    result.typed_dicts = result.extract_typed_dicts(result.get_types(), {})
    helper_arguments = [
        Argument("session", TypeClass(Session), TypeConstant(None)),
        Argument("region_name", TypeClass(str), TypeConstant(None)),
        Argument("api_version", TypeClass(str), TypeConstant(None)),
        Argument("use_ssl", TypeClass(bool), TypeConstant(None)),
        Argument(
            "verify",
            TypeSubscript(Union, [TypeClass(str), TypeClass(bool)]),
            TypeConstant(None),
        ),
        Argument("endpoint_url", TypeClass(str), TypeConstant(None)),
        Argument("aws_access_key_id", TypeClass(str), TypeConstant(None)),
        Argument("aws_secret_access_key", TypeClass(str), TypeConstant(None)),
        Argument("aws_session_token", TypeClass(str), TypeConstant(None)),
        Argument("config", TypeClass(Boto3Config), TypeConstant(None)),
    ]
    client_helper = Function(
        name="boto3_client",
        docstring=f"Equivalent of `boto3.client('{service_name.boto3_name}')`, returns a correct type.",
        arguments=helper_arguments,
        return_type=ExternalImport(
            ImportString(service_name.module_name, ServiceModuleName.client.name),
            result.client.name,
        ),
        body=get_helper_body(helper_arguments, "client", service_name),
    )
    result.helper_functions.append(client_helper)
    if result.service_resource:
        resource_helper = Function(
            name="boto3_resource",
            docstring=f"Equivalent of `boto3.resource('{service_name.boto3_name}')`, returns a correct type.",
            arguments=helper_arguments,
            return_type=ExternalImport(
                ImportString(
                    service_name.module_name, ServiceModuleName.service_resource.name
                ),
                result.service_resource.name,
            ),
            body=get_helper_body(helper_arguments, "resource", service_name),
        )
        result.helper_functions.append(resource_helper)

    for paginator in result.paginators:
        result.helper_functions.append(
            Function(
                name=f"get_{paginator.operation_name}_paginator",
                docstring=f"Equivalent of `client.get_paginator('{paginator.operation_name}')`, returns a correct type.",
                arguments=[
                    Argument(
                        name="client",
                        type=ExternalImport(
                            ImportString(
                                service_name.module_name, ServiceModuleName.client.name
                            ),
                            result.client.name,
                        ),
                    )
                ],
                return_type=ExternalImport(
                    ImportString(
                        service_name.module_name, ServiceModuleName.paginator.name
                    ),
                    paginator.name,
                ),
                body=f"return client.get_paginator('{paginator.operation_name}')",
            )
        )

    for waiter in result.waiters:
        result.helper_functions.append(
            Function(
                name=f"get_{waiter.waiter_name}_waiter",
                docstring=f"Equivalent of `client.get_waiter('{waiter.waiter_name}')`, returns a correct type.",
                arguments=[
                    Argument(
                        name="client",
                        type=ExternalImport(
                            ImportString(
                                service_name.module_name, ServiceModuleName.client.name
                            ),
                            result.client.name,
                        ),
                    )
                ],
                return_type=ExternalImport(
                    ImportString(
                        service_name.module_name, ServiceModuleName.waiter.name
                    ),
                    waiter.name,
                ),
                body=f"return client.get_waiter('{waiter.waiter_name}')",
            )
        )

    return result


def get_helper_body(
    arguments: Iterable[Argument],
    function_name: Literal["resource", "client"],
    service_name: ServiceName,
) -> str:
    helper_body_lines = [
        "kwargs: Dict[str, Any] = {}",
    ]
    for argument in arguments:
        if argument.name == "session":
            continue
        helper_body_lines.append(f"if {argument.name} is not None:")
        helper_body_lines.append(f'    kwargs["{argument.name}"] = {argument.name}')
    helper_body_lines.append("if session is not None:")
    helper_body_lines.append(
        f"    return session.{function_name}('{service_name.boto3_name}', **kwargs)"
    )
    helper_body_lines.append(
        f"return boto3.{function_name}('{service_name.boto3_name}', **kwargs)"
    )
    return "\n".join(helper_body_lines)