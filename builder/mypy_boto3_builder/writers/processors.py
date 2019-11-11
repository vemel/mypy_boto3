from pathlib import Path
from typing import Iterable

from boto3.session import Session

from mypy_boto3_builder.version import __version__ as version
from mypy_boto3_builder.parsers import (
    parse_boto3_module,
    parse_master_module,
    parse_service_module,
)
from mypy_boto3_builder.structures import (
    Boto3Module,
    MasterModule,
    ServiceModule,
)
from mypy_boto3_builder.nice_path import NicePath
from mypy_boto3_builder.service_name import ServiceName
from mypy_boto3_builder.logger import get_logger
from mypy_boto3_builder.writers.boto3_stubs import write_boto3_stubs_module
from mypy_boto3_builder.writers.master_module import write_master_module
from mypy_boto3_builder.writers.service_module import write_service_module


logger = get_logger()


def process_boto3_stubs(
    session: Session, service_names: Iterable[ServiceName], output_path: Path,
) -> Boto3Module:
    logger.debug(f"Parsing boto3")
    boto3_module = parse_boto3_module(session, service_names)
    logger.debug(f"Writing boto3 stubs to {NicePath(output_path)}")

    write_boto3_stubs_module(boto3_module, output_path)
    return boto3_module


def process_master(
    session: Session, service_names: Iterable[ServiceName], output_path: Path,
) -> MasterModule:
    logger.debug(f"Parsing master")
    master_module = parse_master_module(session, service_names)
    logger.debug(f"Writing master to {NicePath(output_path)}")

    write_master_module(master_module, output_path)
    return master_module


def process_service(
    session: Session, service_name: ServiceName, output_path: Path,
) -> ServiceModule:
    logger.debug(f"Parsing {service_name.boto3_name}")
    service_module = parse_service_module(session, service_name)
    logger.debug(f"Writing {service_name.boto3_name} to {NicePath(output_path)}")

    write_service_module(service_module, output_path)
    return service_module