"Helper functions for serverlessrepo service"

from typing import Any, Dict, Union
import boto3
from boto3.session import Session
from botocore.config import Config
from mypy_boto3_serverlessrepo.client import Client
from mypy_boto3_serverlessrepo.paginator import (
    ListApplicationDependenciesPaginator,
    ListApplicationVersionsPaginator,
    ListApplicationsPaginator,
)

# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
def boto3_client(
    session: Session = None,
    region_name: str = None,
    api_version: str = None,
    use_ssl: bool = None,
    verify: Union[str, bool] = None,
    endpoint_url: str = None,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    aws_session_token: str = None,
    config: Config = None,
) -> Client:
    """
    Equivalent of `boto3.client('serverlessrepo')`, returns a correct type.
    """
    kwargs: Dict[str, Any] = {}
    if region_name is not None:
        kwargs["region_name"] = region_name
    if api_version is not None:
        kwargs["api_version"] = api_version
    if use_ssl is not None:
        kwargs["use_ssl"] = use_ssl
    if verify is not None:
        kwargs["verify"] = verify
    if endpoint_url is not None:
        kwargs["endpoint_url"] = endpoint_url
    if aws_access_key_id is not None:
        kwargs["aws_access_key_id"] = aws_access_key_id
    if aws_secret_access_key is not None:
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if aws_session_token is not None:
        kwargs["aws_session_token"] = aws_session_token
    if config is not None:
        kwargs["config"] = config
    if session is not None:
        return session.client("serverlessrepo", **kwargs)
    return boto3.client("serverlessrepo", **kwargs)


# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
def get_list_application_dependencies_paginator(
    client: Client,
) -> ListApplicationDependenciesPaginator:
    """
    Equivalent of `client.get_paginator('list_application_dependencies')`, returns a correct type.
    """
    return client.get_paginator("list_application_dependencies")


# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
def get_list_application_versions_paginator(
    client: Client,
) -> ListApplicationVersionsPaginator:
    """
    Equivalent of `client.get_paginator('list_application_versions')`, returns a correct type.
    """
    return client.get_paginator("list_application_versions")


# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
def get_list_applications_paginator(client: Client) -> ListApplicationsPaginator:
    """
    Equivalent of `client.get_paginator('list_applications')`, returns a correct type.
    """
    return client.get_paginator("list_applications")