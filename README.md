# mypy_boto3

[![PyPI - Handsdown](https://img.shields.io/pypi/v/mypy-boto3.svg?color=blue&style=for-the-badge)](https://pypi.org/project/mypy-boto3)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mypy-boto3.svg?color=blue&style=for-the-badge)](https://pypi.org/project/mypy-boto3)
[![Docs](https://img.shields.io/readthedocs/mypy-boto3.svg?color=blue&style=for-the-badge)](https://mypy-boto3.readthedocs.io/)

Type annotations for [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) compatible with [mypy](https://github.com/python/mypy), [VSCode](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/) and other tools. 

Based on [boto3_type_annotations](https://github.com/alliefitter/boto3_type_annotations) by [@alliefitter](https://github.com/alliefitter).

- [mypy_boto3](#mypyboto3)
  - [Installation](#installation)
    - [Build services index manually](#build-services-index-manually)
  - [Latest changes](#latest-changes)
  - [Usage](#usage)
    - [Setup your IDE](#setup-your-ide)
    - [VSCode](#vscode)
    - [PyCharm](#pycharm)
    - [Other IDEs](#other-ides)
    - [Explicit type annotations](#explicit-type-annotations)
    - [Pylint compatibility](#pylint-compatibility)
  - [How to build](#how-to-build)
    - [Locally](#locally)
    - [With Docker image](#with-docker-image)
  - [Differences from boto3-type-annotations](#differences-from-boto3-type-annotations)
  - [Thank you](#thank-you)
  - [Sub-modules](#sub-modules)
    - [Examples](#examples)
    - [List of all sub-modules](#list-of-all-sub-modules)

## Installation

```bash
# install `boto3` type annotations
# for ec2, s3, rds, lambda, sqs, dynamo and cloudformation
# Consumes ~7 MB of space
python -m pip install boto3-stubs[essential]

# or install annotations for services you use
python -m pip install boto3-stubs[acm,apigateway]
```

### Build services index manually

This package generates a few source files depending on services that you installed.
Generation is done by a post-install script, so as long as you use `pip`, `pipfile`
or `poetry` everything should be done automatically.

However, if you use any other way and notice that services stubs do not work,
you can build services index manually.

```bash
# Use this command when you add or remove service packages
python -m mypy_boto3
```

## Latest changes

Full changelog can be found in [Releases](https://github.com/vemel/mypy_boto3/releases).

## Usage

- Install [mypy](https://github.com/python/mypy) and optionally enable it in your IDE
- Install [boto3](https://github.com/boto/boto3)
- VSCode: Use explicit types for `boto3.client`, `boto3.session.client`,
  `client.get_waiter` and `client.get_paginator` calls to enjoy code auto-complete and
  correct type hints

```python
import boto3

from mypy_boto3 import s3

# you need explicit type annotatins only if your IDE do not support
# function overloads (e.g. VSCode). For PyCharm anf mypy you do not need
# to set types explicitly
client: s3.S3Client = boto3.client("s3")

# IDE autocomplete suggests function name and arguments here
client.create_bucket(Bucket="bucket")

# (mypy) error: Missing positional argument "Key" in call to "get_object" of "S3Client"
client.get_object(Bucket="bucket")

# (mypy) error: Argument "Key" to "get_object" of "S3Client" has incompatible type "None"; expected "str"
client.get_object(Bucket="bucket", Key=None)

resource: s3.S3ServiceResource = boto3.Session(region_name="us-west-1").resource("s3")

# IDE autocomplete suggests function name and arguments here
bucket = resource.Bucket("bucket")

# (mypy) error: Unexpected keyword argument "key" for "upload_file" of "Bucket"; did you mean "Key"?
bucket.upload_file(Filename="my.txt", key="my-txt")

# waiters and paginators are annotated as well
waiter: s3.BucketExistsWaiter = client.get_waiter("bucket_exists")
paginator: s3.ListMultipartUploadsPaginator = client.get_paginator(
    "list_multipart_uploads"
)
```

### Setup your IDE

### VSCode

- Install [Official Python extension](https://github.com/microsoft/vscode-python)
- Install [mypy](https://github.com/python/mypy)
- Activate `mypy` checking in settings: `"python.linting.mypyEnabled": true`
- Install `boto3-stubs` with `boto3` services you use
- Use [explicit type annotations](#explicit-type-annotations) because
  function overload [is not fully supported](https://github.com/microsoft/python-language-server/issues/1648)
  in `Python` extension.

### PyCharm

- Install [mypy plugin](https://plugins.jetbrains.com/plugin/11086-mypy/)
- Install [mypy](https://github.com/python/mypy)
- Set path to `mypy` in `mypy plugin` settings
- Install `boto3-stubs` with `boto3` services you use
- Use [explicit type annotations](#explicit-type-annotations) for
  `session.client` and `session.resource` calls

Official `mypy` plugin does not work for some reason for me. If you know
how to setup it correctly, please hep me to update this section.

### Other IDEs

- Install [mypy](https://github.com/python/mypy)
- Set path to `mypy` in `mypy plugin` settings
- Install `boto3-stubs` with `boto3` services you use

You need [explicit type annotations](#explicit-type-annotations) for code
auto-complete, but `mypy` works even without them.

### Explicit type annotations

Automatic type discovery is too stressful for PyCharm and does not work in VSCode.
So implicit type annotations support has been removed as it is not useful.

To get full advantage of `boto3-stubs`, you can set types explicitly.

```python
import boto3

from mypy_boto3 import ec2

# covered by boto3-stubs, no explicit type required
session = boto3.session.Session(region_name="us-west-1")

# by default it is Any, but we explicitly set it to EC2Client
# to make method auto-complete work
ec2_client: ec2.EC2Client = boto3.client("ec2", region_name="us-west-1")

# same for resource
ec2_resource: ec2.EC2ServiceResource = session.resource("ec2")

# PyCharm does not need explicit type annotations here, but VSCode does
bundle_task_complete_waiter: ec2.BundleTaskCompleteWaiter = ec2_client.get_waiter("bundle_task_complete")
describe_volumes_paginator: ec2.DescribeVolumesPaginator = ec2_client.get_paginator("describe_volumes")

# ec2_client, ec2_resource, bundle_task_complete_waiter and describe_volumes_paginator
# now have correct type so IDE autocomplete for methods, arguments and return types
# works as expected. You do not need to specify types explicitly further
```

### Pylint compatibility

It is totally safe to use `TYPE_CHECKING` flag in order to avoid `boto3-stubs`
dependency in production.
However, there is an issue in `pylint` that it complains about undefined
variables. To fix it, set all types to `Any` in non-`TYPE_CHECKING` mode.

```python
import boto3
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from mypy_boto3.ec2 import EC2Client, EC2ServiceResource
    from mypy_boto3.ec2.waiters import BundleTaskCompleteWaiter
    from mypy_boto3.ec2.paginators import DescribeVolumesPaginator
else:
    EC2Client = Any
    EC2ServiceResource = Any
    BundleTaskCompleteWaiter = Any
    DescribeVolumesPaginator = Any

...
```

## How to build

### Locally

`mypy-boto3` is built for the latest version of `boto3`. If you need type annotations for another
version of `boto3`, you can use `mypy-boto3-builder`.

```bash
# Install preferred version of `boto3`
python -m pip install boto3==1.10.18 botocore==1.13.18

# Install `mypy-boto3-builder`
python -m pip install mypy-boto3-builder

# Build all packages
# You can specify required services explicitly like
# ./scripts/build.sh -s ec2 s3
./scripts/build.sh

# Install custom `mypy-boto3` packages
./scripts/install.sh
```

### With Docker image

- Install [Docker](https://docs.docker.com/install/)
- Pull latest `mypy_boto3_builder` version and tag it

```bash
docker pull docker.pkg.github.com/vemel/mypy_boto3/mypy_boto3_builder:latest
docker tag docker.pkg.github.com/vemel/mypy_boto3/mypy_boto3_builder:latest mypy_boto3_builder
```

- Generate stubs in `output` directory

```bash
mkdir output

# generate stubs for all services
docker run -v `pwd`/output:/output -ti mypy_boto3_builder

# generate stubs for s3 service
docker run -v `pwd`/output:/output -ti mypy_boto3_builder -s s3

# generate stubs for a specific boto3 version
docker run -e BOTO3_VERSION=1.10.18 BOTOCORE_VERSION=1.13.18 -v `pwd`/output:/output -ti mypy_boto3_builder
```

- Install packages from `output` directory as described above

## Differences from boto3-type-annotations

- `mypy` compatibility
- Fully type annotated
- No need to set types explicitly (depends on your IDE)
- Generated types for return values and arguments
- Added `ServiceResource` sub-collections
- Support service-specific sub-modules
- Modules documentation
- Type annotations for return structures
- Correct annotations for `client.get_waiter` and `client.get_paginator`
- Helper functions for IDEs with no `overload` support (Hi, VSCode!)

## Thank you

- Guys behind [boto3-type-annotations](https://pypi.org/project/boto3-type-annotations/),
  this package is based on top of their work
- [black](https://github.com/psf/black) developers for awesome formatting tool
- [mypy](https://github.com/python/mypy) for doing all dirty work for us

## Sub-modules

### Examples

You can install any sub-modules using `pip`

```bash
# pip install boto3-stubs[<submodule_name>,...]

# install `boto3` type annotations
# for ec2, s3, rds, lambda, sqs, dynamo and cloudformation
python -m pip install boto3-stubs[essential]

# install ec2, s3 and sqs type annotations
python -m pip install boto3-stubs[s3,ec2,sqs]

# build service index. You should execute this command everytime
# you install or remove service packages
python -m mypy_boto3
```

### List of all sub-modules

- `boto3-stubs[essential]` - Type annotations for [CloudFormation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation), [DynamoDB](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB), [EC2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2), [Lambda](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda), [RDS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS), [S3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3) and [SQS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS) services.
- `boto3-stubs[accessanalyzer]` - Type annotations for [AccessAnalyzer](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer) service.
- `boto3-stubs[acm]` - Type annotations for [ACM](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM) service.
- `boto3-stubs[acm-pca]` - Type annotations for [ACMPCA](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA) service.
- `boto3-stubs[alexaforbusiness]` - Type annotations for [AlexaForBusiness](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness) service.
- `boto3-stubs[amplify]` - Type annotations for [Amplify](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify) service.
- `boto3-stubs[apigateway]` - Type annotations for [APIGateway](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway) service.
- `boto3-stubs[apigatewaymanagementapi]` - Type annotations for [ApiGatewayManagementApi](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewaymanagementapi.html#ApiGatewayManagementApi) service.
- `boto3-stubs[apigatewayv2]` - Type annotations for [ApiGatewayV2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2) service.
- `boto3-stubs[appconfig]` - Type annotations for [AppConfig](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig.html#AppConfig) service.
- `boto3-stubs[application-autoscaling]` - Type annotations for [ApplicationAutoScaling](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling) service.
- `boto3-stubs[application-insights]` - Type annotations for [ApplicationInsights](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights) service.
- `boto3-stubs[appmesh]` - Type annotations for [AppMesh](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appmesh.html#AppMesh) service.
- `boto3-stubs[appstream]` - Type annotations for [AppStream](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream) service.
- `boto3-stubs[appsync]` - Type annotations for [AppSync](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync) service.
- `boto3-stubs[athena]` - Type annotations for [Athena](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena) service.
- `boto3-stubs[autoscaling]` - Type annotations for [AutoScaling](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling) service.
- `boto3-stubs[autoscaling-plans]` - Type annotations for [AutoScalingPlans](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans) service.
- `boto3-stubs[backup]` - Type annotations for [Backup](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup) service.
- `boto3-stubs[batch]` - Type annotations for [Batch](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch) service.
- `boto3-stubs[budgets]` - Type annotations for [Budgets](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets) service.
- `boto3-stubs[ce]` - Type annotations for [CostExplorer](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer) service.
- `boto3-stubs[chime]` - Type annotations for [Chime](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime) service.
- `boto3-stubs[cloud9]` - Type annotations for [Cloud9](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9) service.
- `boto3-stubs[clouddirectory]` - Type annotations for [CloudDirectory](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory) service.
- `boto3-stubs[cloudformation]` - Type annotations for [CloudFormation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation) service.
- `boto3-stubs[cloudfront]` - Type annotations for [CloudFront](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront) service.
- `boto3-stubs[cloudhsm]` - Type annotations for [CloudHSM](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM) service.
- `boto3-stubs[cloudhsmv2]` - Type annotations for [CloudHSMV2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2) service.
- `boto3-stubs[cloudsearch]` - Type annotations for [CloudSearch](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch) service.
- `boto3-stubs[cloudsearchdomain]` - Type annotations for [CloudSearchDomain](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html#CloudSearchDomain) service.
- `boto3-stubs[cloudtrail]` - Type annotations for [CloudTrail](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail) service.
- `boto3-stubs[cloudwatch]` - Type annotations for [CloudWatch](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch) service.
- `boto3-stubs[codebuild]` - Type annotations for [CodeBuild](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild) service.
- `boto3-stubs[codecommit]` - Type annotations for [CodeCommit](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit) service.
- `boto3-stubs[codedeploy]` - Type annotations for [CodeDeploy](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy) service.
- `boto3-stubs[codeguru-reviewer]` - Type annotations for [CodeGuruReviewer](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer) service.
- `boto3-stubs[codeguruprofiler]` - Type annotations for [CodeGuruProfiler](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler) service.
- `boto3-stubs[codepipeline]` - Type annotations for [CodePipeline](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline) service.
- `boto3-stubs[codestar]` - Type annotations for [CodeStar](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar) service.
- `boto3-stubs[codestar-notifications]` - Type annotations for [CodeStarNotifications](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications) service.
- `boto3-stubs[cognito-identity]` - Type annotations for [CognitoIdentity](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity) service.
- `boto3-stubs[cognito-idp]` - Type annotations for [CognitoIdentityProvider](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider) service.
- `boto3-stubs[cognito-sync]` - Type annotations for [CognitoSync](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync) service.
- `boto3-stubs[comprehend]` - Type annotations for [Comprehend](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html#Comprehend) service.
- `boto3-stubs[comprehendmedical]` - Type annotations for [ComprehendMedical](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical) service.
- `boto3-stubs[compute-optimizer]` - Type annotations for [ComputeOptimizer](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer) service.
- `boto3-stubs[config]` - Type annotations for [ConfigService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService) service.
- `boto3-stubs[connect]` - Type annotations for [Connect](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect) service.
- `boto3-stubs[connectparticipant]` - Type annotations for [ConnectParticipant](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant) service.
- `boto3-stubs[cur]` - Type annotations for [CostandUsageReportService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur.html#CostandUsageReportService) service.
- `boto3-stubs[dataexchange]` - Type annotations for [DataExchange](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange) service.
- `boto3-stubs[datapipeline]` - Type annotations for [DataPipeline](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline.html#DataPipeline) service.
- `boto3-stubs[datasync]` - Type annotations for [DataSync](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync) service.
- `boto3-stubs[dax]` - Type annotations for [DAX](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX) service.
- `boto3-stubs[detective]` - Type annotations for [Detective](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective) service.
- `boto3-stubs[devicefarm]` - Type annotations for [DeviceFarm](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm) service.
- `boto3-stubs[directconnect]` - Type annotations for [DirectConnect](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect) service.
- `boto3-stubs[discovery]` - Type annotations for [ApplicationDiscoveryService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService) service.
- `boto3-stubs[dlm]` - Type annotations for [DLM](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dlm.html#DLM) service.
- `boto3-stubs[dms]` - Type annotations for [DatabaseMigrationService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService) service.
- `boto3-stubs[docdb]` - Type annotations for [DocDB](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB) service.
- `boto3-stubs[ds]` - Type annotations for [DirectoryService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService) service.
- `boto3-stubs[dynamodb]` - Type annotations for [DynamoDB](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB) service.
- `boto3-stubs[dynamodbstreams]` - Type annotations for [DynamoDBStreams](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodbstreams.html#DynamoDBStreams) service.
- `boto3-stubs[ebs]` - Type annotations for [EBS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS) service.
- `boto3-stubs[ec2]` - Type annotations for [EC2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2) service.
- `boto3-stubs[ec2-instance-connect]` - Type annotations for [EC2InstanceConnect](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect) service.
- `boto3-stubs[ecr]` - Type annotations for [ECR](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr.html#ECR) service.
- `boto3-stubs[ecs]` - Type annotations for [ECS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS) service.
- `boto3-stubs[efs]` - Type annotations for [EFS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs.html#EFS) service.
- `boto3-stubs[eks]` - Type annotations for [EKS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS) service.
- `boto3-stubs[elastic-inference]` - Type annotations for [ElasticInference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference) service.
- `boto3-stubs[elasticache]` - Type annotations for [ElastiCache](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache) service.
- `boto3-stubs[elasticbeanstalk]` - Type annotations for [ElasticBeanstalk](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk) service.
- `boto3-stubs[elastictranscoder]` - Type annotations for [ElasticTranscoder](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder) service.
- `boto3-stubs[elb]` - Type annotations for [ElasticLoadBalancing](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing) service.
- `boto3-stubs[elbv2]` - Type annotations for [ElasticLoadBalancingv2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2) service.
- `boto3-stubs[emr]` - Type annotations for [EMR](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR) service.
- `boto3-stubs[es]` - Type annotations for [ElasticsearchService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService) service.
- `boto3-stubs[events]` - Type annotations for [EventBridge](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#EventBridge) service.
- `boto3-stubs[firehose]` - Type annotations for [Firehose](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose) service.
- `boto3-stubs[fms]` - Type annotations for [FMS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS) service.
- `boto3-stubs[forecast]` - Type annotations for [ForecastService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast.html#ForecastService) service.
- `boto3-stubs[forecastquery]` - Type annotations for [ForecastQueryService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecastquery.html#ForecastQueryService) service.
- `boto3-stubs[frauddetector]` - Type annotations for [FraudDetector](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector) service.
- `boto3-stubs[fsx]` - Type annotations for [FSx](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx) service.
- `boto3-stubs[gamelift]` - Type annotations for [GameLift](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift) service.
- `boto3-stubs[glacier]` - Type annotations for [Glacier](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier) service.
- `boto3-stubs[globalaccelerator]` - Type annotations for [GlobalAccelerator](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator) service.
- `boto3-stubs[glue]` - Type annotations for [Glue](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue) service.
- `boto3-stubs[greengrass]` - Type annotations for [Greengrass](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html#Greengrass) service.
- `boto3-stubs[groundstation]` - Type annotations for [GroundStation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation) service.
- `boto3-stubs[guardduty]` - Type annotations for [GuardDuty](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty) service.
- `boto3-stubs[health]` - Type annotations for [Health](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health) service.
- `boto3-stubs[iam]` - Type annotations for [IAM](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM) service.
- `boto3-stubs[imagebuilder]` - Type annotations for [Imagebuilder](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder) service.
- `boto3-stubs[importexport]` - Type annotations for [ImportExport](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html#ImportExport) service.
- `boto3-stubs[inspector]` - Type annotations for [Inspector](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector) service.
- `boto3-stubs[iot]` - Type annotations for [IoT](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT) service.
- `boto3-stubs[iot-data]` - Type annotations for [IoTDataPlane](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane) service.
- `boto3-stubs[iot-jobs-data]` - Type annotations for [IoTJobsDataPlane](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-jobs-data.html#IoTJobsDataPlane) service.
- `boto3-stubs[iot1click-devices]` - Type annotations for [IoT1ClickDevicesService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService) service.
- `boto3-stubs[iot1click-projects]` - Type annotations for [IoT1ClickProjects](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects.html#IoT1ClickProjects) service.
- `boto3-stubs[iotanalytics]` - Type annotations for [IoTAnalytics](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotanalytics.html#IoTAnalytics) service.
- `boto3-stubs[iotevents]` - Type annotations for [IoTEvents](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents) service.
- `boto3-stubs[iotevents-data]` - Type annotations for [IoTEventsData](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData) service.
- `boto3-stubs[iotsecuretunneling]` - Type annotations for [IoTSecureTunneling](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling) service.
- `boto3-stubs[iotthingsgraph]` - Type annotations for [IoTThingsGraph](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph.html#IoTThingsGraph) service.
- `boto3-stubs[kafka]` - Type annotations for [Kafka](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka) service.
- `boto3-stubs[kendra]` - Type annotations for [Kendra](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra) service.
- `boto3-stubs[kinesis]` - Type annotations for [Kinesis](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis) service.
- `boto3-stubs[kinesis-video-archived-media]` - Type annotations for [KinesisVideoArchivedMedia](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia) service.
- `boto3-stubs[kinesis-video-media]` - Type annotations for [KinesisVideoMedia](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-media.html#KinesisVideoMedia) service.
- `boto3-stubs[kinesis-video-signaling]` - Type annotations for [KinesisVideoSignalingChannels](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-signaling.html#KinesisVideoSignalingChannels) service.
- `boto3-stubs[kinesisanalytics]` - Type annotations for [KinesisAnalytics](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalytics.html#KinesisAnalytics) service.
- `boto3-stubs[kinesisanalyticsv2]` - Type annotations for [KinesisAnalyticsV2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2) service.
- `boto3-stubs[kinesisvideo]` - Type annotations for [KinesisVideo](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo) service.
- `boto3-stubs[kms]` - Type annotations for [KMS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS) service.
- `boto3-stubs[lakeformation]` - Type annotations for [LakeFormation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation) service.
- `boto3-stubs[lambda]` - Type annotations for [Lambda](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda) service.
- `boto3-stubs[lex-models]` - Type annotations for [LexModelBuildingService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService) service.
- `boto3-stubs[lex-runtime]` - Type annotations for [LexRuntimeService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html#LexRuntimeService) service.
- `boto3-stubs[license-manager]` - Type annotations for [LicenseManager](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager) service.
- `boto3-stubs[lightsail]` - Type annotations for [Lightsail](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail) service.
- `boto3-stubs[logs]` - Type annotations for [CloudWatchLogs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs) service.
- `boto3-stubs[machinelearning]` - Type annotations for [MachineLearning](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/machinelearning.html#MachineLearning) service.
- `boto3-stubs[macie]` - Type annotations for [Macie](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie) service.
- `boto3-stubs[managedblockchain]` - Type annotations for [ManagedBlockchain](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain) service.
- `boto3-stubs[marketplace-catalog]` - Type annotations for [MarketplaceCatalog](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog.html#MarketplaceCatalog) service.
- `boto3-stubs[marketplace-entitlement]` - Type annotations for [MarketplaceEntitlementService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService) service.
- `boto3-stubs[marketplacecommerceanalytics]` - Type annotations for [MarketplaceCommerceAnalytics](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics.html#MarketplaceCommerceAnalytics) service.
- `boto3-stubs[mediaconnect]` - Type annotations for [MediaConnect](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect) service.
- `boto3-stubs[mediaconvert]` - Type annotations for [MediaConvert](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert) service.
- `boto3-stubs[medialive]` - Type annotations for [MediaLive](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive) service.
- `boto3-stubs[mediapackage]` - Type annotations for [MediaPackage](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage) service.
- `boto3-stubs[mediapackage-vod]` - Type annotations for [MediaPackageVod](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage-vod.html#MediaPackageVod) service.
- `boto3-stubs[mediastore]` - Type annotations for [MediaStore](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore.html#MediaStore) service.
- `boto3-stubs[mediastore-data]` - Type annotations for [MediaStoreData](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData) service.
- `boto3-stubs[mediatailor]` - Type annotations for [MediaTailor](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor) service.
- `boto3-stubs[meteringmarketplace]` - Type annotations for [MarketplaceMetering](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace.html#MarketplaceMetering) service.
- `boto3-stubs[mgh]` - Type annotations for [MigrationHub](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh.html#MigrationHub) service.
- `boto3-stubs[migrationhub-config]` - Type annotations for [MigrationHubConfig](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhub-config.html#MigrationHubConfig) service.
- `boto3-stubs[mobile]` - Type annotations for [Mobile](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile) service.
- `boto3-stubs[mq]` - Type annotations for [MQ](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ) service.
- `boto3-stubs[mturk]` - Type annotations for [MTurk](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk) service.
- `boto3-stubs[neptune]` - Type annotations for [Neptune](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune) service.
- `boto3-stubs[networkmanager]` - Type annotations for [NetworkManager](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmanager.html#NetworkManager) service.
- `boto3-stubs[opsworks]` - Type annotations for [OpsWorks](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks) service.
- `boto3-stubs[opsworkscm]` - Type annotations for [OpsWorksCM](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm.html#OpsWorksCM) service.
- `boto3-stubs[organizations]` - Type annotations for [Organizations](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations) service.
- `boto3-stubs[outposts]` - Type annotations for [Outposts](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts) service.
- `boto3-stubs[personalize]` - Type annotations for [Personalize](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html#Personalize) service.
- `boto3-stubs[personalize-events]` - Type annotations for [PersonalizeEvents](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize-events.html#PersonalizeEvents) service.
- `boto3-stubs[personalize-runtime]` - Type annotations for [PersonalizeRuntime](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize-runtime.html#PersonalizeRuntime) service.
- `boto3-stubs[pi]` - Type annotations for [PI](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI) service.
- `boto3-stubs[pinpoint]` - Type annotations for [Pinpoint](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint.html#Pinpoint) service.
- `boto3-stubs[pinpoint-email]` - Type annotations for [PinpointEmail](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail) service.
- `boto3-stubs[pinpoint-sms-voice]` - Type annotations for [PinpointSMSVoice](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice) service.
- `boto3-stubs[polly]` - Type annotations for [Polly](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly) service.
- `boto3-stubs[pricing]` - Type annotations for [Pricing](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing) service.
- `boto3-stubs[qldb]` - Type annotations for [QLDB](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb.html#QLDB) service.
- `boto3-stubs[qldb-session]` - Type annotations for [QLDBSession](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session.html#QLDBSession) service.
- `boto3-stubs[quicksight]` - Type annotations for [QuickSight](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight) service.
- `boto3-stubs[ram]` - Type annotations for [RAM](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM) service.
- `boto3-stubs[rds]` - Type annotations for [RDS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS) service.
- `boto3-stubs[rds-data]` - Type annotations for [RDSDataService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html#RDSDataService) service.
- `boto3-stubs[redshift]` - Type annotations for [Redshift](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift) service.
- `boto3-stubs[rekognition]` - Type annotations for [Rekognition](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition) service.
- `boto3-stubs[resource-groups]` - Type annotations for [ResourceGroups](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups) service.
- `boto3-stubs[resourcegroupstaggingapi]` - Type annotations for [ResourceGroupsTaggingAPI](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI) service.
- `boto3-stubs[robomaker]` - Type annotations for [RoboMaker](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker) service.
- `boto3-stubs[route53]` - Type annotations for [Route53](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53) service.
- `boto3-stubs[route53domains]` - Type annotations for [Route53Domains](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains) service.
- `boto3-stubs[route53resolver]` - Type annotations for [Route53Resolver](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53resolver.html#Route53Resolver) service.
- `boto3-stubs[s3]` - Type annotations for [S3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3) service.
- `boto3-stubs[s3control]` - Type annotations for [S3Control](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control) service.
- `boto3-stubs[sagemaker]` - Type annotations for [SageMaker](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker) service.
- `boto3-stubs[sagemaker-a2i-runtime]` - Type annotations for [AugmentedAIRuntime](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime) service.
- `boto3-stubs[sagemaker-runtime]` - Type annotations for [SageMakerRuntime](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime) service.
- `boto3-stubs[savingsplans]` - Type annotations for [SavingsPlans](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans.html#SavingsPlans) service.
- `boto3-stubs[schemas]` - Type annotations for [Schemas](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/schemas.html#Schemas) service.
- `boto3-stubs[sdb]` - Type annotations for [SimpleDB](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb.html#SimpleDB) service.
- `boto3-stubs[secretsmanager]` - Type annotations for [SecretsManager](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager) service.
- `boto3-stubs[securityhub]` - Type annotations for [SecurityHub](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub) service.
- `boto3-stubs[serverlessrepo]` - Type annotations for [ServerlessApplicationRepository](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository) service.
- `boto3-stubs[service-quotas]` - Type annotations for [ServiceQuotas](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas.html#ServiceQuotas) service.
- `boto3-stubs[servicecatalog]` - Type annotations for [ServiceCatalog](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog) service.
- `boto3-stubs[servicediscovery]` - Type annotations for [ServiceDiscovery](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicediscovery.html#ServiceDiscovery) service.
- `boto3-stubs[ses]` - Type annotations for [SES](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses.html#SES) service.
- `boto3-stubs[sesv2]` - Type annotations for [SESV2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2) service.
- `boto3-stubs[shield]` - Type annotations for [Shield](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield.html#Shield) service.
- `boto3-stubs[signer]` - Type annotations for [Signer](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#Signer) service.
- `boto3-stubs[sms]` - Type annotations for [SMS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms.html#SMS) service.
- `boto3-stubs[sms-voice]` - Type annotations for [SMSVoice](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms-voice.html#SMSVoice) service.
- `boto3-stubs[snowball]` - Type annotations for [Snowball](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball) service.
- `boto3-stubs[sns]` - Type annotations for [SNS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS) service.
- `boto3-stubs[sqs]` - Type annotations for [SQS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS) service.
- `boto3-stubs[ssm]` - Type annotations for [SSM](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM) service.
- `boto3-stubs[sso]` - Type annotations for [SSO](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html#SSO) service.
- `boto3-stubs[sso-oidc]` - Type annotations for [SSOOIDC](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-oidc.html#SSOOIDC) service.
- `boto3-stubs[stepfunctions]` - Type annotations for [SFN](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN) service.
- `boto3-stubs[storagegateway]` - Type annotations for [StorageGateway](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway) service.
- `boto3-stubs[sts]` - Type annotations for [STS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS) service.
- `boto3-stubs[support]` - Type annotations for [Support](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support) service.
- `boto3-stubs[swf]` - Type annotations for [SWF](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF) service.
- `boto3-stubs[textract]` - Type annotations for [Textract](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract) service.
- `boto3-stubs[transcribe]` - Type annotations for [TranscribeService](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe.html#TranscribeService) service.
- `boto3-stubs[transfer]` - Type annotations for [Transfer](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer) service.
- `boto3-stubs[translate]` - Type annotations for [Translate](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate) service.
- `boto3-stubs[waf]` - Type annotations for [WAF](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF) service.
- `boto3-stubs[waf-regional]` - Type annotations for [WAFRegional](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional) service.
- `boto3-stubs[wafv2]` - Type annotations for [WAFV2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wafv2.html#WAFV2) service.
- `boto3-stubs[workdocs]` - Type annotations for [WorkDocs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs) service.
- `boto3-stubs[worklink]` - Type annotations for [WorkLink](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/worklink.html#WorkLink) service.
- `boto3-stubs[workmail]` - Type annotations for [WorkMail](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail) service.
- `boto3-stubs[workmailmessageflow]` - Type annotations for [WorkMailMessageFlow](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmailmessageflow.html#WorkMailMessageFlow) service.
- `boto3-stubs[workspaces]` - Type annotations for [WorkSpaces](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces) service.
- `boto3-stubs[xray]` - Type annotations for [XRay](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html#XRay) service.
