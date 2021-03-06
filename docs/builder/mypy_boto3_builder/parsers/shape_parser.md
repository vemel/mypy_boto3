# ShapeParser

> Auto-generated documentation for [builder.mypy_boto3_builder.parsers.shape_parser](https://github.com/vemel/mypy_boto3/blob/master/builder/mypy_boto3_builder/parsers/shape_parser.py) module.

Parser for botocore shape files.

- [mypy-boto3](../../../README.md#mypy_boto3) / [Modules](../../../MODULES.md#mypy-boto3-modules) / `Builder` / [Mypy Boto3 Builder](../index.md#mypy-boto3-builder) / [Parsers](index.md#parsers) / ShapeParser
    - [ShapeParser](#shapeparser)
        - [ShapeParser().get_client_method_map](#shapeparserget_client_method_map)
        - [ShapeParser().get_collection_batch_methods](#shapeparserget_collection_batch_methods)
        - [ShapeParser().get_collection_filter_method](#shapeparserget_collection_filter_method)
        - [ShapeParser().get_paginate_method](#shapeparserget_paginate_method)
        - [ShapeParser().get_paginator_names](#shapeparserget_paginator_names)
        - [ShapeParser().get_resource_method_map](#shapeparserget_resource_method_map)
        - [ShapeParser().get_service_resource_method_map](#shapeparserget_service_resource_method_map)
        - [ShapeParser().get_wait_method](#shapeparserget_wait_method)
    - [ShapeParserError](#shapeparsererror)

## ShapeParser

[[find in source code]](https://github.com/vemel/mypy_boto3/blob/master/builder/mypy_boto3_builder/parsers/shape_parser.py#L45)

```python
class ShapeParser():
    def __init__(session: Session, service_name: ServiceName):
```

Parser for botocore shape files.

#### Arguments

- `session` - Boto3 session.
- `service_name` - ServiceName.

#### Attributes

- `SHAPE_TYPE_MAP` - Type map for shape types.: `{'integer': Type.int, 'long': Type.int, 'boolea...`

### ShapeParser().get_client_method_map

[[find in source code]](https://github.com/vemel/mypy_boto3/blob/master/builder/mypy_boto3_builder/parsers/shape_parser.py#L219)

```python
def get_client_method_map() -> Dict[str, Method]:
```

Get client methods from shape.

#### Returns

A map of method name to Method.

### ShapeParser().get_collection_batch_methods

[[find in source code]](https://github.com/vemel/mypy_boto3/blob/master/builder/mypy_boto3_builder/parsers/shape_parser.py#L541)

```python
def get_collection_batch_methods(
    name: str,
    collection: Collection,
) -> List[Method]:
```

Get batch operations for Resource collection.

#### Arguments

- `name` - Collection record name.
- `collection` - Boto3 Collection.

#### Returns

List of Method records.

### ShapeParser().get_collection_filter_method

[[find in source code]](https://github.com/vemel/mypy_boto3/blob/master/builder/mypy_boto3_builder/parsers/shape_parser.py#L507)

```python
def get_collection_filter_method(name: str, collection: Collection) -> Method:
```

Get `filter` classmethod for Resource collection.

#### Arguments

- `name` - Collection record name.
- `collection` - Boto3 Collection.

#### Returns

Filter Method record.

### ShapeParser().get_paginate_method

[[find in source code]](https://github.com/vemel/mypy_boto3/blob/master/builder/mypy_boto3_builder/parsers/shape_parser.py#L339)

```python
def get_paginate_method(paginator_name: str) -> Method:
```

Get Paginator `paginate` method.

#### Arguments

- `paginator_name` - Paginator name.

#### Returns

Method.

### ShapeParser().get_paginator_names

[[find in source code]](https://github.com/vemel/mypy_boto3/blob/master/builder/mypy_boto3_builder/parsers/shape_parser.py#L144)

```python
def get_paginator_names() -> List[str]:
```

Get available paginator names.

#### Returns

A list of paginator names.

### ShapeParser().get_resource_method_map

[[find in source code]](https://github.com/vemel/mypy_boto3/blob/master/builder/mypy_boto3_builder/parsers/shape_parser.py#L439)

```python
def get_resource_method_map(resource_name: str) -> Dict[str, Method]:
```

Get methods for Resource.

#### Arguments

- `resource_name` - Resource name.

#### Returns

A map of method name to Method.

### ShapeParser().get_service_resource_method_map

[[find in source code]](https://github.com/vemel/mypy_boto3/blob/master/builder/mypy_boto3_builder/parsers/shape_parser.py#L414)

```python
def get_service_resource_method_map() -> Dict[str, Method]:
```

Get methods for ServiceResource.

#### Returns

A map of method name to Method.

### ShapeParser().get_wait_method

[[find in source code]](https://github.com/vemel/mypy_boto3/blob/master/builder/mypy_boto3_builder/parsers/shape_parser.py#L388)

```python
def get_wait_method(waiter_name: str) -> Method:
```

Get Waiter `wait` method.

#### Arguments

- `waiter_name` - Waiter name.

#### Returns

Method.

## ShapeParserError

[[find in source code]](https://github.com/vemel/mypy_boto3/blob/master/builder/mypy_boto3_builder/parsers/shape_parser.py#L41)

```python
class ShapeParserError(Exception):
```
