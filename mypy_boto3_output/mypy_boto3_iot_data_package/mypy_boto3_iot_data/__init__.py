"Main interface for iot-data service"

from mypy_boto3_iot_data.client import Client
from mypy_boto3_iot_data.helpers import boto3_client


__all__ = ("Client", "boto3_client")