try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_ec2.client import *
except ImportError:
    raise ImportError("Install boto3-stubs[ec2] to use ec2 Client annotations")