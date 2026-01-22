# Polymarket APIs Package - Complete Reference

> Comprehensive reference of all methods and classes in the `polymarket-apis` PyPI package
> Package: https://pypi.org/project/polymarket-apis/

---

## Package Information

**Package Name:** `polymarket-apis`
**Version:** 0.4.3

## All Classes in Package


================================================================================
## ApiCreds
================================================================================

### Initialization Parameters

```python
ApiCreds(
    data: Any = None,
)
```

### General

#### `construct`

**Signature:**
```python
def construct(cls, _fields_set: set[str] | None = None, values: Any = None):
```

**Parameters:**

- `cls` (Required)
- `_fields_set` (Optional)
  - Type: `set[str] | None`
  - Default: `None`
- `values` (Optional)
  - Type: `Any`

---

#### `construct`

**Signature:**
```python
def construct(_fields_set: set[str] | None = None, values: Any = None):
```

**Parameters:**

- `_fields_set` (Optional)
  - Type: `set[str] | None`
  - Default: `None`
- `values` (Optional)
  - Type: `Any`

---

#### `copy`

**Signature:**
```python
def copy(include: AbstractSetIntStr | MappingIntStrAny | None = None, exclude: AbstractSetIntStr | MappingIntStrAny | None = None, update: Dict[str, Any] | None = None, deep: bool = False):
```

**Parameters:**

- `include` (Optional)
  - Type: `AbstractSetIntStr | MappingIntStrAny | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `AbstractSetIntStr | MappingIntStrAny | None`
  - Default: `None`
- `update` (Optional)
  - Type: `Dict[str, Any] | None`
  - Default: `None`
- `deep` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

Returns a copy of the model.
!!! warning "Deprecated"
This method is now deprecated; use `model_copy` instead.
If you need `include` or `exclude`, use:
```python {test="skip" lint="skip"}
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```
Args:
include: Optional set or mapping specifying which fields to include in the copied model.
exclude: Optional set or mapping specifying which fields to exclude in the copied model.
update: Optional dictionary of field-value pairs to override field values in the copied model.
deep: If True, the values of fields that are Pydantic models will be deep-copied.
Returns:
A copy of the model with included, excluded and updated fields as specified.

---

#### `copy`

**Signature:**
```python
def copy(include: AbstractSetIntStr | MappingIntStrAny | None = None, exclude: AbstractSetIntStr | MappingIntStrAny | None = None, update: Dict[str, Any] | None = None, deep: bool = False):
```

**Parameters:**

- `include` (Optional)
  - Type: `AbstractSetIntStr | MappingIntStrAny | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `AbstractSetIntStr | MappingIntStrAny | None`
  - Default: `None`
- `update` (Optional)
  - Type: `Dict[str, Any] | None`
  - Default: `None`
- `deep` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

Returns a copy of the model.
!!! warning "Deprecated"
This method is now deprecated; use `model_copy` instead.
If you need `include` or `exclude`, use:
```python {test="skip" lint="skip"}
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```
Args:
include: Optional set or mapping specifying which fields to include in the copied model.
exclude: Optional set or mapping specifying which fields to exclude in the copied model.
update: Optional dictionary of field-value pairs to override field values in the copied model.
deep: If True, the values of fields that are Pydantic models will be deep-copied.
Returns:
A copy of the model with included, excluded and updated fields as specified.

---

#### `dict`

**Signature:**
```python
def dict(include: IncEx | None = None, exclude: IncEx | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False):
```

**Parameters:**

- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `dict`

**Signature:**
```python
def dict(include: IncEx | None = None, exclude: IncEx | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False):
```

**Parameters:**

- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `from_orm`

**Signature:**
```python
def from_orm(cls, obj: Any):
```

**Parameters:**

- `cls` (Required)
- `obj` (Required)
  - Type: `Any`

---

#### `from_orm`

**Signature:**
```python
def from_orm(obj: Any):
```

**Parameters:**

- `obj` (Required)
  - Type: `Any`

---

#### `json`

**Signature:**
```python
def json(include: IncEx | None = None, exclude: IncEx | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, encoder: Callable[[Any], Any] | None = PydanticUndefined, models_as_dict: bool = PydanticUndefined, dumps_kwargs: Any = None):
```

**Parameters:**

- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `encoder` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `PydanticUndefined`
- `models_as_dict` (Optional)
  - Type: `bool`
  - Default: `PydanticUndefined`
- `dumps_kwargs` (Optional)
  - Type: `Any`

---

#### `json`

**Signature:**
```python
def json(include: IncEx | None = None, exclude: IncEx | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, encoder: Callable[[Any], Any] | None = PydanticUndefined, models_as_dict: bool = PydanticUndefined, dumps_kwargs: Any = None):
```

**Parameters:**

- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `encoder` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `PydanticUndefined`
- `models_as_dict` (Optional)
  - Type: `bool`
  - Default: `PydanticUndefined`
- `dumps_kwargs` (Optional)
  - Type: `Any`

---

#### `model_construct`

**Signature:**
```python
def model_construct(cls, _fields_set: set[str] | None = None, values: Any = None):
```

**Parameters:**

- `cls` (Required)
- `_fields_set` (Optional)
  - Type: `set[str] | None`
  - Default: `None`
- `values` (Optional)
  - Type: `Any`

**Description:**

Creates a new instance of the `Model` class with validated data.
Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.
!!! note
`model_construct()` generally respects the `model_config.extra` setting on the provided model.
That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
an error if extra values are passed, but they will be ignored.
Args:
_fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
Otherwise, the field names from the `values` argument will be used.
values: Trusted or pre-validated data dictionary.
Returns:
A new instance of the `Model` class with validated data.

---

#### `model_construct`

**Signature:**
```python
def model_construct(_fields_set: set[str] | None = None, values: Any = None):
```

**Parameters:**

- `_fields_set` (Optional)
  - Type: `set[str] | None`
  - Default: `None`
- `values` (Optional)
  - Type: `Any`

**Description:**

Creates a new instance of the `Model` class with validated data.
Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.
!!! note
`model_construct()` generally respects the `model_config.extra` setting on the provided model.
That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
an error if extra values are passed, but they will be ignored.
Args:
_fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
Otherwise, the field names from the `values` argument will be used.
values: Trusted or pre-validated data dictionary.
Returns:
A new instance of the `Model` class with validated data.

---

#### `model_copy`

**Signature:**
```python
def model_copy(update: Mapping[str, Any] | None = None, deep: bool = False):
```

**Parameters:**

- `update` (Optional)
  - Type: `Mapping[str, Any] | None`
  - Default: `None`
- `deep` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_copy`](../concepts/models.md#model-copy)
Returns a copy of the model.
!!! note
The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
might have unexpected side effects if you store anything in it, on top of the model
fields (e.g. the value of [cached properties][functools.cached_property]).
Args:
update: Values to change/add in the new model. Note: the data is not validated
before creating the new model. You should trust this data.
deep: Set to `True` to make a deep copy of the model.
Returns:
New model instance.

---

#### `model_copy`

**Signature:**
```python
def model_copy(update: Mapping[str, Any] | None = None, deep: bool = False):
```

**Parameters:**

- `update` (Optional)
  - Type: `Mapping[str, Any] | None`
  - Default: `None`
- `deep` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_copy`](../concepts/models.md#model-copy)
Returns a copy of the model.
!!! note
The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
might have unexpected side effects if you store anything in it, on top of the model
fields (e.g. the value of [cached properties][functools.cached_property]).
Args:
update: Values to change/add in the new model. Note: the data is not validated
before creating the new model. You should trust this data.
deep: Set to `True` to make a deep copy of the model.
Returns:
New model instance.

---

#### `model_dump`

**Signature:**
```python
def model_dump(mode: Literal['json', 'python'] | str = 'python', include: IncEx | None = None, exclude: IncEx | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False):
```

**Parameters:**

- `mode` (Optional)
  - Type: `Literal['json', 'python'] | str`
  - Default: `'python'`
- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_computed_fields` (Optional)
  - Type: `bool`
  - Default: `False`
- `round_trip` (Optional)
  - Type: `bool`
  - Default: `False`
- `warnings` (Optional)
  - Type: `bool | Literal['none', 'warn', 'error']`
  - Default: `True`
- `fallback` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `None`
- `serialize_as_any` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_dump`](../concepts/serialization.md#python-mode)
Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
Args:
mode: The mode in which `to_python` should run.
If mode is 'json', the output will only contain JSON serializable types.
If mode is 'python', the output may contain non-JSON-serializable Python objects.
include: A set of fields to include in the output.
exclude: A set of fields to exclude from the output.
context: Additional context to pass to the serializer.
by_alias: Whether to use the field's alias in the dictionary key if defined.
exclude_unset: Whether to exclude fields that have not been explicitly set.
exclude_defaults: Whether to exclude fields that are set to their default value.
exclude_none: Whether to exclude fields that have a value of `None`.
exclude_computed_fields: Whether to exclude computed fields.
While this can be useful for round-tripping, it is usually recommended to use the dedicated
`round_trip` parameter instead.
round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
fallback: A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
Returns:
A dictionary representation of the model.

---

#### `model_dump`

**Signature:**
```python
def model_dump(mode: Literal['json', 'python'] | str = 'python', include: IncEx | None = None, exclude: IncEx | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False):
```

**Parameters:**

- `mode` (Optional)
  - Type: `Literal['json', 'python'] | str`
  - Default: `'python'`
- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_computed_fields` (Optional)
  - Type: `bool`
  - Default: `False`
- `round_trip` (Optional)
  - Type: `bool`
  - Default: `False`
- `warnings` (Optional)
  - Type: `bool | Literal['none', 'warn', 'error']`
  - Default: `True`
- `fallback` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `None`
- `serialize_as_any` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_dump`](../concepts/serialization.md#python-mode)
Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
Args:
mode: The mode in which `to_python` should run.
If mode is 'json', the output will only contain JSON serializable types.
If mode is 'python', the output may contain non-JSON-serializable Python objects.
include: A set of fields to include in the output.
exclude: A set of fields to exclude from the output.
context: Additional context to pass to the serializer.
by_alias: Whether to use the field's alias in the dictionary key if defined.
exclude_unset: Whether to exclude fields that have not been explicitly set.
exclude_defaults: Whether to exclude fields that are set to their default value.
exclude_none: Whether to exclude fields that have a value of `None`.
exclude_computed_fields: Whether to exclude computed fields.
While this can be useful for round-tripping, it is usually recommended to use the dedicated
`round_trip` parameter instead.
round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
fallback: A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
Returns:
A dictionary representation of the model.

---

#### `model_dump_json`

**Signature:**
```python
def model_dump_json(indent: int | None = None, ensure_ascii: bool = False, include: IncEx | None = None, exclude: IncEx | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False):
```

**Parameters:**

- `indent` (Optional)
  - Type: `int | None`
  - Default: `None`
- `ensure_ascii` (Optional)
  - Type: `bool`
  - Default: `False`
- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_computed_fields` (Optional)
  - Type: `bool`
  - Default: `False`
- `round_trip` (Optional)
  - Type: `bool`
  - Default: `False`
- `warnings` (Optional)
  - Type: `bool | Literal['none', 'warn', 'error']`
  - Default: `True`
- `fallback` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `None`
- `serialize_as_any` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_dump_json`](../concepts/serialization.md#json-mode)
Generates a JSON representation of the model using Pydantic's `to_json` method.
Args:
indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
If `False` (the default), these characters will be output as-is.
include: Field(s) to include in the JSON output.
exclude: Field(s) to exclude from the JSON output.
context: Additional context to pass to the serializer.
by_alias: Whether to serialize using field aliases.
exclude_unset: Whether to exclude fields that have not been explicitly set.
exclude_defaults: Whether to exclude fields that are set to their default value.
exclude_none: Whether to exclude fields that have a value of `None`.
exclude_computed_fields: Whether to exclude computed fields.
While this can be useful for round-tripping, it is usually recommended to use the dedicated
`round_trip` parameter instead.
round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
fallback: A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
Returns:
A JSON string representation of the model.

---

#### `model_dump_json`

**Signature:**
```python
def model_dump_json(indent: int | None = None, ensure_ascii: bool = False, include: IncEx | None = None, exclude: IncEx | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False):
```

**Parameters:**

- `indent` (Optional)
  - Type: `int | None`
  - Default: `None`
- `ensure_ascii` (Optional)
  - Type: `bool`
  - Default: `False`
- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_computed_fields` (Optional)
  - Type: `bool`
  - Default: `False`
- `round_trip` (Optional)
  - Type: `bool`
  - Default: `False`
- `warnings` (Optional)
  - Type: `bool | Literal['none', 'warn', 'error']`
  - Default: `True`
- `fallback` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `None`
- `serialize_as_any` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_dump_json`](../concepts/serialization.md#json-mode)
Generates a JSON representation of the model using Pydantic's `to_json` method.
Args:
indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
If `False` (the default), these characters will be output as-is.
include: Field(s) to include in the JSON output.
exclude: Field(s) to exclude from the JSON output.
context: Additional context to pass to the serializer.
by_alias: Whether to serialize using field aliases.
exclude_unset: Whether to exclude fields that have not been explicitly set.
exclude_defaults: Whether to exclude fields that are set to their default value.
exclude_none: Whether to exclude fields that have a value of `None`.
exclude_computed_fields: Whether to exclude computed fields.
While this can be useful for round-tripping, it is usually recommended to use the dedicated
`round_trip` parameter instead.
round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
fallback: A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
Returns:
A JSON string representation of the model.

---

#### `model_json_schema`

**Signature:**
```python
def model_json_schema(cls, by_alias: bool = True, ref_template: str = '#/$defs/{model}', schema_generator: type[GenerateJsonSchema] = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: JsonSchemaMode = 'validation', union_format: Literal['any_of', 'primitive_type_array'] = 'any_of'):
```

**Parameters:**

- `cls` (Required)
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`
- `schema_generator` (Optional)
  - Type: `type[GenerateJsonSchema]`
  - Default: `<class 'pydantic.json_schema.GenerateJsonSchema'>`
- `mode` (Optional)
  - Type: `JsonSchemaMode`
  - Default: `'validation'`
- `union_format` (Optional)
  - Type: `Literal['any_of', 'primitive_type_array']`
  - Default: `'any_of'`

**Description:**

Generates a JSON schema for a model class.
Args:
by_alias: Whether to use attribute aliases or not.
ref_template: The reference template.
union_format: The format to use when combining schemas from unions together. Can be one of:
- `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
keyword to combine schemas (the default).
- `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
`any_of`.
schema_generator: To override the logic used to generate the JSON schema, as a subclass of
`GenerateJsonSchema` with your desired modifications
mode: The mode in which to generate the schema.
Returns:
The JSON schema for the given model class.

---

#### `model_json_schema`

**Signature:**
```python
def model_json_schema(by_alias: bool = True, ref_template: str = '#/$defs/{model}', schema_generator: type[GenerateJsonSchema] = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: JsonSchemaMode = 'validation', union_format: Literal['any_of', 'primitive_type_array'] = 'any_of'):
```

**Parameters:**

- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`
- `schema_generator` (Optional)
  - Type: `type[GenerateJsonSchema]`
  - Default: `<class 'pydantic.json_schema.GenerateJsonSchema'>`
- `mode` (Optional)
  - Type: `JsonSchemaMode`
  - Default: `'validation'`
- `union_format` (Optional)
  - Type: `Literal['any_of', 'primitive_type_array']`
  - Default: `'any_of'`

**Description:**

Generates a JSON schema for a model class.
Args:
by_alias: Whether to use attribute aliases or not.
ref_template: The reference template.
union_format: The format to use when combining schemas from unions together. Can be one of:
- `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
keyword to combine schemas (the default).
- `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
`any_of`.
schema_generator: To override the logic used to generate the JSON schema, as a subclass of
`GenerateJsonSchema` with your desired modifications
mode: The mode in which to generate the schema.
Returns:
The JSON schema for the given model class.

---

#### `model_parametrized_name`

**Signature:**
```python
def model_parametrized_name(cls, params: tuple[type[Any], ...]):
```

**Parameters:**

- `cls` (Required)
- `params` (Required)
  - Type: `tuple[type[Any], ...]`

**Description:**

Compute the class name for parametrizations of generic classes.
This method can be overridden to achieve a custom naming scheme for generic BaseModels.
Args:
params: Tuple of types of the class. Given a generic class
`Model` with 2 type variables and a concrete model `Model[str, int]`,
the value `(str, int)` would be passed to `params`.
Returns:
String representing the new class where `params` are passed to `cls` as type variables.
Raises:
TypeError: Raised when trying to generate concrete names for non-generic models.

---

#### `model_parametrized_name`

**Signature:**
```python
def model_parametrized_name(params: tuple[type[Any], ...]):
```

**Parameters:**

- `params` (Required)
  - Type: `tuple[type[Any], ...]`

**Description:**

Compute the class name for parametrizations of generic classes.
This method can be overridden to achieve a custom naming scheme for generic BaseModels.
Args:
params: Tuple of types of the class. Given a generic class
`Model` with 2 type variables and a concrete model `Model[str, int]`,
the value `(str, int)` would be passed to `params`.
Returns:
String representing the new class where `params` are passed to `cls` as type variables.
Raises:
TypeError: Raised when trying to generate concrete names for non-generic models.

---

#### `model_post_init`

**Signature:**
```python
def model_post_init(context: Any):
```

**Parameters:**

- `context` (Required)
  - Type: `Any`

**Description:**

Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

---

#### `model_post_init`

**Signature:**
```python
def model_post_init(context: Any):
```

**Parameters:**

- `context` (Required)
  - Type: `Any`

**Description:**

Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

---

#### `model_rebuild`

**Signature:**
```python
def model_rebuild(cls, force: bool = False, raise_errors: bool = True, _parent_namespace_depth: int = 2, _types_namespace: MappingNamespace | None = None):
```

**Parameters:**

- `cls` (Required)
- `force` (Optional)
  - Type: `bool`
  - Default: `False`
- `raise_errors` (Optional)
  - Type: `bool`
  - Default: `True`
- `_parent_namespace_depth` (Optional)
  - Type: `int`
  - Default: `2`
- `_types_namespace` (Optional)
  - Type: `MappingNamespace | None`
  - Default: `None`

**Description:**

Try to rebuild the pydantic-core schema for the model.
This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.
Args:
force: Whether to force the rebuilding of the model schema, defaults to `False`.
raise_errors: Whether to raise errors, defaults to `True`.
_parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
_types_namespace: The types namespace, defaults to `None`.
Returns:
Returns `None` if the schema is already "complete" and rebuilding was not required.
If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

---

#### `model_rebuild`

**Signature:**
```python
def model_rebuild(force: bool = False, raise_errors: bool = True, _parent_namespace_depth: int = 2, _types_namespace: MappingNamespace | None = None):
```

**Parameters:**

- `force` (Optional)
  - Type: `bool`
  - Default: `False`
- `raise_errors` (Optional)
  - Type: `bool`
  - Default: `True`
- `_parent_namespace_depth` (Optional)
  - Type: `int`
  - Default: `2`
- `_types_namespace` (Optional)
  - Type: `MappingNamespace | None`
  - Default: `None`

**Description:**

Try to rebuild the pydantic-core schema for the model.
This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.
Args:
force: Whether to force the rebuilding of the model schema, defaults to `False`.
raise_errors: Whether to raise errors, defaults to `True`.
_parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
_types_namespace: The types namespace, defaults to `None`.
Returns:
Returns `None` if the schema is already "complete" and rebuilding was not required.
If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

---

#### `model_validate`

**Signature:**
```python
def model_validate(cls, obj: Any, strict: bool | None = None, extra: ExtraValues | None = None, from_attributes: bool | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `cls` (Required)
- `obj` (Required)
  - Type: `Any`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `from_attributes` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

Validate a pydantic model instance.
Args:
obj: The object to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
from_attributes: Whether to extract data from object attributes.
context: Additional context to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Raises:
ValidationError: If the object could not be validated.
Returns:
The validated model instance.

---

#### `model_validate`

**Signature:**
```python
def model_validate(obj: Any, strict: bool | None = None, extra: ExtraValues | None = None, from_attributes: bool | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `obj` (Required)
  - Type: `Any`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `from_attributes` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

Validate a pydantic model instance.
Args:
obj: The object to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
from_attributes: Whether to extract data from object attributes.
context: Additional context to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Raises:
ValidationError: If the object could not be validated.
Returns:
The validated model instance.

---

#### `model_validate_json`

**Signature:**
```python
def model_validate_json(cls, json_data: str | bytes | bytearray, strict: bool | None = None, extra: ExtraValues | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `cls` (Required)
- `json_data` (Required)
  - Type: `str | bytes | bytearray`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

!!! abstract "Usage Documentation"
[JSON Parsing](../concepts/json.md#json-parsing)
Validate the given JSON data against the Pydantic model.
Args:
json_data: The JSON data to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
context: Extra variables to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Returns:
The validated Pydantic model.
Raises:
ValidationError: If `json_data` is not a JSON string or the object could not be validated.

---

#### `model_validate_json`

**Signature:**
```python
def model_validate_json(json_data: str | bytes | bytearray, strict: bool | None = None, extra: ExtraValues | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `json_data` (Required)
  - Type: `str | bytes | bytearray`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

!!! abstract "Usage Documentation"
[JSON Parsing](../concepts/json.md#json-parsing)
Validate the given JSON data against the Pydantic model.
Args:
json_data: The JSON data to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
context: Extra variables to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Returns:
The validated Pydantic model.
Raises:
ValidationError: If `json_data` is not a JSON string or the object could not be validated.

---

#### `model_validate_strings`

**Signature:**
```python
def model_validate_strings(cls, obj: Any, strict: bool | None = None, extra: ExtraValues | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `cls` (Required)
- `obj` (Required)
  - Type: `Any`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

Validate the given object with string data against the Pydantic model.
Args:
obj: The object containing string data to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
context: Extra variables to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Returns:
The validated Pydantic model.

---

#### `model_validate_strings`

**Signature:**
```python
def model_validate_strings(obj: Any, strict: bool | None = None, extra: ExtraValues | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `obj` (Required)
  - Type: `Any`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

Validate the given object with string data against the Pydantic model.
Args:
obj: The object containing string data to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
context: Extra variables to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Returns:
The validated Pydantic model.

---

#### `parse_file`

**Signature:**
```python
def parse_file(cls, path: str | Path, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False):
```

**Parameters:**

- `cls` (Required)
- `path` (Required)
  - Type: `str | Path`
- `content_type` (Optional)
  - Type: `str | None`
  - Default: `None`
- `encoding` (Optional)
  - Type: `str`
  - Default: `'utf8'`
- `proto` (Optional)
  - Type: `DeprecatedParseProtocol | None`
  - Default: `None`
- `allow_pickle` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `parse_file`

**Signature:**
```python
def parse_file(path: str | Path, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False):
```

**Parameters:**

- `path` (Required)
  - Type: `str | Path`
- `content_type` (Optional)
  - Type: `str | None`
  - Default: `None`
- `encoding` (Optional)
  - Type: `str`
  - Default: `'utf8'`
- `proto` (Optional)
  - Type: `DeprecatedParseProtocol | None`
  - Default: `None`
- `allow_pickle` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `parse_obj`

**Signature:**
```python
def parse_obj(cls, obj: Any):
```

**Parameters:**

- `cls` (Required)
- `obj` (Required)
  - Type: `Any`

---

#### `parse_obj`

**Signature:**
```python
def parse_obj(obj: Any):
```

**Parameters:**

- `obj` (Required)
  - Type: `Any`

---

#### `parse_raw`

**Signature:**
```python
def parse_raw(cls, b: str | bytes, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False):
```

**Parameters:**

- `cls` (Required)
- `b` (Required)
  - Type: `str | bytes`
- `content_type` (Optional)
  - Type: `str | None`
  - Default: `None`
- `encoding` (Optional)
  - Type: `str`
  - Default: `'utf8'`
- `proto` (Optional)
  - Type: `DeprecatedParseProtocol | None`
  - Default: `None`
- `allow_pickle` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `parse_raw`

**Signature:**
```python
def parse_raw(b: str | bytes, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False):
```

**Parameters:**

- `b` (Required)
  - Type: `str | bytes`
- `content_type` (Optional)
  - Type: `str | None`
  - Default: `None`
- `encoding` (Optional)
  - Type: `str`
  - Default: `'utf8'`
- `proto` (Optional)
  - Type: `DeprecatedParseProtocol | None`
  - Default: `None`
- `allow_pickle` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `schema`

**Signature:**
```python
def schema(cls, by_alias: bool = True, ref_template: str = '#/$defs/{model}'):
```

**Parameters:**

- `cls` (Required)
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`

---

#### `schema`

**Signature:**
```python
def schema(by_alias: bool = True, ref_template: str = '#/$defs/{model}'):
```

**Parameters:**

- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`

---

#### `schema_json`

**Signature:**
```python
def schema_json(cls, by_alias: bool = True, ref_template: str = '#/$defs/{model}', dumps_kwargs: Any = None):
```

**Parameters:**

- `cls` (Required)
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`
- `dumps_kwargs` (Optional)
  - Type: `Any`

---

#### `schema_json`

**Signature:**
```python
def schema_json(by_alias: bool = True, ref_template: str = '#/$defs/{model}', dumps_kwargs: Any = None):
```

**Parameters:**

- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`
- `dumps_kwargs` (Optional)
  - Type: `Any`

---

#### `update_forward_refs`

**Signature:**
```python
def update_forward_refs(cls, localns: Any = None):
```

**Parameters:**

- `cls` (Required)
- `localns` (Optional)
  - Type: `Any`

---

#### `update_forward_refs`

**Signature:**
```python
def update_forward_refs(localns: Any = None):
```

**Parameters:**

- `localns` (Optional)
  - Type: `Any`

---

#### `validate`

**Signature:**
```python
def validate(cls, value: Any):
```

**Parameters:**

- `cls` (Required)
- `value` (Required)
  - Type: `Any`

---

#### `validate`

**Signature:**
```python
def validate(value: Any):
```

**Parameters:**

- `value` (Required)
  - Type: `Any`

---


================================================================================
## AsyncPolymarketGraphQLClient
================================================================================

Asynchronous GraphQL client for Polymarket subgraphs.

### Initialization Parameters

```python
AsyncPolymarketGraphQLClient(
    endpoint_name: typing.Literal['activity_subgraph', 'fpmm_subgraph', 'open_interest_subgraph', 'orderbook_subgraph', 'pnl_subgraph', 'positions_subgraph', 'sports_oracle_subgraph', 'wallet_subgraph'],
)
```

### GraphQL

#### `query`

**Signature:**
```python
def query(query_string: <class 'str'>):
```

**Parameters:**

- `query_string` (Required)
  - Type: `<class 'str'>`

---

#### `query`

**Signature:**
```python
def query(query_string: <class 'str'>):
```

**Parameters:**

- `query_string` (Required)
  - Type: `<class 'str'>`

---


================================================================================
## MarketOrderArgs
================================================================================

### Initialization Parameters

```python
MarketOrderArgs(
    data: Any = None,
)
```

### General

#### `construct`

**Signature:**
```python
def construct(cls, _fields_set: set[str] | None = None, values: Any = None):
```

**Parameters:**

- `cls` (Required)
- `_fields_set` (Optional)
  - Type: `set[str] | None`
  - Default: `None`
- `values` (Optional)
  - Type: `Any`

---

#### `construct`

**Signature:**
```python
def construct(_fields_set: set[str] | None = None, values: Any = None):
```

**Parameters:**

- `_fields_set` (Optional)
  - Type: `set[str] | None`
  - Default: `None`
- `values` (Optional)
  - Type: `Any`

---

#### `copy`

**Signature:**
```python
def copy(include: AbstractSetIntStr | MappingIntStrAny | None = None, exclude: AbstractSetIntStr | MappingIntStrAny | None = None, update: Dict[str, Any] | None = None, deep: bool = False):
```

**Parameters:**

- `include` (Optional)
  - Type: `AbstractSetIntStr | MappingIntStrAny | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `AbstractSetIntStr | MappingIntStrAny | None`
  - Default: `None`
- `update` (Optional)
  - Type: `Dict[str, Any] | None`
  - Default: `None`
- `deep` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

Returns a copy of the model.
!!! warning "Deprecated"
This method is now deprecated; use `model_copy` instead.
If you need `include` or `exclude`, use:
```python {test="skip" lint="skip"}
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```
Args:
include: Optional set or mapping specifying which fields to include in the copied model.
exclude: Optional set or mapping specifying which fields to exclude in the copied model.
update: Optional dictionary of field-value pairs to override field values in the copied model.
deep: If True, the values of fields that are Pydantic models will be deep-copied.
Returns:
A copy of the model with included, excluded and updated fields as specified.

---

#### `copy`

**Signature:**
```python
def copy(include: AbstractSetIntStr | MappingIntStrAny | None = None, exclude: AbstractSetIntStr | MappingIntStrAny | None = None, update: Dict[str, Any] | None = None, deep: bool = False):
```

**Parameters:**

- `include` (Optional)
  - Type: `AbstractSetIntStr | MappingIntStrAny | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `AbstractSetIntStr | MappingIntStrAny | None`
  - Default: `None`
- `update` (Optional)
  - Type: `Dict[str, Any] | None`
  - Default: `None`
- `deep` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

Returns a copy of the model.
!!! warning "Deprecated"
This method is now deprecated; use `model_copy` instead.
If you need `include` or `exclude`, use:
```python {test="skip" lint="skip"}
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```
Args:
include: Optional set or mapping specifying which fields to include in the copied model.
exclude: Optional set or mapping specifying which fields to exclude in the copied model.
update: Optional dictionary of field-value pairs to override field values in the copied model.
deep: If True, the values of fields that are Pydantic models will be deep-copied.
Returns:
A copy of the model with included, excluded and updated fields as specified.

---

#### `dict`

**Signature:**
```python
def dict(include: IncEx | None = None, exclude: IncEx | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False):
```

**Parameters:**

- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `dict`

**Signature:**
```python
def dict(include: IncEx | None = None, exclude: IncEx | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False):
```

**Parameters:**

- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `from_orm`

**Signature:**
```python
def from_orm(cls, obj: Any):
```

**Parameters:**

- `cls` (Required)
- `obj` (Required)
  - Type: `Any`

---

#### `from_orm`

**Signature:**
```python
def from_orm(obj: Any):
```

**Parameters:**

- `obj` (Required)
  - Type: `Any`

---

#### `json`

**Signature:**
```python
def json(include: IncEx | None = None, exclude: IncEx | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, encoder: Callable[[Any], Any] | None = PydanticUndefined, models_as_dict: bool = PydanticUndefined, dumps_kwargs: Any = None):
```

**Parameters:**

- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `encoder` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `PydanticUndefined`
- `models_as_dict` (Optional)
  - Type: `bool`
  - Default: `PydanticUndefined`
- `dumps_kwargs` (Optional)
  - Type: `Any`

---

#### `json`

**Signature:**
```python
def json(include: IncEx | None = None, exclude: IncEx | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, encoder: Callable[[Any], Any] | None = PydanticUndefined, models_as_dict: bool = PydanticUndefined, dumps_kwargs: Any = None):
```

**Parameters:**

- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `encoder` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `PydanticUndefined`
- `models_as_dict` (Optional)
  - Type: `bool`
  - Default: `PydanticUndefined`
- `dumps_kwargs` (Optional)
  - Type: `Any`

---

#### `model_construct`

**Signature:**
```python
def model_construct(cls, _fields_set: set[str] | None = None, values: Any = None):
```

**Parameters:**

- `cls` (Required)
- `_fields_set` (Optional)
  - Type: `set[str] | None`
  - Default: `None`
- `values` (Optional)
  - Type: `Any`

**Description:**

Creates a new instance of the `Model` class with validated data.
Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.
!!! note
`model_construct()` generally respects the `model_config.extra` setting on the provided model.
That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
an error if extra values are passed, but they will be ignored.
Args:
_fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
Otherwise, the field names from the `values` argument will be used.
values: Trusted or pre-validated data dictionary.
Returns:
A new instance of the `Model` class with validated data.

---

#### `model_construct`

**Signature:**
```python
def model_construct(_fields_set: set[str] | None = None, values: Any = None):
```

**Parameters:**

- `_fields_set` (Optional)
  - Type: `set[str] | None`
  - Default: `None`
- `values` (Optional)
  - Type: `Any`

**Description:**

Creates a new instance of the `Model` class with validated data.
Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.
!!! note
`model_construct()` generally respects the `model_config.extra` setting on the provided model.
That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
an error if extra values are passed, but they will be ignored.
Args:
_fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
Otherwise, the field names from the `values` argument will be used.
values: Trusted or pre-validated data dictionary.
Returns:
A new instance of the `Model` class with validated data.

---

#### `model_copy`

**Signature:**
```python
def model_copy(update: Mapping[str, Any] | None = None, deep: bool = False):
```

**Parameters:**

- `update` (Optional)
  - Type: `Mapping[str, Any] | None`
  - Default: `None`
- `deep` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_copy`](../concepts/models.md#model-copy)
Returns a copy of the model.
!!! note
The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
might have unexpected side effects if you store anything in it, on top of the model
fields (e.g. the value of [cached properties][functools.cached_property]).
Args:
update: Values to change/add in the new model. Note: the data is not validated
before creating the new model. You should trust this data.
deep: Set to `True` to make a deep copy of the model.
Returns:
New model instance.

---

#### `model_copy`

**Signature:**
```python
def model_copy(update: Mapping[str, Any] | None = None, deep: bool = False):
```

**Parameters:**

- `update` (Optional)
  - Type: `Mapping[str, Any] | None`
  - Default: `None`
- `deep` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_copy`](../concepts/models.md#model-copy)
Returns a copy of the model.
!!! note
The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
might have unexpected side effects if you store anything in it, on top of the model
fields (e.g. the value of [cached properties][functools.cached_property]).
Args:
update: Values to change/add in the new model. Note: the data is not validated
before creating the new model. You should trust this data.
deep: Set to `True` to make a deep copy of the model.
Returns:
New model instance.

---

#### `model_dump`

**Signature:**
```python
def model_dump(mode: Literal['json', 'python'] | str = 'python', include: IncEx | None = None, exclude: IncEx | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False):
```

**Parameters:**

- `mode` (Optional)
  - Type: `Literal['json', 'python'] | str`
  - Default: `'python'`
- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_computed_fields` (Optional)
  - Type: `bool`
  - Default: `False`
- `round_trip` (Optional)
  - Type: `bool`
  - Default: `False`
- `warnings` (Optional)
  - Type: `bool | Literal['none', 'warn', 'error']`
  - Default: `True`
- `fallback` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `None`
- `serialize_as_any` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_dump`](../concepts/serialization.md#python-mode)
Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
Args:
mode: The mode in which `to_python` should run.
If mode is 'json', the output will only contain JSON serializable types.
If mode is 'python', the output may contain non-JSON-serializable Python objects.
include: A set of fields to include in the output.
exclude: A set of fields to exclude from the output.
context: Additional context to pass to the serializer.
by_alias: Whether to use the field's alias in the dictionary key if defined.
exclude_unset: Whether to exclude fields that have not been explicitly set.
exclude_defaults: Whether to exclude fields that are set to their default value.
exclude_none: Whether to exclude fields that have a value of `None`.
exclude_computed_fields: Whether to exclude computed fields.
While this can be useful for round-tripping, it is usually recommended to use the dedicated
`round_trip` parameter instead.
round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
fallback: A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
Returns:
A dictionary representation of the model.

---

#### `model_dump`

**Signature:**
```python
def model_dump(mode: Literal['json', 'python'] | str = 'python', include: IncEx | None = None, exclude: IncEx | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False):
```

**Parameters:**

- `mode` (Optional)
  - Type: `Literal['json', 'python'] | str`
  - Default: `'python'`
- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_computed_fields` (Optional)
  - Type: `bool`
  - Default: `False`
- `round_trip` (Optional)
  - Type: `bool`
  - Default: `False`
- `warnings` (Optional)
  - Type: `bool | Literal['none', 'warn', 'error']`
  - Default: `True`
- `fallback` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `None`
- `serialize_as_any` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_dump`](../concepts/serialization.md#python-mode)
Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
Args:
mode: The mode in which `to_python` should run.
If mode is 'json', the output will only contain JSON serializable types.
If mode is 'python', the output may contain non-JSON-serializable Python objects.
include: A set of fields to include in the output.
exclude: A set of fields to exclude from the output.
context: Additional context to pass to the serializer.
by_alias: Whether to use the field's alias in the dictionary key if defined.
exclude_unset: Whether to exclude fields that have not been explicitly set.
exclude_defaults: Whether to exclude fields that are set to their default value.
exclude_none: Whether to exclude fields that have a value of `None`.
exclude_computed_fields: Whether to exclude computed fields.
While this can be useful for round-tripping, it is usually recommended to use the dedicated
`round_trip` parameter instead.
round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
fallback: A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
Returns:
A dictionary representation of the model.

---

#### `model_dump_json`

**Signature:**
```python
def model_dump_json(indent: int | None = None, ensure_ascii: bool = False, include: IncEx | None = None, exclude: IncEx | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False):
```

**Parameters:**

- `indent` (Optional)
  - Type: `int | None`
  - Default: `None`
- `ensure_ascii` (Optional)
  - Type: `bool`
  - Default: `False`
- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_computed_fields` (Optional)
  - Type: `bool`
  - Default: `False`
- `round_trip` (Optional)
  - Type: `bool`
  - Default: `False`
- `warnings` (Optional)
  - Type: `bool | Literal['none', 'warn', 'error']`
  - Default: `True`
- `fallback` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `None`
- `serialize_as_any` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_dump_json`](../concepts/serialization.md#json-mode)
Generates a JSON representation of the model using Pydantic's `to_json` method.
Args:
indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
If `False` (the default), these characters will be output as-is.
include: Field(s) to include in the JSON output.
exclude: Field(s) to exclude from the JSON output.
context: Additional context to pass to the serializer.
by_alias: Whether to serialize using field aliases.
exclude_unset: Whether to exclude fields that have not been explicitly set.
exclude_defaults: Whether to exclude fields that are set to their default value.
exclude_none: Whether to exclude fields that have a value of `None`.
exclude_computed_fields: Whether to exclude computed fields.
While this can be useful for round-tripping, it is usually recommended to use the dedicated
`round_trip` parameter instead.
round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
fallback: A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
Returns:
A JSON string representation of the model.

---

#### `model_dump_json`

**Signature:**
```python
def model_dump_json(indent: int | None = None, ensure_ascii: bool = False, include: IncEx | None = None, exclude: IncEx | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False):
```

**Parameters:**

- `indent` (Optional)
  - Type: `int | None`
  - Default: `None`
- `ensure_ascii` (Optional)
  - Type: `bool`
  - Default: `False`
- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_computed_fields` (Optional)
  - Type: `bool`
  - Default: `False`
- `round_trip` (Optional)
  - Type: `bool`
  - Default: `False`
- `warnings` (Optional)
  - Type: `bool | Literal['none', 'warn', 'error']`
  - Default: `True`
- `fallback` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `None`
- `serialize_as_any` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_dump_json`](../concepts/serialization.md#json-mode)
Generates a JSON representation of the model using Pydantic's `to_json` method.
Args:
indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
If `False` (the default), these characters will be output as-is.
include: Field(s) to include in the JSON output.
exclude: Field(s) to exclude from the JSON output.
context: Additional context to pass to the serializer.
by_alias: Whether to serialize using field aliases.
exclude_unset: Whether to exclude fields that have not been explicitly set.
exclude_defaults: Whether to exclude fields that are set to their default value.
exclude_none: Whether to exclude fields that have a value of `None`.
exclude_computed_fields: Whether to exclude computed fields.
While this can be useful for round-tripping, it is usually recommended to use the dedicated
`round_trip` parameter instead.
round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
fallback: A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
Returns:
A JSON string representation of the model.

---

#### `model_json_schema`

**Signature:**
```python
def model_json_schema(cls, by_alias: bool = True, ref_template: str = '#/$defs/{model}', schema_generator: type[GenerateJsonSchema] = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: JsonSchemaMode = 'validation', union_format: Literal['any_of', 'primitive_type_array'] = 'any_of'):
```

**Parameters:**

- `cls` (Required)
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`
- `schema_generator` (Optional)
  - Type: `type[GenerateJsonSchema]`
  - Default: `<class 'pydantic.json_schema.GenerateJsonSchema'>`
- `mode` (Optional)
  - Type: `JsonSchemaMode`
  - Default: `'validation'`
- `union_format` (Optional)
  - Type: `Literal['any_of', 'primitive_type_array']`
  - Default: `'any_of'`

**Description:**

Generates a JSON schema for a model class.
Args:
by_alias: Whether to use attribute aliases or not.
ref_template: The reference template.
union_format: The format to use when combining schemas from unions together. Can be one of:
- `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
keyword to combine schemas (the default).
- `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
`any_of`.
schema_generator: To override the logic used to generate the JSON schema, as a subclass of
`GenerateJsonSchema` with your desired modifications
mode: The mode in which to generate the schema.
Returns:
The JSON schema for the given model class.

---

#### `model_json_schema`

**Signature:**
```python
def model_json_schema(by_alias: bool = True, ref_template: str = '#/$defs/{model}', schema_generator: type[GenerateJsonSchema] = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: JsonSchemaMode = 'validation', union_format: Literal['any_of', 'primitive_type_array'] = 'any_of'):
```

**Parameters:**

- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`
- `schema_generator` (Optional)
  - Type: `type[GenerateJsonSchema]`
  - Default: `<class 'pydantic.json_schema.GenerateJsonSchema'>`
- `mode` (Optional)
  - Type: `JsonSchemaMode`
  - Default: `'validation'`
- `union_format` (Optional)
  - Type: `Literal['any_of', 'primitive_type_array']`
  - Default: `'any_of'`

**Description:**

Generates a JSON schema for a model class.
Args:
by_alias: Whether to use attribute aliases or not.
ref_template: The reference template.
union_format: The format to use when combining schemas from unions together. Can be one of:
- `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
keyword to combine schemas (the default).
- `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
`any_of`.
schema_generator: To override the logic used to generate the JSON schema, as a subclass of
`GenerateJsonSchema` with your desired modifications
mode: The mode in which to generate the schema.
Returns:
The JSON schema for the given model class.

---

#### `model_parametrized_name`

**Signature:**
```python
def model_parametrized_name(cls, params: tuple[type[Any], ...]):
```

**Parameters:**

- `cls` (Required)
- `params` (Required)
  - Type: `tuple[type[Any], ...]`

**Description:**

Compute the class name for parametrizations of generic classes.
This method can be overridden to achieve a custom naming scheme for generic BaseModels.
Args:
params: Tuple of types of the class. Given a generic class
`Model` with 2 type variables and a concrete model `Model[str, int]`,
the value `(str, int)` would be passed to `params`.
Returns:
String representing the new class where `params` are passed to `cls` as type variables.
Raises:
TypeError: Raised when trying to generate concrete names for non-generic models.

---

#### `model_parametrized_name`

**Signature:**
```python
def model_parametrized_name(params: tuple[type[Any], ...]):
```

**Parameters:**

- `params` (Required)
  - Type: `tuple[type[Any], ...]`

**Description:**

Compute the class name for parametrizations of generic classes.
This method can be overridden to achieve a custom naming scheme for generic BaseModels.
Args:
params: Tuple of types of the class. Given a generic class
`Model` with 2 type variables and a concrete model `Model[str, int]`,
the value `(str, int)` would be passed to `params`.
Returns:
String representing the new class where `params` are passed to `cls` as type variables.
Raises:
TypeError: Raised when trying to generate concrete names for non-generic models.

---

#### `model_post_init`

**Signature:**
```python
def model_post_init(context: Any):
```

**Parameters:**

- `context` (Required)
  - Type: `Any`

**Description:**

Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

---

#### `model_post_init`

**Signature:**
```python
def model_post_init(context: Any):
```

**Parameters:**

- `context` (Required)
  - Type: `Any`

**Description:**

Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

---

#### `model_rebuild`

**Signature:**
```python
def model_rebuild(cls, force: bool = False, raise_errors: bool = True, _parent_namespace_depth: int = 2, _types_namespace: MappingNamespace | None = None):
```

**Parameters:**

- `cls` (Required)
- `force` (Optional)
  - Type: `bool`
  - Default: `False`
- `raise_errors` (Optional)
  - Type: `bool`
  - Default: `True`
- `_parent_namespace_depth` (Optional)
  - Type: `int`
  - Default: `2`
- `_types_namespace` (Optional)
  - Type: `MappingNamespace | None`
  - Default: `None`

**Description:**

Try to rebuild the pydantic-core schema for the model.
This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.
Args:
force: Whether to force the rebuilding of the model schema, defaults to `False`.
raise_errors: Whether to raise errors, defaults to `True`.
_parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
_types_namespace: The types namespace, defaults to `None`.
Returns:
Returns `None` if the schema is already "complete" and rebuilding was not required.
If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

---

#### `model_rebuild`

**Signature:**
```python
def model_rebuild(force: bool = False, raise_errors: bool = True, _parent_namespace_depth: int = 2, _types_namespace: MappingNamespace | None = None):
```

**Parameters:**

- `force` (Optional)
  - Type: `bool`
  - Default: `False`
- `raise_errors` (Optional)
  - Type: `bool`
  - Default: `True`
- `_parent_namespace_depth` (Optional)
  - Type: `int`
  - Default: `2`
- `_types_namespace` (Optional)
  - Type: `MappingNamespace | None`
  - Default: `None`

**Description:**

Try to rebuild the pydantic-core schema for the model.
This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.
Args:
force: Whether to force the rebuilding of the model schema, defaults to `False`.
raise_errors: Whether to raise errors, defaults to `True`.
_parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
_types_namespace: The types namespace, defaults to `None`.
Returns:
Returns `None` if the schema is already "complete" and rebuilding was not required.
If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

---

#### `model_validate`

**Signature:**
```python
def model_validate(cls, obj: Any, strict: bool | None = None, extra: ExtraValues | None = None, from_attributes: bool | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `cls` (Required)
- `obj` (Required)
  - Type: `Any`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `from_attributes` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

Validate a pydantic model instance.
Args:
obj: The object to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
from_attributes: Whether to extract data from object attributes.
context: Additional context to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Raises:
ValidationError: If the object could not be validated.
Returns:
The validated model instance.

---

#### `model_validate`

**Signature:**
```python
def model_validate(obj: Any, strict: bool | None = None, extra: ExtraValues | None = None, from_attributes: bool | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `obj` (Required)
  - Type: `Any`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `from_attributes` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

Validate a pydantic model instance.
Args:
obj: The object to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
from_attributes: Whether to extract data from object attributes.
context: Additional context to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Raises:
ValidationError: If the object could not be validated.
Returns:
The validated model instance.

---

#### `model_validate_json`

**Signature:**
```python
def model_validate_json(cls, json_data: str | bytes | bytearray, strict: bool | None = None, extra: ExtraValues | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `cls` (Required)
- `json_data` (Required)
  - Type: `str | bytes | bytearray`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

!!! abstract "Usage Documentation"
[JSON Parsing](../concepts/json.md#json-parsing)
Validate the given JSON data against the Pydantic model.
Args:
json_data: The JSON data to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
context: Extra variables to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Returns:
The validated Pydantic model.
Raises:
ValidationError: If `json_data` is not a JSON string or the object could not be validated.

---

#### `model_validate_json`

**Signature:**
```python
def model_validate_json(json_data: str | bytes | bytearray, strict: bool | None = None, extra: ExtraValues | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `json_data` (Required)
  - Type: `str | bytes | bytearray`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

!!! abstract "Usage Documentation"
[JSON Parsing](../concepts/json.md#json-parsing)
Validate the given JSON data against the Pydantic model.
Args:
json_data: The JSON data to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
context: Extra variables to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Returns:
The validated Pydantic model.
Raises:
ValidationError: If `json_data` is not a JSON string or the object could not be validated.

---

#### `model_validate_strings`

**Signature:**
```python
def model_validate_strings(cls, obj: Any, strict: bool | None = None, extra: ExtraValues | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `cls` (Required)
- `obj` (Required)
  - Type: `Any`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

Validate the given object with string data against the Pydantic model.
Args:
obj: The object containing string data to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
context: Extra variables to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Returns:
The validated Pydantic model.

---

#### `model_validate_strings`

**Signature:**
```python
def model_validate_strings(obj: Any, strict: bool | None = None, extra: ExtraValues | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `obj` (Required)
  - Type: `Any`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

Validate the given object with string data against the Pydantic model.
Args:
obj: The object containing string data to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
context: Extra variables to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Returns:
The validated Pydantic model.

---

#### `parse_file`

**Signature:**
```python
def parse_file(cls, path: str | Path, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False):
```

**Parameters:**

- `cls` (Required)
- `path` (Required)
  - Type: `str | Path`
- `content_type` (Optional)
  - Type: `str | None`
  - Default: `None`
- `encoding` (Optional)
  - Type: `str`
  - Default: `'utf8'`
- `proto` (Optional)
  - Type: `DeprecatedParseProtocol | None`
  - Default: `None`
- `allow_pickle` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `parse_file`

**Signature:**
```python
def parse_file(path: str | Path, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False):
```

**Parameters:**

- `path` (Required)
  - Type: `str | Path`
- `content_type` (Optional)
  - Type: `str | None`
  - Default: `None`
- `encoding` (Optional)
  - Type: `str`
  - Default: `'utf8'`
- `proto` (Optional)
  - Type: `DeprecatedParseProtocol | None`
  - Default: `None`
- `allow_pickle` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `parse_obj`

**Signature:**
```python
def parse_obj(cls, obj: Any):
```

**Parameters:**

- `cls` (Required)
- `obj` (Required)
  - Type: `Any`

---

#### `parse_obj`

**Signature:**
```python
def parse_obj(obj: Any):
```

**Parameters:**

- `obj` (Required)
  - Type: `Any`

---

#### `parse_raw`

**Signature:**
```python
def parse_raw(cls, b: str | bytes, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False):
```

**Parameters:**

- `cls` (Required)
- `b` (Required)
  - Type: `str | bytes`
- `content_type` (Optional)
  - Type: `str | None`
  - Default: `None`
- `encoding` (Optional)
  - Type: `str`
  - Default: `'utf8'`
- `proto` (Optional)
  - Type: `DeprecatedParseProtocol | None`
  - Default: `None`
- `allow_pickle` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `parse_raw`

**Signature:**
```python
def parse_raw(b: str | bytes, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False):
```

**Parameters:**

- `b` (Required)
  - Type: `str | bytes`
- `content_type` (Optional)
  - Type: `str | None`
  - Default: `None`
- `encoding` (Optional)
  - Type: `str`
  - Default: `'utf8'`
- `proto` (Optional)
  - Type: `DeprecatedParseProtocol | None`
  - Default: `None`
- `allow_pickle` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `schema`

**Signature:**
```python
def schema(cls, by_alias: bool = True, ref_template: str = '#/$defs/{model}'):
```

**Parameters:**

- `cls` (Required)
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`

---

#### `schema`

**Signature:**
```python
def schema(by_alias: bool = True, ref_template: str = '#/$defs/{model}'):
```

**Parameters:**

- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`

---

#### `schema_json`

**Signature:**
```python
def schema_json(cls, by_alias: bool = True, ref_template: str = '#/$defs/{model}', dumps_kwargs: Any = None):
```

**Parameters:**

- `cls` (Required)
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`
- `dumps_kwargs` (Optional)
  - Type: `Any`

---

#### `schema_json`

**Signature:**
```python
def schema_json(by_alias: bool = True, ref_template: str = '#/$defs/{model}', dumps_kwargs: Any = None):
```

**Parameters:**

- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`
- `dumps_kwargs` (Optional)
  - Type: `Any`

---

#### `update_forward_refs`

**Signature:**
```python
def update_forward_refs(cls, localns: Any = None):
```

**Parameters:**

- `cls` (Required)
- `localns` (Optional)
  - Type: `Any`

---

#### `update_forward_refs`

**Signature:**
```python
def update_forward_refs(localns: Any = None):
```

**Parameters:**

- `localns` (Optional)
  - Type: `Any`

---

#### `validate`

**Signature:**
```python
def validate(cls, value: Any):
```

**Parameters:**

- `cls` (Required)
- `value` (Required)
  - Type: `Any`

---

#### `validate`

**Signature:**
```python
def validate(value: Any):
```

**Parameters:**

- `value` (Required)
  - Type: `Any`

---


================================================================================
## OrderArgs
================================================================================

### Initialization Parameters

```python
OrderArgs(
    data: Any = None,
)
```

### General

#### `construct`

**Signature:**
```python
def construct(cls, _fields_set: set[str] | None = None, values: Any = None):
```

**Parameters:**

- `cls` (Required)
- `_fields_set` (Optional)
  - Type: `set[str] | None`
  - Default: `None`
- `values` (Optional)
  - Type: `Any`

---

#### `construct`

**Signature:**
```python
def construct(_fields_set: set[str] | None = None, values: Any = None):
```

**Parameters:**

- `_fields_set` (Optional)
  - Type: `set[str] | None`
  - Default: `None`
- `values` (Optional)
  - Type: `Any`

---

#### `copy`

**Signature:**
```python
def copy(include: AbstractSetIntStr | MappingIntStrAny | None = None, exclude: AbstractSetIntStr | MappingIntStrAny | None = None, update: Dict[str, Any] | None = None, deep: bool = False):
```

**Parameters:**

- `include` (Optional)
  - Type: `AbstractSetIntStr | MappingIntStrAny | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `AbstractSetIntStr | MappingIntStrAny | None`
  - Default: `None`
- `update` (Optional)
  - Type: `Dict[str, Any] | None`
  - Default: `None`
- `deep` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

Returns a copy of the model.
!!! warning "Deprecated"
This method is now deprecated; use `model_copy` instead.
If you need `include` or `exclude`, use:
```python {test="skip" lint="skip"}
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```
Args:
include: Optional set or mapping specifying which fields to include in the copied model.
exclude: Optional set or mapping specifying which fields to exclude in the copied model.
update: Optional dictionary of field-value pairs to override field values in the copied model.
deep: If True, the values of fields that are Pydantic models will be deep-copied.
Returns:
A copy of the model with included, excluded and updated fields as specified.

---

#### `copy`

**Signature:**
```python
def copy(include: AbstractSetIntStr | MappingIntStrAny | None = None, exclude: AbstractSetIntStr | MappingIntStrAny | None = None, update: Dict[str, Any] | None = None, deep: bool = False):
```

**Parameters:**

- `include` (Optional)
  - Type: `AbstractSetIntStr | MappingIntStrAny | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `AbstractSetIntStr | MappingIntStrAny | None`
  - Default: `None`
- `update` (Optional)
  - Type: `Dict[str, Any] | None`
  - Default: `None`
- `deep` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

Returns a copy of the model.
!!! warning "Deprecated"
This method is now deprecated; use `model_copy` instead.
If you need `include` or `exclude`, use:
```python {test="skip" lint="skip"}
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```
Args:
include: Optional set or mapping specifying which fields to include in the copied model.
exclude: Optional set or mapping specifying which fields to exclude in the copied model.
update: Optional dictionary of field-value pairs to override field values in the copied model.
deep: If True, the values of fields that are Pydantic models will be deep-copied.
Returns:
A copy of the model with included, excluded and updated fields as specified.

---

#### `dict`

**Signature:**
```python
def dict(include: IncEx | None = None, exclude: IncEx | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False):
```

**Parameters:**

- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `dict`

**Signature:**
```python
def dict(include: IncEx | None = None, exclude: IncEx | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False):
```

**Parameters:**

- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `from_orm`

**Signature:**
```python
def from_orm(cls, obj: Any):
```

**Parameters:**

- `cls` (Required)
- `obj` (Required)
  - Type: `Any`

---

#### `from_orm`

**Signature:**
```python
def from_orm(obj: Any):
```

**Parameters:**

- `obj` (Required)
  - Type: `Any`

---

#### `json`

**Signature:**
```python
def json(include: IncEx | None = None, exclude: IncEx | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, encoder: Callable[[Any], Any] | None = PydanticUndefined, models_as_dict: bool = PydanticUndefined, dumps_kwargs: Any = None):
```

**Parameters:**

- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `encoder` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `PydanticUndefined`
- `models_as_dict` (Optional)
  - Type: `bool`
  - Default: `PydanticUndefined`
- `dumps_kwargs` (Optional)
  - Type: `Any`

---

#### `json`

**Signature:**
```python
def json(include: IncEx | None = None, exclude: IncEx | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, encoder: Callable[[Any], Any] | None = PydanticUndefined, models_as_dict: bool = PydanticUndefined, dumps_kwargs: Any = None):
```

**Parameters:**

- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `encoder` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `PydanticUndefined`
- `models_as_dict` (Optional)
  - Type: `bool`
  - Default: `PydanticUndefined`
- `dumps_kwargs` (Optional)
  - Type: `Any`

---

#### `model_construct`

**Signature:**
```python
def model_construct(cls, _fields_set: set[str] | None = None, values: Any = None):
```

**Parameters:**

- `cls` (Required)
- `_fields_set` (Optional)
  - Type: `set[str] | None`
  - Default: `None`
- `values` (Optional)
  - Type: `Any`

**Description:**

Creates a new instance of the `Model` class with validated data.
Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.
!!! note
`model_construct()` generally respects the `model_config.extra` setting on the provided model.
That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
an error if extra values are passed, but they will be ignored.
Args:
_fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
Otherwise, the field names from the `values` argument will be used.
values: Trusted or pre-validated data dictionary.
Returns:
A new instance of the `Model` class with validated data.

---

#### `model_construct`

**Signature:**
```python
def model_construct(_fields_set: set[str] | None = None, values: Any = None):
```

**Parameters:**

- `_fields_set` (Optional)
  - Type: `set[str] | None`
  - Default: `None`
- `values` (Optional)
  - Type: `Any`

**Description:**

Creates a new instance of the `Model` class with validated data.
Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.
!!! note
`model_construct()` generally respects the `model_config.extra` setting on the provided model.
That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
an error if extra values are passed, but they will be ignored.
Args:
_fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
Otherwise, the field names from the `values` argument will be used.
values: Trusted or pre-validated data dictionary.
Returns:
A new instance of the `Model` class with validated data.

---

#### `model_copy`

**Signature:**
```python
def model_copy(update: Mapping[str, Any] | None = None, deep: bool = False):
```

**Parameters:**

- `update` (Optional)
  - Type: `Mapping[str, Any] | None`
  - Default: `None`
- `deep` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_copy`](../concepts/models.md#model-copy)
Returns a copy of the model.
!!! note
The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
might have unexpected side effects if you store anything in it, on top of the model
fields (e.g. the value of [cached properties][functools.cached_property]).
Args:
update: Values to change/add in the new model. Note: the data is not validated
before creating the new model. You should trust this data.
deep: Set to `True` to make a deep copy of the model.
Returns:
New model instance.

---

#### `model_copy`

**Signature:**
```python
def model_copy(update: Mapping[str, Any] | None = None, deep: bool = False):
```

**Parameters:**

- `update` (Optional)
  - Type: `Mapping[str, Any] | None`
  - Default: `None`
- `deep` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_copy`](../concepts/models.md#model-copy)
Returns a copy of the model.
!!! note
The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
might have unexpected side effects if you store anything in it, on top of the model
fields (e.g. the value of [cached properties][functools.cached_property]).
Args:
update: Values to change/add in the new model. Note: the data is not validated
before creating the new model. You should trust this data.
deep: Set to `True` to make a deep copy of the model.
Returns:
New model instance.

---

#### `model_dump`

**Signature:**
```python
def model_dump(mode: Literal['json', 'python'] | str = 'python', include: IncEx | None = None, exclude: IncEx | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False):
```

**Parameters:**

- `mode` (Optional)
  - Type: `Literal['json', 'python'] | str`
  - Default: `'python'`
- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_computed_fields` (Optional)
  - Type: `bool`
  - Default: `False`
- `round_trip` (Optional)
  - Type: `bool`
  - Default: `False`
- `warnings` (Optional)
  - Type: `bool | Literal['none', 'warn', 'error']`
  - Default: `True`
- `fallback` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `None`
- `serialize_as_any` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_dump`](../concepts/serialization.md#python-mode)
Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
Args:
mode: The mode in which `to_python` should run.
If mode is 'json', the output will only contain JSON serializable types.
If mode is 'python', the output may contain non-JSON-serializable Python objects.
include: A set of fields to include in the output.
exclude: A set of fields to exclude from the output.
context: Additional context to pass to the serializer.
by_alias: Whether to use the field's alias in the dictionary key if defined.
exclude_unset: Whether to exclude fields that have not been explicitly set.
exclude_defaults: Whether to exclude fields that are set to their default value.
exclude_none: Whether to exclude fields that have a value of `None`.
exclude_computed_fields: Whether to exclude computed fields.
While this can be useful for round-tripping, it is usually recommended to use the dedicated
`round_trip` parameter instead.
round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
fallback: A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
Returns:
A dictionary representation of the model.

---

#### `model_dump`

**Signature:**
```python
def model_dump(mode: Literal['json', 'python'] | str = 'python', include: IncEx | None = None, exclude: IncEx | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False):
```

**Parameters:**

- `mode` (Optional)
  - Type: `Literal['json', 'python'] | str`
  - Default: `'python'`
- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_computed_fields` (Optional)
  - Type: `bool`
  - Default: `False`
- `round_trip` (Optional)
  - Type: `bool`
  - Default: `False`
- `warnings` (Optional)
  - Type: `bool | Literal['none', 'warn', 'error']`
  - Default: `True`
- `fallback` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `None`
- `serialize_as_any` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_dump`](../concepts/serialization.md#python-mode)
Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
Args:
mode: The mode in which `to_python` should run.
If mode is 'json', the output will only contain JSON serializable types.
If mode is 'python', the output may contain non-JSON-serializable Python objects.
include: A set of fields to include in the output.
exclude: A set of fields to exclude from the output.
context: Additional context to pass to the serializer.
by_alias: Whether to use the field's alias in the dictionary key if defined.
exclude_unset: Whether to exclude fields that have not been explicitly set.
exclude_defaults: Whether to exclude fields that are set to their default value.
exclude_none: Whether to exclude fields that have a value of `None`.
exclude_computed_fields: Whether to exclude computed fields.
While this can be useful for round-tripping, it is usually recommended to use the dedicated
`round_trip` parameter instead.
round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
fallback: A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
Returns:
A dictionary representation of the model.

---

#### `model_dump_json`

**Signature:**
```python
def model_dump_json(indent: int | None = None, ensure_ascii: bool = False, include: IncEx | None = None, exclude: IncEx | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False):
```

**Parameters:**

- `indent` (Optional)
  - Type: `int | None`
  - Default: `None`
- `ensure_ascii` (Optional)
  - Type: `bool`
  - Default: `False`
- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_computed_fields` (Optional)
  - Type: `bool`
  - Default: `False`
- `round_trip` (Optional)
  - Type: `bool`
  - Default: `False`
- `warnings` (Optional)
  - Type: `bool | Literal['none', 'warn', 'error']`
  - Default: `True`
- `fallback` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `None`
- `serialize_as_any` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_dump_json`](../concepts/serialization.md#json-mode)
Generates a JSON representation of the model using Pydantic's `to_json` method.
Args:
indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
If `False` (the default), these characters will be output as-is.
include: Field(s) to include in the JSON output.
exclude: Field(s) to exclude from the JSON output.
context: Additional context to pass to the serializer.
by_alias: Whether to serialize using field aliases.
exclude_unset: Whether to exclude fields that have not been explicitly set.
exclude_defaults: Whether to exclude fields that are set to their default value.
exclude_none: Whether to exclude fields that have a value of `None`.
exclude_computed_fields: Whether to exclude computed fields.
While this can be useful for round-tripping, it is usually recommended to use the dedicated
`round_trip` parameter instead.
round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
fallback: A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
Returns:
A JSON string representation of the model.

---

#### `model_dump_json`

**Signature:**
```python
def model_dump_json(indent: int | None = None, ensure_ascii: bool = False, include: IncEx | None = None, exclude: IncEx | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False):
```

**Parameters:**

- `indent` (Optional)
  - Type: `int | None`
  - Default: `None`
- `ensure_ascii` (Optional)
  - Type: `bool`
  - Default: `False`
- `include` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `exclude` (Optional)
  - Type: `IncEx | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `exclude_unset` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_defaults` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_none` (Optional)
  - Type: `bool`
  - Default: `False`
- `exclude_computed_fields` (Optional)
  - Type: `bool`
  - Default: `False`
- `round_trip` (Optional)
  - Type: `bool`
  - Default: `False`
- `warnings` (Optional)
  - Type: `bool | Literal['none', 'warn', 'error']`
  - Default: `True`
- `fallback` (Optional)
  - Type: `Callable[[Any], Any] | None`
  - Default: `None`
- `serialize_as_any` (Optional)
  - Type: `bool`
  - Default: `False`

**Description:**

!!! abstract "Usage Documentation"
[`model_dump_json`](../concepts/serialization.md#json-mode)
Generates a JSON representation of the model using Pydantic's `to_json` method.
Args:
indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
ensure_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped.
If `False` (the default), these characters will be output as-is.
include: Field(s) to include in the JSON output.
exclude: Field(s) to exclude from the JSON output.
context: Additional context to pass to the serializer.
by_alias: Whether to serialize using field aliases.
exclude_unset: Whether to exclude fields that have not been explicitly set.
exclude_defaults: Whether to exclude fields that are set to their default value.
exclude_none: Whether to exclude fields that have a value of `None`.
exclude_computed_fields: Whether to exclude computed fields.
While this can be useful for round-tripping, it is usually recommended to use the dedicated
`round_trip` parameter instead.
round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
fallback: A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
Returns:
A JSON string representation of the model.

---

#### `model_json_schema`

**Signature:**
```python
def model_json_schema(cls, by_alias: bool = True, ref_template: str = '#/$defs/{model}', schema_generator: type[GenerateJsonSchema] = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: JsonSchemaMode = 'validation', union_format: Literal['any_of', 'primitive_type_array'] = 'any_of'):
```

**Parameters:**

- `cls` (Required)
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`
- `schema_generator` (Optional)
  - Type: `type[GenerateJsonSchema]`
  - Default: `<class 'pydantic.json_schema.GenerateJsonSchema'>`
- `mode` (Optional)
  - Type: `JsonSchemaMode`
  - Default: `'validation'`
- `union_format` (Optional)
  - Type: `Literal['any_of', 'primitive_type_array']`
  - Default: `'any_of'`

**Description:**

Generates a JSON schema for a model class.
Args:
by_alias: Whether to use attribute aliases or not.
ref_template: The reference template.
union_format: The format to use when combining schemas from unions together. Can be one of:
- `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
keyword to combine schemas (the default).
- `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
`any_of`.
schema_generator: To override the logic used to generate the JSON schema, as a subclass of
`GenerateJsonSchema` with your desired modifications
mode: The mode in which to generate the schema.
Returns:
The JSON schema for the given model class.

---

#### `model_json_schema`

**Signature:**
```python
def model_json_schema(by_alias: bool = True, ref_template: str = '#/$defs/{model}', schema_generator: type[GenerateJsonSchema] = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: JsonSchemaMode = 'validation', union_format: Literal['any_of', 'primitive_type_array'] = 'any_of'):
```

**Parameters:**

- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`
- `schema_generator` (Optional)
  - Type: `type[GenerateJsonSchema]`
  - Default: `<class 'pydantic.json_schema.GenerateJsonSchema'>`
- `mode` (Optional)
  - Type: `JsonSchemaMode`
  - Default: `'validation'`
- `union_format` (Optional)
  - Type: `Literal['any_of', 'primitive_type_array']`
  - Default: `'any_of'`

**Description:**

Generates a JSON schema for a model class.
Args:
by_alias: Whether to use attribute aliases or not.
ref_template: The reference template.
union_format: The format to use when combining schemas from unions together. Can be one of:
- `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
keyword to combine schemas (the default).
- `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
`any_of`.
schema_generator: To override the logic used to generate the JSON schema, as a subclass of
`GenerateJsonSchema` with your desired modifications
mode: The mode in which to generate the schema.
Returns:
The JSON schema for the given model class.

---

#### `model_parametrized_name`

**Signature:**
```python
def model_parametrized_name(cls, params: tuple[type[Any], ...]):
```

**Parameters:**

- `cls` (Required)
- `params` (Required)
  - Type: `tuple[type[Any], ...]`

**Description:**

Compute the class name for parametrizations of generic classes.
This method can be overridden to achieve a custom naming scheme for generic BaseModels.
Args:
params: Tuple of types of the class. Given a generic class
`Model` with 2 type variables and a concrete model `Model[str, int]`,
the value `(str, int)` would be passed to `params`.
Returns:
String representing the new class where `params` are passed to `cls` as type variables.
Raises:
TypeError: Raised when trying to generate concrete names for non-generic models.

---

#### `model_parametrized_name`

**Signature:**
```python
def model_parametrized_name(params: tuple[type[Any], ...]):
```

**Parameters:**

- `params` (Required)
  - Type: `tuple[type[Any], ...]`

**Description:**

Compute the class name for parametrizations of generic classes.
This method can be overridden to achieve a custom naming scheme for generic BaseModels.
Args:
params: Tuple of types of the class. Given a generic class
`Model` with 2 type variables and a concrete model `Model[str, int]`,
the value `(str, int)` would be passed to `params`.
Returns:
String representing the new class where `params` are passed to `cls` as type variables.
Raises:
TypeError: Raised when trying to generate concrete names for non-generic models.

---

#### `model_post_init`

**Signature:**
```python
def model_post_init(context: Any):
```

**Parameters:**

- `context` (Required)
  - Type: `Any`

**Description:**

Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

---

#### `model_post_init`

**Signature:**
```python
def model_post_init(context: Any):
```

**Parameters:**

- `context` (Required)
  - Type: `Any`

**Description:**

Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

---

#### `model_rebuild`

**Signature:**
```python
def model_rebuild(cls, force: bool = False, raise_errors: bool = True, _parent_namespace_depth: int = 2, _types_namespace: MappingNamespace | None = None):
```

**Parameters:**

- `cls` (Required)
- `force` (Optional)
  - Type: `bool`
  - Default: `False`
- `raise_errors` (Optional)
  - Type: `bool`
  - Default: `True`
- `_parent_namespace_depth` (Optional)
  - Type: `int`
  - Default: `2`
- `_types_namespace` (Optional)
  - Type: `MappingNamespace | None`
  - Default: `None`

**Description:**

Try to rebuild the pydantic-core schema for the model.
This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.
Args:
force: Whether to force the rebuilding of the model schema, defaults to `False`.
raise_errors: Whether to raise errors, defaults to `True`.
_parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
_types_namespace: The types namespace, defaults to `None`.
Returns:
Returns `None` if the schema is already "complete" and rebuilding was not required.
If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

---

#### `model_rebuild`

**Signature:**
```python
def model_rebuild(force: bool = False, raise_errors: bool = True, _parent_namespace_depth: int = 2, _types_namespace: MappingNamespace | None = None):
```

**Parameters:**

- `force` (Optional)
  - Type: `bool`
  - Default: `False`
- `raise_errors` (Optional)
  - Type: `bool`
  - Default: `True`
- `_parent_namespace_depth` (Optional)
  - Type: `int`
  - Default: `2`
- `_types_namespace` (Optional)
  - Type: `MappingNamespace | None`
  - Default: `None`

**Description:**

Try to rebuild the pydantic-core schema for the model.
This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.
Args:
force: Whether to force the rebuilding of the model schema, defaults to `False`.
raise_errors: Whether to raise errors, defaults to `True`.
_parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
_types_namespace: The types namespace, defaults to `None`.
Returns:
Returns `None` if the schema is already "complete" and rebuilding was not required.
If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

---

#### `model_validate`

**Signature:**
```python
def model_validate(cls, obj: Any, strict: bool | None = None, extra: ExtraValues | None = None, from_attributes: bool | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `cls` (Required)
- `obj` (Required)
  - Type: `Any`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `from_attributes` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

Validate a pydantic model instance.
Args:
obj: The object to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
from_attributes: Whether to extract data from object attributes.
context: Additional context to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Raises:
ValidationError: If the object could not be validated.
Returns:
The validated model instance.

---

#### `model_validate`

**Signature:**
```python
def model_validate(obj: Any, strict: bool | None = None, extra: ExtraValues | None = None, from_attributes: bool | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `obj` (Required)
  - Type: `Any`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `from_attributes` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

Validate a pydantic model instance.
Args:
obj: The object to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
from_attributes: Whether to extract data from object attributes.
context: Additional context to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Raises:
ValidationError: If the object could not be validated.
Returns:
The validated model instance.

---

#### `model_validate_json`

**Signature:**
```python
def model_validate_json(cls, json_data: str | bytes | bytearray, strict: bool | None = None, extra: ExtraValues | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `cls` (Required)
- `json_data` (Required)
  - Type: `str | bytes | bytearray`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

!!! abstract "Usage Documentation"
[JSON Parsing](../concepts/json.md#json-parsing)
Validate the given JSON data against the Pydantic model.
Args:
json_data: The JSON data to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
context: Extra variables to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Returns:
The validated Pydantic model.
Raises:
ValidationError: If `json_data` is not a JSON string or the object could not be validated.

---

#### `model_validate_json`

**Signature:**
```python
def model_validate_json(json_data: str | bytes | bytearray, strict: bool | None = None, extra: ExtraValues | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `json_data` (Required)
  - Type: `str | bytes | bytearray`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

!!! abstract "Usage Documentation"
[JSON Parsing](../concepts/json.md#json-parsing)
Validate the given JSON data against the Pydantic model.
Args:
json_data: The JSON data to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
context: Extra variables to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Returns:
The validated Pydantic model.
Raises:
ValidationError: If `json_data` is not a JSON string or the object could not be validated.

---

#### `model_validate_strings`

**Signature:**
```python
def model_validate_strings(cls, obj: Any, strict: bool | None = None, extra: ExtraValues | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `cls` (Required)
- `obj` (Required)
  - Type: `Any`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

Validate the given object with string data against the Pydantic model.
Args:
obj: The object containing string data to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
context: Extra variables to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Returns:
The validated Pydantic model.

---

#### `model_validate_strings`

**Signature:**
```python
def model_validate_strings(obj: Any, strict: bool | None = None, extra: ExtraValues | None = None, context: Any | None = None, by_alias: bool | None = None, by_name: bool | None = None):
```

**Parameters:**

- `obj` (Required)
  - Type: `Any`
- `strict` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `extra` (Optional)
  - Type: `ExtraValues | None`
  - Default: `None`
- `context` (Optional)
  - Type: `Any | None`
  - Default: `None`
- `by_alias` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `by_name` (Optional)
  - Type: `bool | None`
  - Default: `None`

**Description:**

Validate the given object with string data against the Pydantic model.
Args:
obj: The object containing string data to validate.
strict: Whether to enforce types strictly.
extra: Whether to ignore, allow, or forbid extra data during model validation.
See the [`extra` configuration value][pydantic.ConfigDict.extra] for details.
context: Extra variables to pass to the validator.
by_alias: Whether to use the field's alias when validating against the provided input data.
by_name: Whether to use the field's name when validating against the provided input data.
Returns:
The validated Pydantic model.

---

#### `parse_file`

**Signature:**
```python
def parse_file(cls, path: str | Path, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False):
```

**Parameters:**

- `cls` (Required)
- `path` (Required)
  - Type: `str | Path`
- `content_type` (Optional)
  - Type: `str | None`
  - Default: `None`
- `encoding` (Optional)
  - Type: `str`
  - Default: `'utf8'`
- `proto` (Optional)
  - Type: `DeprecatedParseProtocol | None`
  - Default: `None`
- `allow_pickle` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `parse_file`

**Signature:**
```python
def parse_file(path: str | Path, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False):
```

**Parameters:**

- `path` (Required)
  - Type: `str | Path`
- `content_type` (Optional)
  - Type: `str | None`
  - Default: `None`
- `encoding` (Optional)
  - Type: `str`
  - Default: `'utf8'`
- `proto` (Optional)
  - Type: `DeprecatedParseProtocol | None`
  - Default: `None`
- `allow_pickle` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `parse_obj`

**Signature:**
```python
def parse_obj(cls, obj: Any):
```

**Parameters:**

- `cls` (Required)
- `obj` (Required)
  - Type: `Any`

---

#### `parse_obj`

**Signature:**
```python
def parse_obj(obj: Any):
```

**Parameters:**

- `obj` (Required)
  - Type: `Any`

---

#### `parse_raw`

**Signature:**
```python
def parse_raw(cls, b: str | bytes, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False):
```

**Parameters:**

- `cls` (Required)
- `b` (Required)
  - Type: `str | bytes`
- `content_type` (Optional)
  - Type: `str | None`
  - Default: `None`
- `encoding` (Optional)
  - Type: `str`
  - Default: `'utf8'`
- `proto` (Optional)
  - Type: `DeprecatedParseProtocol | None`
  - Default: `None`
- `allow_pickle` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `parse_raw`

**Signature:**
```python
def parse_raw(b: str | bytes, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False):
```

**Parameters:**

- `b` (Required)
  - Type: `str | bytes`
- `content_type` (Optional)
  - Type: `str | None`
  - Default: `None`
- `encoding` (Optional)
  - Type: `str`
  - Default: `'utf8'`
- `proto` (Optional)
  - Type: `DeprecatedParseProtocol | None`
  - Default: `None`
- `allow_pickle` (Optional)
  - Type: `bool`
  - Default: `False`

---

#### `schema`

**Signature:**
```python
def schema(cls, by_alias: bool = True, ref_template: str = '#/$defs/{model}'):
```

**Parameters:**

- `cls` (Required)
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`

---

#### `schema`

**Signature:**
```python
def schema(by_alias: bool = True, ref_template: str = '#/$defs/{model}'):
```

**Parameters:**

- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`

---

#### `schema_json`

**Signature:**
```python
def schema_json(cls, by_alias: bool = True, ref_template: str = '#/$defs/{model}', dumps_kwargs: Any = None):
```

**Parameters:**

- `cls` (Required)
- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`
- `dumps_kwargs` (Optional)
  - Type: `Any`

---

#### `schema_json`

**Signature:**
```python
def schema_json(by_alias: bool = True, ref_template: str = '#/$defs/{model}', dumps_kwargs: Any = None):
```

**Parameters:**

- `by_alias` (Optional)
  - Type: `bool`
  - Default: `True`
- `ref_template` (Optional)
  - Type: `str`
  - Default: `'#/$defs/{model}'`
- `dumps_kwargs` (Optional)
  - Type: `Any`

---

#### `update_forward_refs`

**Signature:**
```python
def update_forward_refs(cls, localns: Any = None):
```

**Parameters:**

- `cls` (Required)
- `localns` (Optional)
  - Type: `Any`

---

#### `update_forward_refs`

**Signature:**
```python
def update_forward_refs(localns: Any = None):
```

**Parameters:**

- `localns` (Optional)
  - Type: `Any`

---

#### `validate`

**Signature:**
```python
def validate(cls, value: Any):
```

**Parameters:**

- `cls` (Required)
- `value` (Required)
  - Type: `Any`

---

#### `validate`

**Signature:**
```python
def validate(value: Any):
```

**Parameters:**

- `value` (Required)
  - Type: `Any`

---


================================================================================
## OrderType
================================================================================

### Initialization Parameters

```python
OrderType(
    args = None,
    kwds = None,
)
```

*[No public methods found]*


================================================================================
## PolymarketClobClient
================================================================================

### Initialization Parameters

```python
PolymarketClobClient(
    private_key: <class 'str'>,
    address: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)],
    creds: polymarket_apis.types.clob_types.ApiCreds | None = None,
    chain_id: typing.Literal[137, 80002] = 137,
    signature_type: typing.Literal[0, 1, 2] = 1,
)
```

### General

#### `cancel_all`

**Signature:**
```python
def cancel_all():
```

**Description:**

Cancels all available orders for the user.

---

#### `cancel_all`

**Signature:**
```python
def cancel_all():
```

**Description:**

Cancels all available orders for the user.

---

#### `create_api_creds`

**Signature:**
```python
def create_api_creds(nonce: int | None = None):
```

**Parameters:**

- `nonce` (Optional)
  - Type: `int | None`
  - Default: `None`

---

#### `create_api_creds`

**Signature:**
```python
def create_api_creds(nonce: int | None = None):
```

**Parameters:**

- `nonce` (Optional)
  - Type: `int | None`
  - Default: `None`

---

#### `create_or_derive_api_creds`

**Signature:**
```python
def create_or_derive_api_creds(nonce: int | None = None):
```

**Parameters:**

- `nonce` (Optional)
  - Type: `int | None`
  - Default: `None`

---

#### `create_or_derive_api_creds`

**Signature:**
```python
def create_or_derive_api_creds(nonce: int | None = None):
```

**Parameters:**

- `nonce` (Optional)
  - Type: `int | None`
  - Default: `None`

---

#### `create_readonly_api_key`

**Signature:**
```python
def create_readonly_api_key():
```

---

#### `create_readonly_api_key`

**Signature:**
```python
def create_readonly_api_key():
```

---

#### `delete_api_keys`

**Signature:**
```python
def delete_api_keys():
```

---

#### `delete_api_keys`

**Signature:**
```python
def delete_api_keys():
```

---

#### `delete_readonly_api_key`

**Signature:**
```python
def delete_readonly_api_key(key: <class 'str'>):
```

**Parameters:**

- `key` (Required)
  - Type: `<class 'str'>`

---

#### `delete_readonly_api_key`

**Signature:**
```python
def delete_readonly_api_key(key: <class 'str'>):
```

**Parameters:**

- `key` (Required)
  - Type: `<class 'str'>`

---

#### `derive_api_key`

**Signature:**
```python
def derive_api_key(nonce: int | None = None):
```

**Parameters:**

- `nonce` (Optional)
  - Type: `int | None`
  - Default: `None`

---

#### `derive_api_key`

**Signature:**
```python
def derive_api_key(nonce: int | None = None):
```

**Parameters:**

- `nonce` (Optional)
  - Type: `int | None`
  - Default: `None`

---

#### `get_all_history`

**Signature:**
```python
def get_all_history(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

**Description:**

Get the full price history of a token.

---

#### `get_all_history`

**Signature:**
```python
def get_all_history(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

**Description:**

Get the full price history of a token.

---

#### `get_api_keys`

**Signature:**
```python
def get_api_keys():
```

---

#### `get_api_keys`

**Signature:**
```python
def get_api_keys():
```

---

#### `get_fee_rate_bps`

**Signature:**
```python
def get_fee_rate_bps(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

---

#### `get_fee_rate_bps`

**Signature:**
```python
def get_fee_rate_bps(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

---

#### `get_history`

**Signature:**
```python
def get_history(token_id: <class 'str'>, start_time: datetime.datetime | None = None, end_time: datetime.datetime | None = None, fidelity: <class 'int'> = 2):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `start_time` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `end_time` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `fidelity` (Optional)
  - Type: `<class 'int'>`
  - Default: `2`

**Description:**

Get the price history of a token between a selected date range of max 15 days or from start_time to now.

---

#### `get_history`

**Signature:**
```python
def get_history(token_id: <class 'str'>, start_time: datetime.datetime | None = None, end_time: datetime.datetime | None = None, fidelity: <class 'int'> = 2):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `start_time` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `end_time` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `fidelity` (Optional)
  - Type: `<class 'int'>`
  - Default: `2`

**Description:**

Get the price history of a token between a selected date range of max 15 days or from start_time to now.

---

#### `get_midpoint`

**Signature:**
```python
def get_midpoint(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

**Description:**

Get the mid-market price for the given token.

---

#### `get_midpoint`

**Signature:**
```python
def get_midpoint(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

**Description:**

Get the mid-market price for the given token.

---

#### `get_midpoints`

**Signature:**
```python
def get_midpoints(token_ids: list[str]):
```

**Parameters:**

- `token_ids` (Required)
  - Type: `list[str]`

**Description:**

Get the mid-market prices for a set of tokens.

---

#### `get_midpoints`

**Signature:**
```python
def get_midpoints(token_ids: list[str]):
```

**Parameters:**

- `token_ids` (Required)
  - Type: `list[str]`

**Description:**

Get the mid-market prices for a set of tokens.

---

#### `get_neg_risk`

**Signature:**
```python
def get_neg_risk(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

---

#### `get_neg_risk`

**Signature:**
```python
def get_neg_risk(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

---

#### `get_ok`

**Signature:**
```python
def get_ok():
```

---

#### `get_ok`

**Signature:**
```python
def get_ok():
```

---

#### `get_readonly_api_keys`

**Signature:**
```python
def get_readonly_api_keys():
```

---

#### `get_readonly_api_keys`

**Signature:**
```python
def get_readonly_api_keys():
```

---

#### `get_recent_history`

**Signature:**
```python
def get_recent_history(token_id: <class 'str'>, interval: typing.Literal['1h', '6h', '1d', '1w', '1m', 'max'] = '1d', fidelity: <class 'int'> = 1):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `interval` (Optional)
  - Type: `typing.Literal['1h', '6h', '1d', '1w', '1m', 'max']`
  - Default: `'1d'`
- `fidelity` (Optional)
  - Type: `<class 'int'>`
  - Default: `1`

**Description:**

Get the recent price history of a token (up to now) - 1h, 6h, 1d, 1w, 1m.

---

#### `get_recent_history`

**Signature:**
```python
def get_recent_history(token_id: <class 'str'>, interval: typing.Literal['1h', '6h', '1d', '1w', '1m', 'max'] = '1d', fidelity: <class 'int'> = 1):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `interval` (Optional)
  - Type: `typing.Literal['1h', '6h', '1d', '1w', '1m', 'max']`
  - Default: `'1d'`
- `fidelity` (Optional)
  - Type: `<class 'int'>`
  - Default: `1`

**Description:**

Get the recent price history of a token (up to now) - 1h, 6h, 1d, 1w, 1m.

---

#### `get_spread`

**Signature:**
```python
def get_spread(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

**Description:**

Get the spread for the given token.

---

#### `get_spread`

**Signature:**
```python
def get_spread(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

**Description:**

Get the spread for the given token.

---

#### `get_spreads`

**Signature:**
```python
def get_spreads(token_ids: list[str]):
```

**Parameters:**

- `token_ids` (Required)
  - Type: `list[str]`

**Description:**

Get the spreads for a set of tokens.

---

#### `get_spreads`

**Signature:**
```python
def get_spreads(token_ids: list[str]):
```

**Parameters:**

- `token_ids` (Required)
  - Type: `list[str]`

**Description:**

Get the spreads for a set of tokens.

---

#### `get_tick_size`

**Signature:**
```python
def get_tick_size(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

---

#### `get_tick_size`

**Signature:**
```python
def get_tick_size(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

---

#### `get_utc_time`

**Signature:**
```python
def get_utc_time():
```

---

#### `get_utc_time`

**Signature:**
```python
def get_utc_time():
```

---

#### `set_api_creds`

**Signature:**
```python
def set_api_creds(creds: <class 'polymarket_apis.types.clob_types.ApiCreds'>):
```

**Parameters:**

- `creds` (Required)
  - Type: `<class 'polymarket_apis.types.clob_types.ApiCreds'>`

---

#### `set_api_creds`

**Signature:**
```python
def set_api_creds(creds: <class 'polymarket_apis.types.clob_types.ApiCreds'>):
```

**Parameters:**

- `creds` (Required)
  - Type: `<class 'polymarket_apis.types.clob_types.ApiCreds'>`

---

### Market Data

#### `calculate_market_price`

**Signature:**
```python
def calculate_market_price(token_id: <class 'str'>, side: <class 'str'>, amount: <class 'float'>, order_type: <enum 'OrderType'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `side` (Required)
  - Type: `<class 'str'>`
- `amount` (Required)
  - Type: `<class 'float'>`
- `order_type` (Required)
  - Type: `<enum 'OrderType'>`

**Description:**

Calculates the matching price considering an amount and the current orderbook.

---

#### `calculate_market_price`

**Signature:**
```python
def calculate_market_price(token_id: <class 'str'>, side: <class 'str'>, amount: <class 'float'>, order_type: <enum 'OrderType'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `side` (Required)
  - Type: `<class 'str'>`
- `amount` (Required)
  - Type: `<class 'float'>`
- `order_type` (Required)
  - Type: `<enum 'OrderType'>`

**Description:**

Calculates the matching price considering an amount and the current orderbook.

---

#### `get_all_markets`

**Signature:**
```python
def get_all_markets(next_cursor = 'MA=='):
```

**Parameters:**

- `next_cursor` (Optional)
  - Default: `'MA=='`

**Description:**

Recursively fetch all ClobMarkets using pagination.

---

#### `get_all_markets`

**Signature:**
```python
def get_all_markets(next_cursor = 'MA=='):
```

**Parameters:**

- `next_cursor` (Optional)
  - Default: `'MA=='`

**Description:**

Recursively fetch all ClobMarkets using pagination.

---

#### `get_last_trade_price`

**Signature:**
```python
def get_last_trade_price(token_id):
```

**Parameters:**

- `token_id` (Required)

**Description:**

Fetches the last trade price for a token_id.

---

#### `get_last_trade_price`

**Signature:**
```python
def get_last_trade_price(token_id):
```

**Parameters:**

- `token_id` (Required)

**Description:**

Fetches the last trade price for a token_id.

---

#### `get_last_trades_prices`

**Signature:**
```python
def get_last_trades_prices(token_ids: list[str]):
```

**Parameters:**

- `token_ids` (Required)
  - Type: `list[str]`

**Description:**

Fetches the last trades prices for a set of token ids.

---

#### `get_last_trades_prices`

**Signature:**
```python
def get_last_trades_prices(token_ids: list[str]):
```

**Parameters:**

- `token_ids` (Required)
  - Type: `list[str]`

**Description:**

Fetches the last trades prices for a set of token ids.

---

#### `get_market`

**Signature:**
```python
def get_market(condition_id):
```

**Parameters:**

- `condition_id` (Required)

**Description:**

Get a ClobMarket by condition_id.

---

#### `get_market`

**Signature:**
```python
def get_market(condition_id):
```

**Parameters:**

- `condition_id` (Required)

**Description:**

Get a ClobMarket by condition_id.

---

#### `get_market_rewards`

**Signature:**
```python
def get_market_rewards(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`

**Description:**

Get the MarketRewards for a given market (condition_id).
- metadata, tokens, max_spread, min_size, rewards_config, market_competitiveness.

---

#### `get_market_rewards`

**Signature:**
```python
def get_market_rewards(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`

**Description:**

Get the MarketRewards for a given market (condition_id).
- metadata, tokens, max_spread, min_size, rewards_config, market_competitiveness.

---

#### `get_markets`

**Signature:**
```python
def get_markets(next_cursor = 'MA=='):
```

**Parameters:**

- `next_cursor` (Optional)
  - Default: `'MA=='`

**Description:**

Get paginated ClobMarkets.

---

#### `get_markets`

**Signature:**
```python
def get_markets(next_cursor = 'MA=='):
```

**Parameters:**

- `next_cursor` (Optional)
  - Default: `'MA=='`

**Description:**

Get paginated ClobMarkets.

---

#### `get_price`

**Signature:**
```python
def get_price(token_id: <class 'str'>, side: typing.Literal['BUY', 'SELL']):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `side` (Required)
  - Type: `typing.Literal['BUY', 'SELL']`

**Description:**

Get the market price for the given token and side.

---

#### `get_price`

**Signature:**
```python
def get_price(token_id: <class 'str'>, side: typing.Literal['BUY', 'SELL']):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `side` (Required)
  - Type: `typing.Literal['BUY', 'SELL']`

**Description:**

Get the market price for the given token and side.

---

#### `get_prices`

**Signature:**
```python
def get_prices(params: list[polymarket_apis.types.clob_types.BookParams]):
```

**Parameters:**

- `params` (Required)
  - Type: `list[polymarket_apis.types.clob_types.BookParams]`

**Description:**

Get the market prices for a set of tokens and sides.

---

#### `get_prices`

**Signature:**
```python
def get_prices(params: list[polymarket_apis.types.clob_types.BookParams]):
```

**Parameters:**

- `params` (Required)
  - Type: `list[polymarket_apis.types.clob_types.BookParams]`

**Description:**

Get the market prices for a set of tokens and sides.

---

#### `get_reward_markets`

**Signature:**
```python
def get_reward_markets(query: str | None = None, sort_by: typing.Optional[typing.Literal['market', 'max_spread', 'min_size', 'rate_per_day', 'spread', 'price', 'earnings', 'earning_percentage']] = 'market', sort_direction: typing.Optional[typing.Literal['ASC', 'DESC']] = None, show_favorites: <class 'bool'> = False):
```

**Parameters:**

- `query` (Optional)
  - Type: `str | None`
  - Default: `None`
- `sort_by` (Optional)
  - Type: `typing.Optional[typing.Literal['market', 'max_spread', 'min_size', 'rate_per_day', 'spread', 'price', 'earnings', 'earning_percentage']]`
  - Default: `'market'`
- `sort_direction` (Optional)
  - Type: `typing.Optional[typing.Literal['ASC', 'DESC']]`
  - Default: `None`
- `show_favorites` (Optional)
  - Type: `<class 'bool'>`
  - Default: `False`

**Description:**

Search through markets that offer rewards (polymarket.com/rewards items) by query, sorted by different metrics. If query is empty, returns all markets with rewards.
- market start date ("market") - TODO confirm this
- max spread for rewards in usdc
- min size for rewards in shares
- reward rate per day in usdc
- current spread of a market
- current price of a market
- your daily earnings on a market - only need auth for these last two
- your current earning percentage on a market.

---

#### `get_reward_markets`

**Signature:**
```python
def get_reward_markets(query: str | None = None, sort_by: typing.Optional[typing.Literal['market', 'max_spread', 'min_size', 'rate_per_day', 'spread', 'price', 'earnings', 'earning_percentage']] = 'market', sort_direction: typing.Optional[typing.Literal['ASC', 'DESC']] = None, show_favorites: <class 'bool'> = False):
```

**Parameters:**

- `query` (Optional)
  - Type: `str | None`
  - Default: `None`
- `sort_by` (Optional)
  - Type: `typing.Optional[typing.Literal['market', 'max_spread', 'min_size', 'rate_per_day', 'spread', 'price', 'earnings', 'earning_percentage']]`
  - Default: `'market'`
- `sort_direction` (Optional)
  - Type: `typing.Optional[typing.Literal['ASC', 'DESC']]`
  - Default: `None`
- `show_favorites` (Optional)
  - Type: `<class 'bool'>`
  - Default: `False`

**Description:**

Search through markets that offer rewards (polymarket.com/rewards items) by query, sorted by different metrics. If query is empty, returns all markets with rewards.
- market start date ("market") - TODO confirm this
- max spread for rewards in usdc
- min size for rewards in shares
- reward rate per day in usdc
- current spread of a market
- current price of a market
- your daily earnings on a market - only need auth for these last two
- your current earning percentage on a market.

---

### Orders

#### `are_orders_scoring`

**Signature:**
```python
def are_orders_scoring(order_ids: list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]):
```

**Parameters:**

- `order_ids` (Required)
  - Type: `list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]`

**Description:**

Check if the orders are currently scoring.

---

#### `are_orders_scoring`

**Signature:**
```python
def are_orders_scoring(order_ids: list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]):
```

**Parameters:**

- `order_ids` (Required)
  - Type: `list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]`

**Description:**

Check if the orders are currently scoring.

---

#### `cancel_order`

**Signature:**
```python
def cancel_order(order_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]):
```

**Parameters:**

- `order_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`

**Description:**

Cancels an order.

---

#### `cancel_order`

**Signature:**
```python
def cancel_order(order_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]):
```

**Parameters:**

- `order_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`

**Description:**

Cancels an order.

---

#### `cancel_orders`

**Signature:**
```python
def cancel_orders(order_ids: list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]):
```

**Parameters:**

- `order_ids` (Required)
  - Type: `list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]`

**Description:**

Cancels orders.

---

#### `cancel_orders`

**Signature:**
```python
def cancel_orders(order_ids: list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]):
```

**Parameters:**

- `order_ids` (Required)
  - Type: `list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]`

**Description:**

Cancels orders.

---

#### `create_and_post_market_order`

**Signature:**
```python
def create_and_post_market_order(order_args: <class 'polymarket_apis.types.clob_types.MarketOrderArgs'>, options: polymarket_apis.types.clob_types.PartialCreateOrderOptions | None = None, order_type: <enum 'OrderType'> = <OrderType.FOK: 'FOK'>):
```

**Parameters:**

- `order_args` (Required)
  - Type: `<class 'polymarket_apis.types.clob_types.MarketOrderArgs'>`
- `options` (Optional)
  - Type: `polymarket_apis.types.clob_types.PartialCreateOrderOptions | None`
  - Default: `None`
- `order_type` (Optional)
  - Type: `<enum 'OrderType'>`
  - Default: `<OrderType.FOK: 'FOK'>`

**Description:**

Utility function to create and publish a market order.

---

#### `create_and_post_market_order`

**Signature:**
```python
def create_and_post_market_order(order_args: <class 'polymarket_apis.types.clob_types.MarketOrderArgs'>, options: polymarket_apis.types.clob_types.PartialCreateOrderOptions | None = None, order_type: <enum 'OrderType'> = <OrderType.FOK: 'FOK'>):
```

**Parameters:**

- `order_args` (Required)
  - Type: `<class 'polymarket_apis.types.clob_types.MarketOrderArgs'>`
- `options` (Optional)
  - Type: `polymarket_apis.types.clob_types.PartialCreateOrderOptions | None`
  - Default: `None`
- `order_type` (Optional)
  - Type: `<enum 'OrderType'>`
  - Default: `<OrderType.FOK: 'FOK'>`

**Description:**

Utility function to create and publish a market order.

---

#### `create_and_post_order`

**Signature:**
```python
def create_and_post_order(order_args: <class 'polymarket_apis.types.clob_types.OrderArgs'>, options: polymarket_apis.types.clob_types.PartialCreateOrderOptions | None = None, order_type: <enum 'OrderType'> = <OrderType.GTC: 'GTC'>):
```

**Parameters:**

- `order_args` (Required)
  - Type: `<class 'polymarket_apis.types.clob_types.OrderArgs'>`
- `options` (Optional)
  - Type: `polymarket_apis.types.clob_types.PartialCreateOrderOptions | None`
  - Default: `None`
- `order_type` (Optional)
  - Type: `<enum 'OrderType'>`
  - Default: `<OrderType.GTC: 'GTC'>`

**Description:**

Utility function to create and publish an order.

---

#### `create_and_post_order`

**Signature:**
```python
def create_and_post_order(order_args: <class 'polymarket_apis.types.clob_types.OrderArgs'>, options: polymarket_apis.types.clob_types.PartialCreateOrderOptions | None = None, order_type: <enum 'OrderType'> = <OrderType.GTC: 'GTC'>):
```

**Parameters:**

- `order_args` (Required)
  - Type: `<class 'polymarket_apis.types.clob_types.OrderArgs'>`
- `options` (Optional)
  - Type: `polymarket_apis.types.clob_types.PartialCreateOrderOptions | None`
  - Default: `None`
- `order_type` (Optional)
  - Type: `<enum 'OrderType'>`
  - Default: `<OrderType.GTC: 'GTC'>`

**Description:**

Utility function to create and publish an order.

---

#### `create_and_post_orders`

**Signature:**
```python
def create_and_post_orders(args: list[polymarket_apis.types.clob_types.OrderArgs], order_types: list[polymarket_apis.types.clob_types.OrderType]):
```

**Parameters:**

- `args` (Required)
  - Type: `list[polymarket_apis.types.clob_types.OrderArgs]`
- `order_types` (Required)
  - Type: `list[polymarket_apis.types.clob_types.OrderType]`

**Description:**

Utility function to create and publish multiple orders at once.

---

#### `create_and_post_orders`

**Signature:**
```python
def create_and_post_orders(args: list[polymarket_apis.types.clob_types.OrderArgs], order_types: list[polymarket_apis.types.clob_types.OrderType]):
```

**Parameters:**

- `args` (Required)
  - Type: `list[polymarket_apis.types.clob_types.OrderArgs]`
- `order_types` (Required)
  - Type: `list[polymarket_apis.types.clob_types.OrderType]`

**Description:**

Utility function to create and publish multiple orders at once.

---

#### `create_market_order`

**Signature:**
```python
def create_market_order(order_args: <class 'polymarket_apis.types.clob_types.MarketOrderArgs'>, options: polymarket_apis.types.clob_types.PartialCreateOrderOptions | None = None):
```

**Parameters:**

- `order_args` (Required)
  - Type: `<class 'polymarket_apis.types.clob_types.MarketOrderArgs'>`
- `options` (Optional)
  - Type: `polymarket_apis.types.clob_types.PartialCreateOrderOptions | None`
  - Default: `None`

**Description:**

Creates and signs a market order.

---

#### `create_market_order`

**Signature:**
```python
def create_market_order(order_args: <class 'polymarket_apis.types.clob_types.MarketOrderArgs'>, options: polymarket_apis.types.clob_types.PartialCreateOrderOptions | None = None):
```

**Parameters:**

- `order_args` (Required)
  - Type: `<class 'polymarket_apis.types.clob_types.MarketOrderArgs'>`
- `options` (Optional)
  - Type: `polymarket_apis.types.clob_types.PartialCreateOrderOptions | None`
  - Default: `None`

**Description:**

Creates and signs a market order.

---

#### `create_order`

**Signature:**
```python
def create_order(order_args: <class 'polymarket_apis.types.clob_types.OrderArgs'>, options: polymarket_apis.types.clob_types.PartialCreateOrderOptions | None = None):
```

**Parameters:**

- `order_args` (Required)
  - Type: `<class 'polymarket_apis.types.clob_types.OrderArgs'>`
- `options` (Optional)
  - Type: `polymarket_apis.types.clob_types.PartialCreateOrderOptions | None`
  - Default: `None`

**Description:**

Creates and signs an order.

---

#### `create_order`

**Signature:**
```python
def create_order(order_args: <class 'polymarket_apis.types.clob_types.OrderArgs'>, options: polymarket_apis.types.clob_types.PartialCreateOrderOptions | None = None):
```

**Parameters:**

- `order_args` (Required)
  - Type: `<class 'polymarket_apis.types.clob_types.OrderArgs'>`
- `options` (Optional)
  - Type: `polymarket_apis.types.clob_types.PartialCreateOrderOptions | None`
  - Default: `None`

**Description:**

Creates and signs an order.

---

#### `get_order_book`

**Signature:**
```python
def get_order_book(token_id):
```

**Parameters:**

- `token_id` (Required)

**Description:**

Get the orderbook for the given token.

---

#### `get_order_book`

**Signature:**
```python
def get_order_book(token_id):
```

**Parameters:**

- `token_id` (Required)

**Description:**

Get the orderbook for the given token.

---

#### `get_order_books`

**Signature:**
```python
def get_order_books(token_ids: list[str]):
```

**Parameters:**

- `token_ids` (Required)
  - Type: `list[str]`

**Description:**

Get the orderbook for a set of tokens.

---

#### `get_order_books`

**Signature:**
```python
def get_order_books(token_ids: list[str]):
```

**Parameters:**

- `token_ids` (Required)
  - Type: `list[str]`

**Description:**

Get the orderbook for a set of tokens.

---

#### `get_order_books_async`

**Signature:**
```python
def get_order_books_async(token_ids: list[str]):
```

**Parameters:**

- `token_ids` (Required)
  - Type: `list[str]`

**Description:**

Get the orderbook for a set of tokens asynchronously.

---

#### `get_order_books_async`

**Signature:**
```python
def get_order_books_async(token_ids: list[str]):
```

**Parameters:**

- `token_ids` (Required)
  - Type: `list[str]`

**Description:**

Get the orderbook for a set of tokens asynchronously.

---

#### `get_orders`

**Signature:**
```python
def get_orders(order_id: str | None = None, condition_id: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]] = None, token_id: str | None = None, next_cursor: <class 'str'> = 'MA=='):
```

**Parameters:**

- `order_id` (Optional)
  - Type: `str | None`
  - Default: `None`
- `condition_id` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]`
  - Default: `None`
- `token_id` (Optional)
  - Type: `str | None`
  - Default: `None`
- `next_cursor` (Optional)
  - Type: `<class 'str'>`
  - Default: `'MA=='`

**Description:**

Gets your active orders, filtered by order_id, condition_id, token_id.

---

#### `get_orders`

**Signature:**
```python
def get_orders(order_id: str | None = None, condition_id: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]] = None, token_id: str | None = None, next_cursor: <class 'str'> = 'MA=='):
```

**Parameters:**

- `order_id` (Optional)
  - Type: `str | None`
  - Default: `None`
- `condition_id` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]`
  - Default: `None`
- `token_id` (Optional)
  - Type: `str | None`
  - Default: `None`
- `next_cursor` (Optional)
  - Type: `<class 'str'>`
  - Default: `'MA=='`

**Description:**

Gets your active orders, filtered by order_id, condition_id, token_id.

---

#### `is_order_scoring`

**Signature:**
```python
def is_order_scoring(order_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]):
```

**Parameters:**

- `order_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`

**Description:**

Check if the order is currently scoring.

---

#### `is_order_scoring`

**Signature:**
```python
def is_order_scoring(order_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]):
```

**Parameters:**

- `order_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`

**Description:**

Check if the order is currently scoring.

---

#### `post_order`

**Signature:**
```python
def post_order(order: <class 'py_order_utils.model.order.SignedOrder'>, order_type: <enum 'OrderType'> = <OrderType.GTC: 'GTC'>):
```

**Parameters:**

- `order` (Required)
  - Type: `<class 'py_order_utils.model.order.SignedOrder'>`
- `order_type` (Optional)
  - Type: `<enum 'OrderType'>`
  - Default: `<OrderType.GTC: 'GTC'>`

**Description:**

Posts a SignedOrder.

---

#### `post_order`

**Signature:**
```python
def post_order(order: <class 'py_order_utils.model.order.SignedOrder'>, order_type: <enum 'OrderType'> = <OrderType.GTC: 'GTC'>):
```

**Parameters:**

- `order` (Required)
  - Type: `<class 'py_order_utils.model.order.SignedOrder'>`
- `order_type` (Optional)
  - Type: `<enum 'OrderType'>`
  - Default: `<OrderType.GTC: 'GTC'>`

**Description:**

Posts a SignedOrder.

---

#### `post_orders`

**Signature:**
```python
def post_orders(args: list[polymarket_apis.types.clob_types.PostOrdersArgs]):
```

**Parameters:**

- `args` (Required)
  - Type: `list[polymarket_apis.types.clob_types.PostOrdersArgs]`

**Description:**

Posts multiple SignedOrders at once.

---

#### `post_orders`

**Signature:**
```python
def post_orders(args: list[polymarket_apis.types.clob_types.PostOrdersArgs]):
```

**Parameters:**

- `args` (Required)
  - Type: `list[polymarket_apis.types.clob_types.PostOrdersArgs]`

**Description:**

Posts multiple SignedOrders at once.

---

### Portfolio

#### `get_token_balance`

**Signature:**
```python
def get_token_balance(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

---

#### `get_token_balance`

**Signature:**
```python
def get_token_balance(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

---

#### `get_usdc_balance`

**Signature:**
```python
def get_usdc_balance():
```

---

#### `get_usdc_balance`

**Signature:**
```python
def get_usdc_balance():
```

---

### Rewards

#### `get_total_rewards`

**Signature:**
```python
def get_total_rewards(date: datetime.datetime | None = None):
```

**Parameters:**

- `date` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`

**Description:**

Get the total rewards earned on a given date (seems to only hold the 6 most recent data points).

---

#### `get_total_rewards`

**Signature:**
```python
def get_total_rewards(date: datetime.datetime | None = None):
```

**Parameters:**

- `date` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`

**Description:**

Get the total rewards earned on a given date (seems to only hold the 6 most recent data points).

---

### Trades

#### `get_trades`

**Signature:**
```python
def get_trades(condition_id: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]] = None, token_id: str | None = None, trade_id: str | None = None, before: datetime.datetime | None = None, after: datetime.datetime | None = None, address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None, next_cursor = 'MA=='):
```

**Parameters:**

- `condition_id` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]`
  - Default: `None`
- `token_id` (Optional)
  - Type: `str | None`
  - Default: `None`
- `trade_id` (Optional)
  - Type: `str | None`
  - Default: `None`
- `before` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `after` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`
- `next_cursor` (Optional)
  - Default: `'MA=='`

**Description:**

Fetches the trade history for a user.

---

#### `get_trades`

**Signature:**
```python
def get_trades(condition_id: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]] = None, token_id: str | None = None, trade_id: str | None = None, before: datetime.datetime | None = None, after: datetime.datetime | None = None, address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None, next_cursor = 'MA=='):
```

**Parameters:**

- `condition_id` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]`
  - Default: `None`
- `token_id` (Optional)
  - Type: `str | None`
  - Default: `None`
- `trade_id` (Optional)
  - Type: `str | None`
  - Default: `None`
- `before` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `after` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`
- `next_cursor` (Optional)
  - Default: `'MA=='`

**Description:**

Fetches the trade history for a user.

---


================================================================================
## PolymarketDataClient
================================================================================

### Initialization Parameters

```python
PolymarketDataClient(
    base_url: <class 'str'> = 'https://data-api.polymarket.com',
)
```

### General

#### `get_activity`

**Signature:**
```python
def get_activity(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], limit: <class 'int'> = 100, offset: <class 'int'> = 0, condition_id: typing.Union[str, list[str], NoneType] = None, event_id: typing.Union[int, list[int], NoneType] = None, type: typing.Union[typing.Literal['TRADE', 'SPLIT', 'MERGE', 'REDEEM', 'REWARD', 'CONVERSION'], list[typing.Literal['TRADE', 'SPLIT', 'MERGE', 'REDEEM', 'REWARD', 'CONVERSION']], NoneType] = None, start: typing.Optional[datetime.datetime] = None, end: typing.Optional[datetime.datetime] = None, side: typing.Optional[typing.Literal['BUY', 'SELL']] = None, sort_by: typing.Literal['TIMESTAMP', 'TOKENS', 'CASH'] = 'TIMESTAMP', sort_direction: typing.Literal['ASC', 'DESC'] = 'DESC'):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `100`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `condition_id` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`
- `event_id` (Optional)
  - Type: `typing.Union[int, list[int], NoneType]`
  - Default: `None`
- `type` (Optional)
  - Type: `typing.Union[typing.Literal['TRADE', 'SPLIT', 'MERGE', 'REDEEM', 'REWARD', 'CONVERSION'], list[typing.Literal['TRADE', 'SPLIT', 'MERGE', 'REDEEM', 'REWARD', 'CONVERSION']], NoneType]`
  - Default: `None`
- `start` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `end` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `side` (Optional)
  - Type: `typing.Optional[typing.Literal['BUY', 'SELL']]`
  - Default: `None`
- `sort_by` (Optional)
  - Type: `typing.Literal['TIMESTAMP', 'TOKENS', 'CASH']`
  - Default: `'TIMESTAMP'`
- `sort_direction` (Optional)
  - Type: `typing.Literal['ASC', 'DESC']`
  - Default: `'DESC'`

---

#### `get_activity`

**Signature:**
```python
def get_activity(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], limit: <class 'int'> = 100, offset: <class 'int'> = 0, condition_id: typing.Union[str, list[str], NoneType] = None, event_id: typing.Union[int, list[int], NoneType] = None, type: typing.Union[typing.Literal['TRADE', 'SPLIT', 'MERGE', 'REDEEM', 'REWARD', 'CONVERSION'], list[typing.Literal['TRADE', 'SPLIT', 'MERGE', 'REDEEM', 'REWARD', 'CONVERSION']], NoneType] = None, start: typing.Optional[datetime.datetime] = None, end: typing.Optional[datetime.datetime] = None, side: typing.Optional[typing.Literal['BUY', 'SELL']] = None, sort_by: typing.Literal['TIMESTAMP', 'TOKENS', 'CASH'] = 'TIMESTAMP', sort_direction: typing.Literal['ASC', 'DESC'] = 'DESC'):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `100`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `condition_id` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`
- `event_id` (Optional)
  - Type: `typing.Union[int, list[int], NoneType]`
  - Default: `None`
- `type` (Optional)
  - Type: `typing.Union[typing.Literal['TRADE', 'SPLIT', 'MERGE', 'REDEEM', 'REWARD', 'CONVERSION'], list[typing.Literal['TRADE', 'SPLIT', 'MERGE', 'REDEEM', 'REWARD', 'CONVERSION']], NoneType]`
  - Default: `None`
- `start` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `end` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `side` (Optional)
  - Type: `typing.Optional[typing.Literal['BUY', 'SELL']]`
  - Default: `None`
- `sort_by` (Optional)
  - Type: `typing.Literal['TIMESTAMP', 'TOKENS', 'CASH']`
  - Default: `'TIMESTAMP'`
- `sort_direction` (Optional)
  - Type: `typing.Literal['ASC', 'DESC']`
  - Default: `'DESC'`

---

#### `get_holders`

**Signature:**
```python
def get_holders(condition_id: <class 'str'>, limit: <class 'int'> = 500, min_balance: <class 'int'> = 1):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `<class 'str'>`
- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `500`
- `min_balance` (Optional)
  - Type: `<class 'int'>`
  - Default: `1`

**Description:**

Takes in a condition_id and returns top holders for each corresponding token_id.

---

#### `get_holders`

**Signature:**
```python
def get_holders(condition_id: <class 'str'>, limit: <class 'int'> = 500, min_balance: <class 'int'> = 1):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `<class 'str'>`
- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `500`
- `min_balance` (Optional)
  - Type: `<class 'int'>`
  - Default: `1`

**Description:**

Takes in a condition_id and returns top holders for each corresponding token_id.

---

#### `get_leaderboard_top_users`

**Signature:**
```python
def get_leaderboard_top_users(metric: typing.Literal['profit', 'volume'] = 'profit', window: typing.Literal['1d', '7d', '30d', 'all'] = 'all', limit: <class 'int'> = 100):
```

**Parameters:**

- `metric` (Optional)
  - Type: `typing.Literal['profit', 'volume']`
  - Default: `'profit'`
- `window` (Optional)
  - Type: `typing.Literal['1d', '7d', '30d', 'all']`
  - Default: `'all'`
- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `100`

**Description:**

Get the leaderboard of the top at most 100 users by profit or volume.

---

#### `get_leaderboard_top_users`

**Signature:**
```python
def get_leaderboard_top_users(metric: typing.Literal['profit', 'volume'] = 'profit', window: typing.Literal['1d', '7d', '30d', 'all'] = 'all', limit: <class 'int'> = 100):
```

**Parameters:**

- `metric` (Optional)
  - Type: `typing.Literal['profit', 'volume']`
  - Default: `'profit'`
- `window` (Optional)
  - Type: `typing.Literal['1d', '7d', '30d', 'all']`
  - Default: `'all'`
- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `100`

**Description:**

Get the leaderboard of the top at most 100 users by profit or volume.

---

#### `get_leaderboard_user_rank`

**Signature:**
```python
def get_leaderboard_user_rank(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], metric: typing.Literal['profit', 'volume'] = 'profit', window: typing.Literal['1d', '7d', '30d', 'all'] = 'all'):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `metric` (Optional)
  - Type: `typing.Literal['profit', 'volume']`
  - Default: `'profit'`
- `window` (Optional)
  - Type: `typing.Literal['1d', '7d', '30d', 'all']`
  - Default: `'all'`

**Description:**

Get a user's rank on the leaderboard by profit or volume.

---

#### `get_leaderboard_user_rank`

**Signature:**
```python
def get_leaderboard_user_rank(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], metric: typing.Literal['profit', 'volume'] = 'profit', window: typing.Literal['1d', '7d', '30d', 'all'] = 'all'):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `metric` (Optional)
  - Type: `typing.Literal['profit', 'volume']`
  - Default: `'profit'`
- `window` (Optional)
  - Type: `typing.Literal['1d', '7d', '30d', 'all']`
  - Default: `'all'`

**Description:**

Get a user's rank on the leaderboard by profit or volume.

---

#### `get_live_volume`

**Signature:**
```python
def get_live_volume(event_id: <class 'int'>):
```

**Parameters:**

- `event_id` (Required)
  - Type: `<class 'int'>`

**Description:**

Get live volume for a given event.

---

#### `get_live_volume`

**Signature:**
```python
def get_live_volume(event_id: <class 'int'>):
```

**Parameters:**

- `event_id` (Required)
  - Type: `<class 'int'>`

**Description:**

Get live volume for a given event.

---

#### `get_ok`

**Signature:**
```python
def get_ok():
```

---

#### `get_ok`

**Signature:**
```python
def get_ok():
```

---

#### `get_open_interest`

**Signature:**
```python
def get_open_interest(condition_ids: typing.Union[str, list[str], NoneType] = None):
```

**Parameters:**

- `condition_ids` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`

**Description:**

Get open interest.

---

#### `get_open_interest`

**Signature:**
```python
def get_open_interest(condition_ids: typing.Union[str, list[str], NoneType] = None):
```

**Parameters:**

- `condition_ids` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`

**Description:**

Get open interest.

---

#### `get_pnl`

**Signature:**
```python
def get_pnl(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], period: typing.Literal['all', '1m', '1w', '1d'] = 'all', frequency: typing.Literal['1h', '3h', '12h', '1d'] = '1h'):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `period` (Optional)
  - Type: `typing.Literal['all', '1m', '1w', '1d']`
  - Default: `'all'`
- `frequency` (Optional)
  - Type: `typing.Literal['1h', '3h', '12h', '1d']`
  - Default: `'1h'`

**Description:**

Get a user's PnL timeseries in the last day, week, month or all with a given frequency.

---

#### `get_pnl`

**Signature:**
```python
def get_pnl(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], period: typing.Literal['all', '1m', '1w', '1d'] = 'all', frequency: typing.Literal['1h', '3h', '12h', '1d'] = '1h'):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `period` (Optional)
  - Type: `typing.Literal['all', '1m', '1w', '1d']`
  - Default: `'all'`
- `frequency` (Optional)
  - Type: `typing.Literal['1h', '3h', '12h', '1d']`
  - Default: `'1h'`

**Description:**

Get a user's PnL timeseries in the last day, week, month or all with a given frequency.

---

#### `get_user_metric`

**Signature:**
```python
def get_user_metric(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], metric: typing.Literal['profit', 'volume'] = 'profit', window: typing.Literal['1d', '7d', '30d', 'all'] = 'all'):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `metric` (Optional)
  - Type: `typing.Literal['profit', 'volume']`
  - Default: `'profit'`
- `window` (Optional)
  - Type: `typing.Literal['1d', '7d', '30d', 'all']`
  - Default: `'all'`

**Description:**

Get a user's overall profit or volume in the last day, week, month or all.

---

#### `get_user_metric`

**Signature:**
```python
def get_user_metric(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], metric: typing.Literal['profit', 'volume'] = 'profit', window: typing.Literal['1d', '7d', '30d', 'all'] = 'all'):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `metric` (Optional)
  - Type: `typing.Literal['profit', 'volume']`
  - Default: `'profit'`
- `window` (Optional)
  - Type: `typing.Literal['1d', '7d', '30d', 'all']`
  - Default: `'all'`

**Description:**

Get a user's overall profit or volume in the last day, week, month or all.

---

#### `get_value`

**Signature:**
```python
def get_value(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], condition_ids: typing.Union[str, list[str], NoneType] = None):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `condition_ids` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`

**Description:**

Get the current value of a user's position in a set of markets.
Takes in condition_id as:
- None      --> total value of positions
- str       --> value of position
- list[str] --> sum of the values of positions.

---

#### `get_value`

**Signature:**
```python
def get_value(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], condition_ids: typing.Union[str, list[str], NoneType] = None):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `condition_ids` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`

**Description:**

Get the current value of a user's position in a set of markets.
Takes in condition_id as:
- None      --> total value of positions
- str       --> value of position
- list[str] --> sum of the values of positions.

---

### Market Data

#### `get_total_markets_traded`

**Signature:**
```python
def get_total_markets_traded(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`

**Description:**

Get the total number of markets a user has traded in.

---

#### `get_total_markets_traded`

**Signature:**
```python
def get_total_markets_traded(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`

**Description:**

Get the total number of markets a user has traded in.

---

### Portfolio

#### `get_all_positions`

**Signature:**
```python
def get_all_positions(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], size_threshold: <class 'float'> = 0.0):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `size_threshold` (Optional)
  - Type: `<class 'float'>`
  - Default: `0.0`

---

#### `get_all_positions`

**Signature:**
```python
def get_all_positions(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], size_threshold: <class 'float'> = 0.0):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `size_threshold` (Optional)
  - Type: `<class 'float'>`
  - Default: `0.0`

---

#### `get_closed_positions`

**Signature:**
```python
def get_closed_positions(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], condition_ids: typing.Union[str, list[str], NoneType] = None):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `condition_ids` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`

**Description:**

Get all closed positions.

---

#### `get_closed_positions`

**Signature:**
```python
def get_closed_positions(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], condition_ids: typing.Union[str, list[str], NoneType] = None):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `condition_ids` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`

**Description:**

Get all closed positions.

---

#### `get_positions`

**Signature:**
```python
def get_positions(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], condition_id: typing.Union[str, list[str], NoneType] = None, event_id: typing.Union[int, list[int], NoneType] = None, size_threshold: <class 'float'> = 1.0, redeemable: <class 'bool'> = False, mergeable: <class 'bool'> = False, title: typing.Optional[str] = None, limit: <class 'int'> = 100, offset: <class 'int'> = 0, sort_by: typing.Literal['TOKENS', 'CURRENT', 'INITIAL', 'CASHPNL', 'PERCENTPNL', 'TITLE', 'RESOLVING', 'PRICE', 'AVGPRICE'] = 'TOKENS', sort_direction: typing.Literal['ASC', 'DESC'] = 'DESC'):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `condition_id` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`
- `event_id` (Optional)
  - Type: `typing.Union[int, list[int], NoneType]`
  - Default: `None`
- `size_threshold` (Optional)
  - Type: `<class 'float'>`
  - Default: `1.0`
- `redeemable` (Optional)
  - Type: `<class 'bool'>`
  - Default: `False`
- `mergeable` (Optional)
  - Type: `<class 'bool'>`
  - Default: `False`
- `title` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `100`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `sort_by` (Optional)
  - Type: `typing.Literal['TOKENS', 'CURRENT', 'INITIAL', 'CASHPNL', 'PERCENTPNL', 'TITLE', 'RESOLVING', 'PRICE', 'AVGPRICE']`
  - Default: `'TOKENS'`
- `sort_direction` (Optional)
  - Type: `typing.Literal['ASC', 'DESC']`
  - Default: `'DESC'`

---

#### `get_positions`

**Signature:**
```python
def get_positions(user: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], condition_id: typing.Union[str, list[str], NoneType] = None, event_id: typing.Union[int, list[int], NoneType] = None, size_threshold: <class 'float'> = 1.0, redeemable: <class 'bool'> = False, mergeable: <class 'bool'> = False, title: typing.Optional[str] = None, limit: <class 'int'> = 100, offset: <class 'int'> = 0, sort_by: typing.Literal['TOKENS', 'CURRENT', 'INITIAL', 'CASHPNL', 'PERCENTPNL', 'TITLE', 'RESOLVING', 'PRICE', 'AVGPRICE'] = 'TOKENS', sort_direction: typing.Literal['ASC', 'DESC'] = 'DESC'):
```

**Parameters:**

- `user` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `condition_id` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`
- `event_id` (Optional)
  - Type: `typing.Union[int, list[int], NoneType]`
  - Default: `None`
- `size_threshold` (Optional)
  - Type: `<class 'float'>`
  - Default: `1.0`
- `redeemable` (Optional)
  - Type: `<class 'bool'>`
  - Default: `False`
- `mergeable` (Optional)
  - Type: `<class 'bool'>`
  - Default: `False`
- `title` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `100`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `sort_by` (Optional)
  - Type: `typing.Literal['TOKENS', 'CURRENT', 'INITIAL', 'CASHPNL', 'PERCENTPNL', 'TITLE', 'RESOLVING', 'PRICE', 'AVGPRICE']`
  - Default: `'TOKENS'`
- `sort_direction` (Optional)
  - Type: `typing.Literal['ASC', 'DESC']`
  - Default: `'DESC'`

---

### Trades

#### `get_trades`

**Signature:**
```python
def get_trades(limit: <class 'int'> = 100, offset: <class 'int'> = 0, taker_only: <class 'bool'> = True, filter_type: typing.Optional[typing.Literal['CASH', 'TOKENS']] = None, filter_amount: typing.Optional[float] = None, condition_id: typing.Union[str, list[str], NoneType] = None, event_id: typing.Union[int, list[int], NoneType] = None, user: typing.Optional[str] = None, side: typing.Optional[typing.Literal['BUY', 'SELL']] = None):
```

**Parameters:**

- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `100`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `taker_only` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `filter_type` (Optional)
  - Type: `typing.Optional[typing.Literal['CASH', 'TOKENS']]`
  - Default: `None`
- `filter_amount` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `condition_id` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`
- `event_id` (Optional)
  - Type: `typing.Union[int, list[int], NoneType]`
  - Default: `None`
- `user` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `side` (Optional)
  - Type: `typing.Optional[typing.Literal['BUY', 'SELL']]`
  - Default: `None`

---

#### `get_trades`

**Signature:**
```python
def get_trades(limit: <class 'int'> = 100, offset: <class 'int'> = 0, taker_only: <class 'bool'> = True, filter_type: typing.Optional[typing.Literal['CASH', 'TOKENS']] = None, filter_amount: typing.Optional[float] = None, condition_id: typing.Union[str, list[str], NoneType] = None, event_id: typing.Union[int, list[int], NoneType] = None, user: typing.Optional[str] = None, side: typing.Optional[typing.Literal['BUY', 'SELL']] = None):
```

**Parameters:**

- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `100`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `taker_only` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `filter_type` (Optional)
  - Type: `typing.Optional[typing.Literal['CASH', 'TOKENS']]`
  - Default: `None`
- `filter_amount` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `condition_id` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`
- `event_id` (Optional)
  - Type: `typing.Union[int, list[int], NoneType]`
  - Default: `None`
- `user` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `side` (Optional)
  - Type: `typing.Optional[typing.Literal['BUY', 'SELL']]`
  - Default: `None`

---


================================================================================
## PolymarketGammaClient
================================================================================

### Initialization Parameters

```python
PolymarketGammaClient(
    base_url: <class 'str'> = 'https://gamma-api.polymarket.com',
)
```

### Comments

#### `get_comments`

**Signature:**
```python
def get_comments(parent_entity_type: typing.Literal['Event', 'Series', 'market'], parent_entity_id: <class 'int'>, limit = 500, offset = 0, order: typing.Optional[str] = None, ascending: <class 'bool'> = True, get_positions: typing.Optional[bool] = None, holders_only: typing.Optional[bool] = None):
```

**Parameters:**

- `parent_entity_type` (Required)
  - Type: `typing.Literal['Event', 'Series', 'market']`
- `parent_entity_id` (Required)
  - Type: `<class 'int'>`
- `limit` (Optional)
  - Default: `500`
- `offset` (Optional)
  - Default: `0`
- `order` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `get_positions` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `holders_only` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

**Description:**

Warning, the server doesn't give back the right amount of comments you asked for.

---

#### `get_comments`

**Signature:**
```python
def get_comments(parent_entity_type: typing.Literal['Event', 'Series', 'market'], parent_entity_id: <class 'int'>, limit = 500, offset = 0, order: typing.Optional[str] = None, ascending: <class 'bool'> = True, get_positions: typing.Optional[bool] = None, holders_only: typing.Optional[bool] = None):
```

**Parameters:**

- `parent_entity_type` (Required)
  - Type: `typing.Literal['Event', 'Series', 'market']`
- `parent_entity_id` (Required)
  - Type: `<class 'int'>`
- `limit` (Optional)
  - Default: `500`
- `offset` (Optional)
  - Default: `0`
- `order` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `get_positions` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `holders_only` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

**Description:**

Warning, the server doesn't give back the right amount of comments you asked for.

---

#### `get_comments_by_id`

**Signature:**
```python
def get_comments_by_id(comment_id: <class 'str'>, get_positions: typing.Optional[bool] = None):
```

**Parameters:**

- `comment_id` (Required)
  - Type: `<class 'str'>`
- `get_positions` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

**Description:**

Returns all comments that belong to the comment's thread.

---

#### `get_comments_by_id`

**Signature:**
```python
def get_comments_by_id(comment_id: <class 'str'>, get_positions: typing.Optional[bool] = None):
```

**Parameters:**

- `comment_id` (Required)
  - Type: `<class 'str'>`
- `get_positions` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

**Description:**

Returns all comments that belong to the comment's thread.

---

#### `get_comments_by_user_address`

**Signature:**
```python
def get_comments_by_user_address(user_address: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], limit = 500, offset = 0, order: typing.Optional[str] = None, ascending: <class 'bool'> = True):
```

**Parameters:**

- `user_address` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `limit` (Optional)
  - Default: `500`
- `offset` (Optional)
  - Default: `0`
- `order` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

---

#### `get_comments_by_user_address`

**Signature:**
```python
def get_comments_by_user_address(user_address: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], limit = 500, offset = 0, order: typing.Optional[str] = None, ascending: <class 'bool'> = True):
```

**Parameters:**

- `user_address` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `limit` (Optional)
  - Default: `500`
- `offset` (Optional)
  - Default: `0`
- `order` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

---

### Events

#### `get_all_events`

**Signature:**
```python
def get_all_events(order: typing.Optional[str] = None, ascending: <class 'bool'> = True, event_ids: typing.Union[str, list[str], NoneType] = None, slugs: typing.Optional[list[str]] = None, archived: typing.Optional[bool] = None, active: typing.Optional[bool] = None, closed: typing.Optional[bool] = None, liquidity_min: typing.Optional[float] = None, liquidity_max: typing.Optional[float] = None, volume_min: typing.Optional[float] = None, volume_max: typing.Optional[float] = None, start_date_min: typing.Optional[datetime.datetime] = None, start_date_max: typing.Optional[datetime.datetime] = None, end_date_min: typing.Optional[datetime.datetime] = None, end_date_max: typing.Optional[datetime.datetime] = None, tag: typing.Optional[str] = None, tag_id: typing.Optional[int] = None, tag_slug: typing.Optional[str] = None, related_tags: <class 'bool'> = False):
```

**Parameters:**

- `order` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `event_ids` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`
- `slugs` (Optional)
  - Type: `typing.Optional[list[str]]`
  - Default: `None`
- `archived` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `active` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `closed` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `liquidity_min` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `liquidity_max` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `volume_min` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `volume_max` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `start_date_min` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `start_date_max` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `end_date_min` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `end_date_max` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `tag` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `tag_id` (Optional)
  - Type: `typing.Optional[int]`
  - Default: `None`
- `tag_slug` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `related_tags` (Optional)
  - Type: `<class 'bool'>`
  - Default: `False`

---

#### `get_all_events`

**Signature:**
```python
def get_all_events(order: typing.Optional[str] = None, ascending: <class 'bool'> = True, event_ids: typing.Union[str, list[str], NoneType] = None, slugs: typing.Optional[list[str]] = None, archived: typing.Optional[bool] = None, active: typing.Optional[bool] = None, closed: typing.Optional[bool] = None, liquidity_min: typing.Optional[float] = None, liquidity_max: typing.Optional[float] = None, volume_min: typing.Optional[float] = None, volume_max: typing.Optional[float] = None, start_date_min: typing.Optional[datetime.datetime] = None, start_date_max: typing.Optional[datetime.datetime] = None, end_date_min: typing.Optional[datetime.datetime] = None, end_date_max: typing.Optional[datetime.datetime] = None, tag: typing.Optional[str] = None, tag_id: typing.Optional[int] = None, tag_slug: typing.Optional[str] = None, related_tags: <class 'bool'> = False):
```

**Parameters:**

- `order` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `event_ids` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`
- `slugs` (Optional)
  - Type: `typing.Optional[list[str]]`
  - Default: `None`
- `archived` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `active` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `closed` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `liquidity_min` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `liquidity_max` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `volume_min` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `volume_max` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `start_date_min` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `start_date_max` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `end_date_min` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `end_date_max` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `tag` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `tag_id` (Optional)
  - Type: `typing.Optional[int]`
  - Default: `None`
- `tag_slug` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `related_tags` (Optional)
  - Type: `<class 'bool'>`
  - Default: `False`

---

#### `get_event_by_id`

**Signature:**
```python
def get_event_by_id(event_id: <class 'int'>, include_chat: typing.Optional[bool] = None, include_template: typing.Optional[bool] = None):
```

**Parameters:**

- `event_id` (Required)
  - Type: `<class 'int'>`
- `include_chat` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `include_template` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_event_by_id`

**Signature:**
```python
def get_event_by_id(event_id: <class 'int'>, include_chat: typing.Optional[bool] = None, include_template: typing.Optional[bool] = None):
```

**Parameters:**

- `event_id` (Required)
  - Type: `<class 'int'>`
- `include_chat` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `include_template` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_event_by_slug`

**Signature:**
```python
def get_event_by_slug(slug: <class 'str'>, include_chat: typing.Optional[bool] = None, include_template: typing.Optional[bool] = None):
```

**Parameters:**

- `slug` (Required)
  - Type: `<class 'str'>`
- `include_chat` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `include_template` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_event_by_slug`

**Signature:**
```python
def get_event_by_slug(slug: <class 'str'>, include_chat: typing.Optional[bool] = None, include_template: typing.Optional[bool] = None):
```

**Parameters:**

- `slug` (Required)
  - Type: `<class 'str'>`
- `include_chat` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `include_template` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_event_tags`

**Signature:**
```python
def get_event_tags(event_id: <class 'int'>):
```

**Parameters:**

- `event_id` (Required)
  - Type: `<class 'int'>`

---

#### `get_event_tags`

**Signature:**
```python
def get_event_tags(event_id: <class 'int'>):
```

**Parameters:**

- `event_id` (Required)
  - Type: `<class 'int'>`

---

#### `get_events`

**Signature:**
```python
def get_events(limit: <class 'int'> = 500, offset: <class 'int'> = 0, order: typing.Optional[str] = None, ascending: <class 'bool'> = True, event_ids: typing.Union[str, list[str], NoneType] = None, slugs: typing.Optional[list[str]] = None, archived: typing.Optional[bool] = None, active: typing.Optional[bool] = None, closed: typing.Optional[bool] = None, liquidity_min: typing.Optional[float] = None, liquidity_max: typing.Optional[float] = None, volume_min: typing.Optional[float] = None, volume_max: typing.Optional[float] = None, start_date_min: typing.Optional[datetime.datetime] = None, start_date_max: typing.Optional[datetime.datetime] = None, end_date_min: typing.Optional[datetime.datetime] = None, end_date_max: typing.Optional[datetime.datetime] = None, tag: typing.Optional[str] = None, tag_id: typing.Optional[int] = None, tag_slug: typing.Optional[str] = None, related_tags: <class 'bool'> = False):
```

**Parameters:**

- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `500`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `order` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `event_ids` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`
- `slugs` (Optional)
  - Type: `typing.Optional[list[str]]`
  - Default: `None`
- `archived` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `active` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `closed` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `liquidity_min` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `liquidity_max` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `volume_min` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `volume_max` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `start_date_min` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `start_date_max` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `end_date_min` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `end_date_max` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `tag` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `tag_id` (Optional)
  - Type: `typing.Optional[int]`
  - Default: `None`
- `tag_slug` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `related_tags` (Optional)
  - Type: `<class 'bool'>`
  - Default: `False`

---

#### `get_events`

**Signature:**
```python
def get_events(limit: <class 'int'> = 500, offset: <class 'int'> = 0, order: typing.Optional[str] = None, ascending: <class 'bool'> = True, event_ids: typing.Union[str, list[str], NoneType] = None, slugs: typing.Optional[list[str]] = None, archived: typing.Optional[bool] = None, active: typing.Optional[bool] = None, closed: typing.Optional[bool] = None, liquidity_min: typing.Optional[float] = None, liquidity_max: typing.Optional[float] = None, volume_min: typing.Optional[float] = None, volume_max: typing.Optional[float] = None, start_date_min: typing.Optional[datetime.datetime] = None, start_date_max: typing.Optional[datetime.datetime] = None, end_date_min: typing.Optional[datetime.datetime] = None, end_date_max: typing.Optional[datetime.datetime] = None, tag: typing.Optional[str] = None, tag_id: typing.Optional[int] = None, tag_slug: typing.Optional[str] = None, related_tags: <class 'bool'> = False):
```

**Parameters:**

- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `500`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `order` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `event_ids` (Optional)
  - Type: `typing.Union[str, list[str], NoneType]`
  - Default: `None`
- `slugs` (Optional)
  - Type: `typing.Optional[list[str]]`
  - Default: `None`
- `archived` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `active` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `closed` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `liquidity_min` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `liquidity_max` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `volume_min` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `volume_max` (Optional)
  - Type: `typing.Optional[float]`
  - Default: `None`
- `start_date_min` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `start_date_max` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `end_date_min` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `end_date_max` (Optional)
  - Type: `typing.Optional[datetime.datetime]`
  - Default: `None`
- `tag` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `tag_id` (Optional)
  - Type: `typing.Optional[int]`
  - Default: `None`
- `tag_slug` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `related_tags` (Optional)
  - Type: `<class 'bool'>`
  - Default: `False`

---

#### `grok_event_summary`

**Signature:**
```python
def grok_event_summary(event_slug: <class 'str'>):
```

**Parameters:**

- `event_slug` (Required)
  - Type: `<class 'str'>`

---

#### `grok_event_summary`

**Signature:**
```python
def grok_event_summary(event_slug: <class 'str'>):
```

**Parameters:**

- `event_slug` (Required)
  - Type: `<class 'str'>`

---

### General

#### `get_all_series`

**Signature:**
```python
def get_all_series(order: typing.Optional[str] = None, ascending: <class 'bool'> = True, slug: typing.Optional[str] = None, closed: typing.Optional[bool] = None, include_chat: typing.Optional[bool] = None, recurrence: typing.Optional[typing.Literal['hourly', 'daily', 'weekly', 'monthly', 'annual']] = None):
```

**Parameters:**

- `order` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `slug` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `closed` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `include_chat` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `recurrence` (Optional)
  - Type: `typing.Optional[typing.Literal['hourly', 'daily', 'weekly', 'monthly', 'annual']]`
  - Default: `None`

---

#### `get_all_series`

**Signature:**
```python
def get_all_series(order: typing.Optional[str] = None, ascending: <class 'bool'> = True, slug: typing.Optional[str] = None, closed: typing.Optional[bool] = None, include_chat: typing.Optional[bool] = None, recurrence: typing.Optional[typing.Literal['hourly', 'daily', 'weekly', 'monthly', 'annual']] = None):
```

**Parameters:**

- `order` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `slug` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `closed` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `include_chat` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `recurrence` (Optional)
  - Type: `typing.Optional[typing.Literal['hourly', 'daily', 'weekly', 'monthly', 'annual']]`
  - Default: `None`

---

#### `get_all_teams`

**Signature:**
```python
def get_all_teams(order: typing.Optional[typing.Literal['id', 'name', 'league', 'record', 'logo', 'abbreviation', 'alias', 'createdAt', 'updatedAt']] = None, ascending: <class 'bool'> = True, league: typing.Optional[str] = None, name: typing.Optional[str] = None, abbreviation: typing.Optional[str] = None):
```

**Parameters:**

- `order` (Optional)
  - Type: `typing.Optional[typing.Literal['id', 'name', 'league', 'record', 'logo', 'abbreviation', 'alias', 'createdAt', 'updatedAt']]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `league` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `name` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `abbreviation` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`

---

#### `get_all_teams`

**Signature:**
```python
def get_all_teams(order: typing.Optional[typing.Literal['id', 'name', 'league', 'record', 'logo', 'abbreviation', 'alias', 'createdAt', 'updatedAt']] = None, ascending: <class 'bool'> = True, league: typing.Optional[str] = None, name: typing.Optional[str] = None, abbreviation: typing.Optional[str] = None):
```

**Parameters:**

- `order` (Optional)
  - Type: `typing.Optional[typing.Literal['id', 'name', 'league', 'record', 'logo', 'abbreviation', 'alias', 'createdAt', 'updatedAt']]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `league` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `name` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `abbreviation` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`

---

#### `get_series`

**Signature:**
```python
def get_series(limit: <class 'int'> = 300, offset: <class 'int'> = 0, order: typing.Optional[str] = None, ascending: <class 'bool'> = True, slug: typing.Optional[str] = None, closed: typing.Optional[bool] = None, include_chat: typing.Optional[bool] = None, recurrence: typing.Optional[typing.Literal['hourly', 'daily', 'weekly', 'monthly', 'annual']] = None):
```

**Parameters:**

- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `300`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `order` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `slug` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `closed` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `include_chat` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `recurrence` (Optional)
  - Type: `typing.Optional[typing.Literal['hourly', 'daily', 'weekly', 'monthly', 'annual']]`
  - Default: `None`

---

#### `get_series`

**Signature:**
```python
def get_series(limit: <class 'int'> = 300, offset: <class 'int'> = 0, order: typing.Optional[str] = None, ascending: <class 'bool'> = True, slug: typing.Optional[str] = None, closed: typing.Optional[bool] = None, include_chat: typing.Optional[bool] = None, recurrence: typing.Optional[typing.Literal['hourly', 'daily', 'weekly', 'monthly', 'annual']] = None):
```

**Parameters:**

- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `300`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `order` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `slug` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `closed` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `include_chat` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `recurrence` (Optional)
  - Type: `typing.Optional[typing.Literal['hourly', 'daily', 'weekly', 'monthly', 'annual']]`
  - Default: `None`

---

#### `get_series_by_id`

**Signature:**
```python
def get_series_by_id(series_id: <class 'str'>):
```

**Parameters:**

- `series_id` (Required)
  - Type: `<class 'str'>`

---

#### `get_series_by_id`

**Signature:**
```python
def get_series_by_id(series_id: <class 'str'>):
```

**Parameters:**

- `series_id` (Required)
  - Type: `<class 'str'>`

---

#### `get_sports_metadata`

**Signature:**
```python
def get_sports_metadata():
```

---

#### `get_sports_metadata`

**Signature:**
```python
def get_sports_metadata():
```

---

#### `get_teams`

**Signature:**
```python
def get_teams(limit: <class 'int'> = 500, offset: <class 'int'> = 0, order: typing.Optional[typing.Literal['id', 'name', 'league', 'record', 'logo', 'abbreviation', 'alias', 'createdAt', 'updatedAt']] = None, ascending: <class 'bool'> = True, league: typing.Optional[str] = None, name: typing.Optional[str] = None, abbreviation: typing.Optional[str] = None):
```

**Parameters:**

- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `500`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `order` (Optional)
  - Type: `typing.Optional[typing.Literal['id', 'name', 'league', 'record', 'logo', 'abbreviation', 'alias', 'createdAt', 'updatedAt']]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `league` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `name` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `abbreviation` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`

---

#### `get_teams`

**Signature:**
```python
def get_teams(limit: <class 'int'> = 500, offset: <class 'int'> = 0, order: typing.Optional[typing.Literal['id', 'name', 'league', 'record', 'logo', 'abbreviation', 'alias', 'createdAt', 'updatedAt']] = None, ascending: <class 'bool'> = True, league: typing.Optional[str] = None, name: typing.Optional[str] = None, abbreviation: typing.Optional[str] = None):
```

**Parameters:**

- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `500`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `order` (Optional)
  - Type: `typing.Optional[typing.Literal['id', 'name', 'league', 'record', 'logo', 'abbreviation', 'alias', 'createdAt', 'updatedAt']]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `league` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `name` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`
- `abbreviation` (Optional)
  - Type: `typing.Optional[str]`
  - Default: `None`

---

### Market Data

#### `get_market`

**Signature:**
```python
def get_market(market_id: <class 'str'>):
```

**Parameters:**

- `market_id` (Required)
  - Type: `<class 'str'>`

**Description:**

Get a GammaMarket by market_id.

---

#### `get_market`

**Signature:**
```python
def get_market(market_id: <class 'str'>):
```

**Parameters:**

- `market_id` (Required)
  - Type: `<class 'str'>`

**Description:**

Get a GammaMarket by market_id.

---

#### `get_market_by_id`

**Signature:**
```python
def get_market_by_id(market_id: <class 'str'>, include_tag: typing.Optional[bool] = None):
```

**Parameters:**

- `market_id` (Required)
  - Type: `<class 'str'>`
- `include_tag` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_market_by_id`

**Signature:**
```python
def get_market_by_id(market_id: <class 'str'>, include_tag: typing.Optional[bool] = None):
```

**Parameters:**

- `market_id` (Required)
  - Type: `<class 'str'>`
- `include_tag` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_market_by_slug`

**Signature:**
```python
def get_market_by_slug(slug: <class 'str'>, include_tag: typing.Optional[bool] = None):
```

**Parameters:**

- `slug` (Required)
  - Type: `<class 'str'>`
- `include_tag` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_market_by_slug`

**Signature:**
```python
def get_market_by_slug(slug: <class 'str'>, include_tag: typing.Optional[bool] = None):
```

**Parameters:**

- `slug` (Required)
  - Type: `<class 'str'>`
- `include_tag` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_market_tags`

**Signature:**
```python
def get_market_tags(market_id: <class 'str'>):
```

**Parameters:**

- `market_id` (Required)
  - Type: `<class 'str'>`

---

#### `get_market_tags`

**Signature:**
```python
def get_market_tags(market_id: <class 'str'>):
```

**Parameters:**

- `market_id` (Required)
  - Type: `<class 'str'>`

---

#### `get_markets`

**Signature:**
```python
def get_markets(limit: int | None = None, offset: int | None = None, order: str | None = None, ascending: <class 'bool'> = True, archived: bool | None = None, active: bool | None = None, closed: bool | None = None, slugs: list[str] | None = None, market_ids: list[int] | None = None, token_ids: list[str] | None = None, condition_ids: list[str] | None = None, tag_id: int | None = None, related_tags: bool | None = False, liquidity_num_min: float | None = None, liquidity_num_max: float | None = None, volume_num_min: float | None = None, volume_num_max: float | None = None, start_date_min: datetime.datetime | None = None, start_date_max: datetime.datetime | None = None, end_date_min: datetime.datetime | None = None, end_date_max: datetime.datetime | None = None):
```

**Parameters:**

- `limit` (Optional)
  - Type: `int | None`
  - Default: `None`
- `offset` (Optional)
  - Type: `int | None`
  - Default: `None`
- `order` (Optional)
  - Type: `str | None`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `archived` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `active` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `closed` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `slugs` (Optional)
  - Type: `list[str] | None`
  - Default: `None`
- `market_ids` (Optional)
  - Type: `list[int] | None`
  - Default: `None`
- `token_ids` (Optional)
  - Type: `list[str] | None`
  - Default: `None`
- `condition_ids` (Optional)
  - Type: `list[str] | None`
  - Default: `None`
- `tag_id` (Optional)
  - Type: `int | None`
  - Default: `None`
- `related_tags` (Optional)
  - Type: `bool | None`
  - Default: `False`
- `liquidity_num_min` (Optional)
  - Type: `float | None`
  - Default: `None`
- `liquidity_num_max` (Optional)
  - Type: `float | None`
  - Default: `None`
- `volume_num_min` (Optional)
  - Type: `float | None`
  - Default: `None`
- `volume_num_max` (Optional)
  - Type: `float | None`
  - Default: `None`
- `start_date_min` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `start_date_max` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `end_date_min` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `end_date_max` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`

---

#### `get_markets`

**Signature:**
```python
def get_markets(limit: int | None = None, offset: int | None = None, order: str | None = None, ascending: <class 'bool'> = True, archived: bool | None = None, active: bool | None = None, closed: bool | None = None, slugs: list[str] | None = None, market_ids: list[int] | None = None, token_ids: list[str] | None = None, condition_ids: list[str] | None = None, tag_id: int | None = None, related_tags: bool | None = False, liquidity_num_min: float | None = None, liquidity_num_max: float | None = None, volume_num_min: float | None = None, volume_num_max: float | None = None, start_date_min: datetime.datetime | None = None, start_date_max: datetime.datetime | None = None, end_date_min: datetime.datetime | None = None, end_date_max: datetime.datetime | None = None):
```

**Parameters:**

- `limit` (Optional)
  - Type: `int | None`
  - Default: `None`
- `offset` (Optional)
  - Type: `int | None`
  - Default: `None`
- `order` (Optional)
  - Type: `str | None`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `archived` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `active` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `closed` (Optional)
  - Type: `bool | None`
  - Default: `None`
- `slugs` (Optional)
  - Type: `list[str] | None`
  - Default: `None`
- `market_ids` (Optional)
  - Type: `list[int] | None`
  - Default: `None`
- `token_ids` (Optional)
  - Type: `list[str] | None`
  - Default: `None`
- `condition_ids` (Optional)
  - Type: `list[str] | None`
  - Default: `None`
- `tag_id` (Optional)
  - Type: `int | None`
  - Default: `None`
- `related_tags` (Optional)
  - Type: `bool | None`
  - Default: `False`
- `liquidity_num_min` (Optional)
  - Type: `float | None`
  - Default: `None`
- `liquidity_num_max` (Optional)
  - Type: `float | None`
  - Default: `None`
- `volume_num_min` (Optional)
  - Type: `float | None`
  - Default: `None`
- `volume_num_max` (Optional)
  - Type: `float | None`
  - Default: `None`
- `start_date_min` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `start_date_max` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `end_date_min` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`
- `end_date_max` (Optional)
  - Type: `datetime.datetime | None`
  - Default: `None`

---

#### `grok_election_market_explanation`

**Signature:**
```python
def grok_election_market_explanation(candidate_name: <class 'str'>, election_title: <class 'str'>):
```

**Parameters:**

- `candidate_name` (Required)
  - Type: `<class 'str'>`
- `election_title` (Required)
  - Type: `<class 'str'>`

---

#### `grok_election_market_explanation`

**Signature:**
```python
def grok_election_market_explanation(candidate_name: <class 'str'>, election_title: <class 'str'>):
```

**Parameters:**

- `candidate_name` (Required)
  - Type: `<class 'str'>`
- `election_title` (Required)
  - Type: `<class 'str'>`

---

### Search

#### `search`

**Signature:**
```python
def search(query: <class 'str'>, cache: typing.Optional[bool] = None, status: typing.Optional[typing.Literal['active', 'resolved']] = None, limit_per_type: typing.Optional[int] = None, page: typing.Optional[int] = None, tags: typing.Optional[list[str]] = None, keep_closed_markets: typing.Optional[bool] = None, sort: typing.Optional[typing.Literal['volume', 'volume_24hr', 'liquidity', 'start_date', 'end_date', 'competitive']] = None, ascending: typing.Optional[bool] = None, search_tags: typing.Optional[bool] = None, search_profiles: typing.Optional[bool] = None, recurrence: typing.Optional[typing.Literal['hourly', 'daily', 'weekly', 'monthly', 'annual']] = None, exclude_tag_ids: typing.Optional[list[int]] = None, optimized: typing.Optional[bool] = None):
```

**Parameters:**

- `query` (Required)
  - Type: `<class 'str'>`
- `cache` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `status` (Optional)
  - Type: `typing.Optional[typing.Literal['active', 'resolved']]`
  - Default: `None`
- `limit_per_type` (Optional)
  - Type: `typing.Optional[int]`
  - Default: `None`
- `page` (Optional)
  - Type: `typing.Optional[int]`
  - Default: `None`
- `tags` (Optional)
  - Type: `typing.Optional[list[str]]`
  - Default: `None`
- `keep_closed_markets` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `sort` (Optional)
  - Type: `typing.Optional[typing.Literal['volume', 'volume_24hr', 'liquidity', 'start_date', 'end_date', 'competitive']]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `search_tags` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `search_profiles` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `recurrence` (Optional)
  - Type: `typing.Optional[typing.Literal['hourly', 'daily', 'weekly', 'monthly', 'annual']]`
  - Default: `None`
- `exclude_tag_ids` (Optional)
  - Type: `typing.Optional[list[int]]`
  - Default: `None`
- `optimized` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `search`

**Signature:**
```python
def search(query: <class 'str'>, cache: typing.Optional[bool] = None, status: typing.Optional[typing.Literal['active', 'resolved']] = None, limit_per_type: typing.Optional[int] = None, page: typing.Optional[int] = None, tags: typing.Optional[list[str]] = None, keep_closed_markets: typing.Optional[bool] = None, sort: typing.Optional[typing.Literal['volume', 'volume_24hr', 'liquidity', 'start_date', 'end_date', 'competitive']] = None, ascending: typing.Optional[bool] = None, search_tags: typing.Optional[bool] = None, search_profiles: typing.Optional[bool] = None, recurrence: typing.Optional[typing.Literal['hourly', 'daily', 'weekly', 'monthly', 'annual']] = None, exclude_tag_ids: typing.Optional[list[int]] = None, optimized: typing.Optional[bool] = None):
```

**Parameters:**

- `query` (Required)
  - Type: `<class 'str'>`
- `cache` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `status` (Optional)
  - Type: `typing.Optional[typing.Literal['active', 'resolved']]`
  - Default: `None`
- `limit_per_type` (Optional)
  - Type: `typing.Optional[int]`
  - Default: `None`
- `page` (Optional)
  - Type: `typing.Optional[int]`
  - Default: `None`
- `tags` (Optional)
  - Type: `typing.Optional[list[str]]`
  - Default: `None`
- `keep_closed_markets` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `sort` (Optional)
  - Type: `typing.Optional[typing.Literal['volume', 'volume_24hr', 'liquidity', 'start_date', 'end_date', 'competitive']]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `search_tags` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `search_profiles` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `recurrence` (Optional)
  - Type: `typing.Optional[typing.Literal['hourly', 'daily', 'weekly', 'monthly', 'annual']]`
  - Default: `None`
- `exclude_tag_ids` (Optional)
  - Type: `typing.Optional[list[int]]`
  - Default: `None`
- `optimized` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

### Tags

#### `get_all_tags`

**Signature:**
```python
def get_all_tags(order: typing.Optional[typing.Literal['id', 'label', 'slug', 'forceShow', 'forceHide', 'isCarousel', 'createdAt', 'updatedAt', 'createdBy', 'updatedBy']] = None, ascending: <class 'bool'> = True, include_templates: typing.Optional[bool] = None, is_carousel: typing.Optional[bool] = None):
```

**Parameters:**

- `order` (Optional)
  - Type: `typing.Optional[typing.Literal['id', 'label', 'slug', 'forceShow', 'forceHide', 'isCarousel', 'createdAt', 'updatedAt', 'createdBy', 'updatedBy']]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `include_templates` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `is_carousel` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_all_tags`

**Signature:**
```python
def get_all_tags(order: typing.Optional[typing.Literal['id', 'label', 'slug', 'forceShow', 'forceHide', 'isCarousel', 'createdAt', 'updatedAt', 'createdBy', 'updatedBy']] = None, ascending: <class 'bool'> = True, include_templates: typing.Optional[bool] = None, is_carousel: typing.Optional[bool] = None):
```

**Parameters:**

- `order` (Optional)
  - Type: `typing.Optional[typing.Literal['id', 'label', 'slug', 'forceShow', 'forceHide', 'isCarousel', 'createdAt', 'updatedAt', 'createdBy', 'updatedBy']]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `include_templates` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `is_carousel` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_related_tag_ids_by_slug`

**Signature:**
```python
def get_related_tag_ids_by_slug(slug: <class 'str'>, omit_empty: typing.Optional[bool] = None, status: typing.Optional[typing.Literal['active', 'closed', 'all']] = None):
```

**Parameters:**

- `slug` (Required)
  - Type: `<class 'str'>`
- `omit_empty` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `status` (Optional)
  - Type: `typing.Optional[typing.Literal['active', 'closed', 'all']]`
  - Default: `None`

---

#### `get_related_tag_ids_by_slug`

**Signature:**
```python
def get_related_tag_ids_by_slug(slug: <class 'str'>, omit_empty: typing.Optional[bool] = None, status: typing.Optional[typing.Literal['active', 'closed', 'all']] = None):
```

**Parameters:**

- `slug` (Required)
  - Type: `<class 'str'>`
- `omit_empty` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `status` (Optional)
  - Type: `typing.Optional[typing.Literal['active', 'closed', 'all']]`
  - Default: `None`

---

#### `get_related_tag_ids_by_tag_id`

**Signature:**
```python
def get_related_tag_ids_by_tag_id(tag_id: <class 'int'>, omit_empty: typing.Optional[bool] = None, status: typing.Optional[typing.Literal['active', 'closed', 'all']] = None):
```

**Parameters:**

- `tag_id` (Required)
  - Type: `<class 'int'>`
- `omit_empty` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `status` (Optional)
  - Type: `typing.Optional[typing.Literal['active', 'closed', 'all']]`
  - Default: `None`

---

#### `get_related_tag_ids_by_tag_id`

**Signature:**
```python
def get_related_tag_ids_by_tag_id(tag_id: <class 'int'>, omit_empty: typing.Optional[bool] = None, status: typing.Optional[typing.Literal['active', 'closed', 'all']] = None):
```

**Parameters:**

- `tag_id` (Required)
  - Type: `<class 'int'>`
- `omit_empty` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `status` (Optional)
  - Type: `typing.Optional[typing.Literal['active', 'closed', 'all']]`
  - Default: `None`

---

#### `get_related_tags_by_slug`

**Signature:**
```python
def get_related_tags_by_slug(slug: <class 'str'>, omit_empty: typing.Optional[bool] = None, status: typing.Optional[typing.Literal['active', 'closed', 'all']] = None):
```

**Parameters:**

- `slug` (Required)
  - Type: `<class 'str'>`
- `omit_empty` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `status` (Optional)
  - Type: `typing.Optional[typing.Literal['active', 'closed', 'all']]`
  - Default: `None`

---

#### `get_related_tags_by_slug`

**Signature:**
```python
def get_related_tags_by_slug(slug: <class 'str'>, omit_empty: typing.Optional[bool] = None, status: typing.Optional[typing.Literal['active', 'closed', 'all']] = None):
```

**Parameters:**

- `slug` (Required)
  - Type: `<class 'str'>`
- `omit_empty` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `status` (Optional)
  - Type: `typing.Optional[typing.Literal['active', 'closed', 'all']]`
  - Default: `None`

---

#### `get_related_tags_by_tag_id`

**Signature:**
```python
def get_related_tags_by_tag_id(tag_id: <class 'int'>, omit_empty: typing.Optional[bool] = None, status: typing.Optional[typing.Literal['active', 'closed', 'all']] = None):
```

**Parameters:**

- `tag_id` (Required)
  - Type: `<class 'int'>`
- `omit_empty` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `status` (Optional)
  - Type: `typing.Optional[typing.Literal['active', 'closed', 'all']]`
  - Default: `None`

---

#### `get_related_tags_by_tag_id`

**Signature:**
```python
def get_related_tags_by_tag_id(tag_id: <class 'int'>, omit_empty: typing.Optional[bool] = None, status: typing.Optional[typing.Literal['active', 'closed', 'all']] = None):
```

**Parameters:**

- `tag_id` (Required)
  - Type: `<class 'int'>`
- `omit_empty` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `status` (Optional)
  - Type: `typing.Optional[typing.Literal['active', 'closed', 'all']]`
  - Default: `None`

---

#### `get_tag`

**Signature:**
```python
def get_tag(tag_id: <class 'str'>, include_template: typing.Optional[bool] = None):
```

**Parameters:**

- `tag_id` (Required)
  - Type: `<class 'str'>`
- `include_template` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_tag`

**Signature:**
```python
def get_tag(tag_id: <class 'str'>, include_template: typing.Optional[bool] = None):
```

**Parameters:**

- `tag_id` (Required)
  - Type: `<class 'str'>`
- `include_template` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_tags`

**Signature:**
```python
def get_tags(limit: <class 'int'> = 300, offset: <class 'int'> = 0, order: typing.Optional[typing.Literal['id', 'label', 'slug', 'forceShow', 'forceHide', 'isCarousel', 'createdAt', 'updatedAt', 'createdBy', 'updatedBy']] = None, ascending: <class 'bool'> = True, include_templates: typing.Optional[bool] = None, is_carousel: typing.Optional[bool] = None):
```

**Parameters:**

- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `300`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `order` (Optional)
  - Type: `typing.Optional[typing.Literal['id', 'label', 'slug', 'forceShow', 'forceHide', 'isCarousel', 'createdAt', 'updatedAt', 'createdBy', 'updatedBy']]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `include_templates` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `is_carousel` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---

#### `get_tags`

**Signature:**
```python
def get_tags(limit: <class 'int'> = 300, offset: <class 'int'> = 0, order: typing.Optional[typing.Literal['id', 'label', 'slug', 'forceShow', 'forceHide', 'isCarousel', 'createdAt', 'updatedAt', 'createdBy', 'updatedBy']] = None, ascending: <class 'bool'> = True, include_templates: typing.Optional[bool] = None, is_carousel: typing.Optional[bool] = None):
```

**Parameters:**

- `limit` (Optional)
  - Type: `<class 'int'>`
  - Default: `300`
- `offset` (Optional)
  - Type: `<class 'int'>`
  - Default: `0`
- `order` (Optional)
  - Type: `typing.Optional[typing.Literal['id', 'label', 'slug', 'forceShow', 'forceHide', 'isCarousel', 'createdAt', 'updatedAt', 'createdBy', 'updatedBy']]`
  - Default: `None`
- `ascending` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`
- `include_templates` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`
- `is_carousel` (Optional)
  - Type: `typing.Optional[bool]`
  - Default: `None`

---


================================================================================
## PolymarketGaslessWeb3Client
================================================================================

Polymarket Web3 client for gasless transactions via relay.

### Initialization Parameters

```python
PolymarketGaslessWeb3Client(
    private_key: <class 'str'>,
    signature_type: typing.Literal[1, 2] = 1,
    builder_creds: polymarket_apis.types.clob_types.ApiCreds | None = None,
    chain_id: typing.Literal[137, 80002] = 137,
)
```

### General

#### `get_base_address`

**Signature:**
```python
def get_base_address():
```

**Description:**

Get the base EOA address.

---

#### `get_base_address`

**Signature:**
```python
def get_base_address():
```

**Description:**

Get the base EOA address.

---

#### `get_condition_id_neg_risk`

**Signature:**
```python
def get_condition_id_neg_risk(question_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]):
```

**Parameters:**

- `question_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`

**Description:**

Get condition ID for a neg risk market.
Returns a keccak256 hash of the oracle and question id.

---

#### `get_condition_id_neg_risk`

**Signature:**
```python
def get_condition_id_neg_risk(question_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]):
```

**Parameters:**

- `question_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`

**Description:**

Get condition ID for a neg risk market.
Returns a keccak256 hash of the oracle and question id.

---

#### `get_poly_proxy_address`

**Signature:**
```python
def get_poly_proxy_address(address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get the Polymarket proxy address.

---

#### `get_poly_proxy_address`

**Signature:**
```python
def get_poly_proxy_address(address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get the Polymarket proxy address.

---

#### `get_safe_proxy_address`

**Signature:**
```python
def get_safe_proxy_address(address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get the Safe proxy address.

---

#### `get_safe_proxy_address`

**Signature:**
```python
def get_safe_proxy_address(address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get the Safe proxy address.

---

#### `get_token_complement`

**Signature:**
```python
def get_token_complement(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

**Description:**

Get the complement token ID.

---

#### `get_token_complement`

**Signature:**
```python
def get_token_complement(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

**Description:**

Get the complement token ID.

---

### Portfolio

#### `convert_positions`

**Signature:**
```python
def convert_positions(question_ids: list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]], amount: <class 'float'>):
```

**Parameters:**

- `question_ids` (Required)
  - Type: `list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]`
- `amount` (Required)
  - Type: `<class 'float'>`

**Description:**

Convert neg risk No positions to Yes positions and USDC.
Args:
question_ids: Array of question_ids representing positions to convert
amount: Number of shares to convert

---

#### `convert_positions`

**Signature:**
```python
def convert_positions(question_ids: list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]], amount: <class 'float'>):
```

**Parameters:**

- `question_ids` (Required)
  - Type: `list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]`
- `amount` (Required)
  - Type: `<class 'float'>`

**Description:**

Convert neg risk No positions to Yes positions and USDC.
Args:
question_ids: Array of question_ids representing positions to convert
amount: Number of shares to convert

---

#### `get_pol_balance`

**Signature:**
```python
def get_pol_balance():
```

**Description:**

Get POL balance for the base address associated with the private key.

---

#### `get_pol_balance`

**Signature:**
```python
def get_pol_balance():
```

**Description:**

Get POL balance for the base address associated with the private key.

---

#### `get_token_balance`

**Signature:**
```python
def get_token_balance(token_id: <class 'str'>, address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get token balance of an address.

---

#### `get_token_balance`

**Signature:**
```python
def get_token_balance(token_id: <class 'str'>, address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get token balance of an address.

---

#### `get_usdc_balance`

**Signature:**
```python
def get_usdc_balance(address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get USDC balance of an address.
If no address is given, returns the balance of the instantiated client.

---

#### `get_usdc_balance`

**Signature:**
```python
def get_usdc_balance(address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get USDC balance of an address.
If no address is given, returns the balance of the instantiated client.

---

#### `merge_position`

**Signature:**
```python
def merge_position(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)], amount: <class 'float'>, neg_risk: <class 'bool'> = True):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`
- `amount` (Required)
  - Type: `<class 'float'>`
- `neg_risk` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

**Description:**

Merge two complementary positions into USDC.

---

#### `merge_position`

**Signature:**
```python
def merge_position(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)], amount: <class 'float'>, neg_risk: <class 'bool'> = True):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`
- `amount` (Required)
  - Type: `<class 'float'>`
- `neg_risk` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

**Description:**

Merge two complementary positions into USDC.

---

#### `redeem_position`

**Signature:**
```python
def redeem_position(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)], amounts: list[float], neg_risk: <class 'bool'> = True):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`
- `amounts` (Required)
  - Type: `list[float]`
- `neg_risk` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

**Description:**

Redeem positions into USDC.
Args:
condition_id: Condition ID
amounts: List of amounts [x, y] where x is shares of first outcome,
y is shares of second outcome
neg_risk: Whether this is a neg risk market

---

#### `redeem_position`

**Signature:**
```python
def redeem_position(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)], amounts: list[float], neg_risk: <class 'bool'> = True):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`
- `amounts` (Required)
  - Type: `list[float]`
- `neg_risk` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

**Description:**

Redeem positions into USDC.
Args:
condition_id: Condition ID
amounts: List of amounts [x, y] where x is shares of first outcome,
y is shares of second outcome
neg_risk: Whether this is a neg risk market

---

#### `split_position`

**Signature:**
```python
def split_position(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)], amount: <class 'float'>, neg_risk: <class 'bool'> = True):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`
- `amount` (Required)
  - Type: `<class 'float'>`
- `neg_risk` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

**Description:**

Split USDC into two complementary positions.

---

#### `split_position`

**Signature:**
```python
def split_position(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)], amount: <class 'float'>, neg_risk: <class 'bool'> = True):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`
- `amount` (Required)
  - Type: `<class 'float'>`
- `neg_risk` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

**Description:**

Split USDC into two complementary positions.

---


================================================================================
## PolymarketGraphQLClient
================================================================================

Synchronous GraphQL client for Polymarket subgraphs.

### Initialization Parameters

```python
PolymarketGraphQLClient(
    endpoint_name: typing.Literal['activity_subgraph', 'fpmm_subgraph', 'open_interest_subgraph', 'orderbook_subgraph', 'pnl_subgraph', 'positions_subgraph', 'sports_oracle_subgraph', 'wallet_subgraph'],
)
```

### GraphQL

#### `query`

**Signature:**
```python
def query(query_string: <class 'str'>):
```

**Parameters:**

- `query_string` (Required)
  - Type: `<class 'str'>`

---

#### `query`

**Signature:**
```python
def query(query_string: <class 'str'>):
```

**Parameters:**

- `query_string` (Required)
  - Type: `<class 'str'>`

---


================================================================================
## PolymarketWeb3Client
================================================================================

Polymarket Web3 client for on-chain transactions (pays gas).

    Supports:
    - EOA wallets (signature_type=0)
    - Poly proxy wallets (signature_type=1)
    - Safe/Gnosis wallets (signature_type=2)

### Initialization Parameters

```python
PolymarketWeb3Client(
    private_key: <class 'str'>,
    signature_type: typing.Literal[0, 1, 2] = 1,
    chain_id: typing.Literal[137, 80002] = 137,
)
```

### General

#### `deploy_safe`

**Signature:**
```python
def deploy_safe():
```

**Description:**

Deploy a Safe wallet.

---

#### `deploy_safe`

**Signature:**
```python
def deploy_safe():
```

**Description:**

Deploy a Safe wallet.

---

#### `get_base_address`

**Signature:**
```python
def get_base_address():
```

**Description:**

Get the base EOA address.

---

#### `get_base_address`

**Signature:**
```python
def get_base_address():
```

**Description:**

Get the base EOA address.

---

#### `get_condition_id_neg_risk`

**Signature:**
```python
def get_condition_id_neg_risk(question_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]):
```

**Parameters:**

- `question_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`

**Description:**

Get condition ID for a neg risk market.
Returns a keccak256 hash of the oracle and question id.

---

#### `get_condition_id_neg_risk`

**Signature:**
```python
def get_condition_id_neg_risk(question_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]):
```

**Parameters:**

- `question_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`

**Description:**

Get condition ID for a neg risk market.
Returns a keccak256 hash of the oracle and question id.

---

#### `get_poly_proxy_address`

**Signature:**
```python
def get_poly_proxy_address(address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get the Polymarket proxy address.

---

#### `get_poly_proxy_address`

**Signature:**
```python
def get_poly_proxy_address(address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get the Polymarket proxy address.

---

#### `get_safe_proxy_address`

**Signature:**
```python
def get_safe_proxy_address(address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get the Safe proxy address.

---

#### `get_safe_proxy_address`

**Signature:**
```python
def get_safe_proxy_address(address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get the Safe proxy address.

---

#### `get_token_complement`

**Signature:**
```python
def get_token_complement(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

**Description:**

Get the complement token ID.

---

#### `get_token_complement`

**Signature:**
```python
def get_token_complement(token_id: <class 'str'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`

**Description:**

Get the complement token ID.

---

#### `set_all_approvals`

**Signature:**
```python
def set_all_approvals():
```

**Description:**

Set all necessary approvals.

---

#### `set_all_approvals`

**Signature:**
```python
def set_all_approvals():
```

**Description:**

Set all necessary approvals.

---

#### `set_collateral_approval`

**Signature:**
```python
def set_collateral_approval(spender: eth_typing.evm.ChecksumAddress):
```

**Parameters:**

- `spender` (Required)
  - Type: `eth_typing.evm.ChecksumAddress`

**Description:**

Set approval for spender on USDC.

---

#### `set_collateral_approval`

**Signature:**
```python
def set_collateral_approval(spender: eth_typing.evm.ChecksumAddress):
```

**Parameters:**

- `spender` (Required)
  - Type: `eth_typing.evm.ChecksumAddress`

**Description:**

Set approval for spender on USDC.

---

#### `set_conditional_tokens_approval`

**Signature:**
```python
def set_conditional_tokens_approval(spender: eth_typing.evm.ChecksumAddress):
```

**Parameters:**

- `spender` (Required)
  - Type: `eth_typing.evm.ChecksumAddress`

**Description:**

Set approval for spender on conditional tokens.

---

#### `set_conditional_tokens_approval`

**Signature:**
```python
def set_conditional_tokens_approval(spender: eth_typing.evm.ChecksumAddress):
```

**Parameters:**

- `spender` (Required)
  - Type: `eth_typing.evm.ChecksumAddress`

**Description:**

Set approval for spender on conditional tokens.

---

### Portfolio

#### `convert_positions`

**Signature:**
```python
def convert_positions(question_ids: list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]], amount: <class 'float'>):
```

**Parameters:**

- `question_ids` (Required)
  - Type: `list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]`
- `amount` (Required)
  - Type: `<class 'float'>`

**Description:**

Convert neg risk No positions to Yes positions and USDC.
Args:
question_ids: Array of question_ids representing positions to convert
amount: Number of shares to convert

---

#### `convert_positions`

**Signature:**
```python
def convert_positions(question_ids: list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]], amount: <class 'float'>):
```

**Parameters:**

- `question_ids` (Required)
  - Type: `list[typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]]`
- `amount` (Required)
  - Type: `<class 'float'>`

**Description:**

Convert neg risk No positions to Yes positions and USDC.
Args:
question_ids: Array of question_ids representing positions to convert
amount: Number of shares to convert

---

#### `get_pol_balance`

**Signature:**
```python
def get_pol_balance():
```

**Description:**

Get POL balance for the base address associated with the private key.

---

#### `get_pol_balance`

**Signature:**
```python
def get_pol_balance():
```

**Description:**

Get POL balance for the base address associated with the private key.

---

#### `get_token_balance`

**Signature:**
```python
def get_token_balance(token_id: <class 'str'>, address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get token balance of an address.

---

#### `get_token_balance`

**Signature:**
```python
def get_token_balance(token_id: <class 'str'>, address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get token balance of an address.

---

#### `get_usdc_balance`

**Signature:**
```python
def get_usdc_balance(address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get USDC balance of an address.
If no address is given, returns the balance of the instantiated client.

---

#### `get_usdc_balance`

**Signature:**
```python
def get_usdc_balance(address: typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]] = None):
```

**Parameters:**

- `address` (Optional)
  - Type: `typing.Optional[typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]]`
  - Default: `None`

**Description:**

Get USDC balance of an address.
If no address is given, returns the balance of the instantiated client.

---

#### `merge_position`

**Signature:**
```python
def merge_position(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)], amount: <class 'float'>, neg_risk: <class 'bool'> = True):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`
- `amount` (Required)
  - Type: `<class 'float'>`
- `neg_risk` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

**Description:**

Merge two complementary positions into USDC.

---

#### `merge_position`

**Signature:**
```python
def merge_position(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)], amount: <class 'float'>, neg_risk: <class 'bool'> = True):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`
- `amount` (Required)
  - Type: `<class 'float'>`
- `neg_risk` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

**Description:**

Merge two complementary positions into USDC.

---

#### `redeem_position`

**Signature:**
```python
def redeem_position(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)], amounts: list[float], neg_risk: <class 'bool'> = True):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`
- `amounts` (Required)
  - Type: `list[float]`
- `neg_risk` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

**Description:**

Redeem positions into USDC.
Args:
condition_id: Condition ID
amounts: List of amounts [x, y] where x is shares of first outcome,
y is shares of second outcome
neg_risk: Whether this is a neg risk market

---

#### `redeem_position`

**Signature:**
```python
def redeem_position(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)], amounts: list[float], neg_risk: <class 'bool'> = True):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`
- `amounts` (Required)
  - Type: `list[float]`
- `neg_risk` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

**Description:**

Redeem positions into USDC.
Args:
condition_id: Condition ID
amounts: List of amounts [x, y] where x is shares of first outcome,
y is shares of second outcome
neg_risk: Whether this is a neg risk market

---

#### `split_position`

**Signature:**
```python
def split_position(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)], amount: <class 'float'>, neg_risk: <class 'bool'> = True):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`
- `amount` (Required)
  - Type: `<class 'float'>`
- `neg_risk` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

**Description:**

Split USDC into two complementary positions.

---

#### `split_position`

**Signature:**
```python
def split_position(condition_id: typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)], amount: <class 'float'>, neg_risk: <class 'bool'> = True):
```

**Parameters:**

- `condition_id` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_keccak256 at 0x0000024EB35639C0>)]`
- `amount` (Required)
  - Type: `<class 'float'>`
- `neg_risk` (Optional)
  - Type: `<class 'bool'>`
  - Default: `True`

**Description:**

Split USDC into two complementary positions.

---

### Transfers

#### `transfer_token`

**Signature:**
```python
def transfer_token(token_id: <class 'str'>, recipient: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], amount: <class 'float'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `recipient` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `amount` (Required)
  - Type: `<class 'float'>`

**Description:**

Transfer conditional token to recipient.

---

#### `transfer_token`

**Signature:**
```python
def transfer_token(token_id: <class 'str'>, recipient: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], amount: <class 'float'>):
```

**Parameters:**

- `token_id` (Required)
  - Type: `<class 'str'>`
- `recipient` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `amount` (Required)
  - Type: `<class 'float'>`

**Description:**

Transfer conditional token to recipient.

---

#### `transfer_usdc`

**Signature:**
```python
def transfer_usdc(recipient: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], amount: <class 'float'>):
```

**Parameters:**

- `recipient` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `amount` (Required)
  - Type: `<class 'float'>`

**Description:**

Transfer USDC to recipient.

---

#### `transfer_usdc`

**Signature:**
```python
def transfer_usdc(recipient: typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)], amount: <class 'float'>):
```

**Parameters:**

- `recipient` (Required)
  - Type: `typing.Annotated[str, AfterValidator(func=<function validate_eth_address at 0x0000024EB35D6660>)]`
- `amount` (Required)
  - Type: `<class 'float'>`

**Description:**

Transfer USDC to recipient.

---


================================================================================
## PolymarketWebsocketsClient
================================================================================

### Market Data

#### `market_socket`

**Signature:**
```python
def market_socket(token_ids: list[str], process_event: <class 'collections.abc.Callable'> = <function _process_market_event at 0x0000024EB5B977E0>):
```

**Parameters:**

- `token_ids` (Required)
  - Type: `list[str]`
- `process_event` (Optional)
  - Type: `<class 'collections.abc.Callable'>`
  - Default: `<function _process_market_event at 0x0000024EB5B977E0>`

**Description:**

Connect to the market websocket and subscribe to market events for specific token IDs.
Args:
token_ids: List of token IDs to subscribe to
process_event: Callback function to process received events

---

#### `market_socket`

**Signature:**
```python
def market_socket(token_ids: list[str], process_event: <class 'collections.abc.Callable'> = <function _process_market_event at 0x0000024EB5B977E0>):
```

**Parameters:**

- `token_ids` (Required)
  - Type: `list[str]`
- `process_event` (Optional)
  - Type: `<class 'collections.abc.Callable'>`
  - Default: `<function _process_market_event at 0x0000024EB5B977E0>`

**Description:**

Connect to the market websocket and subscribe to market events for specific token IDs.
Args:
token_ids: List of token IDs to subscribe to
process_event: Callback function to process received events

---

### WebSocket

#### `live_data_socket`

**Signature:**
```python
def live_data_socket(subscriptions: list[dict[str, typing.Any]], process_event: <class 'collections.abc.Callable'> = <function _process_live_data_event at 0x0000024EB5BB7100>, creds: typing.Optional[polymarket_apis.types.clob_types.ApiCreds] = None):
```

**Parameters:**

- `subscriptions` (Required)
  - Type: `list[dict[str, typing.Any]]`
- `process_event` (Optional)
  - Type: `<class 'collections.abc.Callable'>`
  - Default: `<function _process_live_data_event at 0x0000024EB5BB7100>`
- `creds` (Optional)
  - Type: `typing.Optional[polymarket_apis.types.clob_types.ApiCreds]`
  - Default: `None`

**Description:**

Connect to the live data websocket and subscribe to specified events.
Args:
subscriptions: List of subscription configurations
process_event: Callback function to process received events
creds: ApiCreds for authentication if subscribing to clob_user topic

---

#### `live_data_socket`

**Signature:**
```python
def live_data_socket(subscriptions: list[dict[str, typing.Any]], process_event: <class 'collections.abc.Callable'> = <function _process_live_data_event at 0x0000024EB5BB7100>, creds: typing.Optional[polymarket_apis.types.clob_types.ApiCreds] = None):
```

**Parameters:**

- `subscriptions` (Required)
  - Type: `list[dict[str, typing.Any]]`
- `process_event` (Optional)
  - Type: `<class 'collections.abc.Callable'>`
  - Default: `<function _process_live_data_event at 0x0000024EB5BB7100>`
- `creds` (Optional)
  - Type: `typing.Optional[polymarket_apis.types.clob_types.ApiCreds]`
  - Default: `None`

**Description:**

Connect to the live data websocket and subscribe to specified events.
Args:
subscriptions: List of subscription configurations
process_event: Callback function to process received events
creds: ApiCreds for authentication if subscribing to clob_user topic

---

#### `user_socket`

**Signature:**
```python
def user_socket(creds: <class 'polymarket_apis.types.clob_types.ApiCreds'>, process_event: <class 'collections.abc.Callable'> = <function _process_user_event at 0x0000024EB5BB6FC0>):
```

**Parameters:**

- `creds` (Required)
  - Type: `<class 'polymarket_apis.types.clob_types.ApiCreds'>`
- `process_event` (Optional)
  - Type: `<class 'collections.abc.Callable'>`
  - Default: `<function _process_user_event at 0x0000024EB5BB6FC0>`

**Description:**

Connect to the user websocket and subscribe to user events.
Args:
creds: API credentials for authentication
process_event: Callback function to process received events

---

#### `user_socket`

**Signature:**
```python
def user_socket(creds: <class 'polymarket_apis.types.clob_types.ApiCreds'>, process_event: <class 'collections.abc.Callable'> = <function _process_user_event at 0x0000024EB5BB6FC0>):
```

**Parameters:**

- `creds` (Required)
  - Type: `<class 'polymarket_apis.types.clob_types.ApiCreds'>`
- `process_event` (Optional)
  - Type: `<class 'collections.abc.Callable'>`
  - Default: `<function _process_user_event at 0x0000024EB5BB6FC0>`

**Description:**

Connect to the user websocket and subscribe to user events.
Args:
creds: API credentials for authentication
process_event: Callback function to process received events

---


================================================================================
Package Module Structure
================================================================================

## Module Contents

### Class: `ApiCreds`
  **Methods:**
    - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
    - `from_orm(obj: 'Any') -> 'Self'`
    - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - Creates a new instance of the `Model` class with validated data.
    - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
      - Generates a JSON schema for a model class.
    - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
      - Compute the class name for parametrizations of generic classes.
    - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
      - Try to rebuild the pydantic-core schema for the model.
    - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
      - Validate a pydantic model instance.
    - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
      - !!! abstract "Usage Documentation"
    - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
      - Validate the given object with string data against the Pydantic model.
    - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
    - `parse_obj(obj: 'Any') -> 'Self'`
    - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
    - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
    - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
    - `update_forward_refs(**localns: 'Any') -> 'None'`
    - `validate(value: 'Any') -> 'Self'`

### Class: `AsyncPolymarketGraphQLClient`
  *Asynchronous GraphQL client for Polymarket subgraphs.*

### Class: `MarketOrderArgs`
  **Methods:**
    - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
    - `from_orm(obj: 'Any') -> 'Self'`
    - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - Creates a new instance of the `Model` class with validated data.
    - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
      - Generates a JSON schema for a model class.
    - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
      - Compute the class name for parametrizations of generic classes.
    - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
      - Try to rebuild the pydantic-core schema for the model.
    - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
      - Validate a pydantic model instance.
    - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
      - !!! abstract "Usage Documentation"
    - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
      - Validate the given object with string data against the Pydantic model.
    - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
    - `parse_obj(obj: 'Any') -> 'Self'`
    - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
    - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
    - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
    - `update_forward_refs(**localns: 'Any') -> 'None'`
    - `validate(value: 'Any') -> 'Self'`

### Class: `OrderArgs`
  **Methods:**
    - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
    - `from_orm(obj: 'Any') -> 'Self'`
    - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - Creates a new instance of the `Model` class with validated data.
    - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
      - Generates a JSON schema for a model class.
    - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
      - Compute the class name for parametrizations of generic classes.
    - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
      - Try to rebuild the pydantic-core schema for the model.
    - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
      - Validate a pydantic model instance.
    - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
      - !!! abstract "Usage Documentation"
    - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
      - Validate the given object with string data against the Pydantic model.
    - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
    - `parse_obj(obj: 'Any') -> 'Self'`
    - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
    - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
    - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
    - `update_forward_refs(**localns: 'Any') -> 'None'`
    - `validate(value: 'Any') -> 'Self'`

### Class: `OrderType`

### Class: `PolymarketClobClient`

### Class: `PolymarketDataClient`

### Class: `PolymarketGammaClient`

### Class: `PolymarketGaslessWeb3Client`
  *Polymarket Web3 client for gasless transactions via relay.*

### Class: `PolymarketGraphQLClient`
  *Synchronous GraphQL client for Polymarket subgraphs.*

### Class: `PolymarketWeb3Client`
  *Polymarket Web3 client for on-chain transactions (pays gas).*

### Class: `PolymarketWebsocketsClient`


## Submodules

### clients
  ### Class: `AsyncPolymarketGraphQLClient`
    *Asynchronous GraphQL client for Polymarket subgraphs.*

  ### Class: `PolymarketClobClient`

  ### Class: `PolymarketDataClient`

  ### Class: `PolymarketGammaClient`

  ### Class: `PolymarketGaslessWeb3Client`
    *Polymarket Web3 client for gasless transactions via relay.*

  ### Class: `PolymarketGraphQLClient`
    *Synchronous GraphQL client for Polymarket subgraphs.*

  ### Class: `PolymarketWeb3Client`
    *Polymarket Web3 client for on-chain transactions (pays gas).*

  ### Class: `PolymarketWebsocketsClient`

### types
  ### Class: `Activity`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `ActivityOrderMatchEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `ActivityTradeEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `ApiCreds`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `AssetType`

  ### Class: `BidAsk`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `BookParams`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `ClobMarket`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`
      - `validate_condition_fields(value: str, handler: pydantic_core.core_schema.ValidatorFunctionWrapHandler, info: pydantic_core.core_schema.ValidationInfo) -> str`
      - `validate_neg_risk_fields(value: str, handler: pydantic_core.core_schema.ValidatorFunctionWrapHandler, info: pydantic_core.core_schema.ValidationInfo) -> str | None`

  ### Class: `ClobReward`
    *Reward model.*
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `CommentEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `ContractConfig`
    *Contract Configuration.*
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `CreateOrderOptions`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `CryptoPriceSubscribeEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `CryptoPriceUpdateEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `DailyEarnedReward`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `ErrorEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `Event`
    *Event model.*
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `GammaMarket`
    *Market model.*
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`
      - `validate_condition_id(value: 'str', handler: 'ValidatorFunctionWrapHandler', info: 'ValidationInfo') -> 'str'`

  ### Class: `Holder`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `HolderResponse`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `LastTradePriceEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `LiveDataLastTradePriceEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `LiveDataOrderBookSummaryEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `LiveDataOrderEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `LiveDataPriceChangeEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `LiveDataTickSizeChangeEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `LiveDataTradeEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `MarketOrderArgs`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `MarketRewards`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `MarketStatusChangeEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `Midpoint`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `OpenOrder`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `OrderArgs`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `OrderBookSummary`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `OrderBookSummaryEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `OrderCancelResponse`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `OrderEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`
      - `validate_expiration(v)`

  ### Class: `OrderPostResponse`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `OrderType`

  ### Class: `PaginatedResponse`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `Pagination`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `PartialCreateOrderOptions`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `PolygonTrade`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `Position`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `handle_empty_end_date(v)`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `PostOrdersArgs`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `Price`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `PriceChangeEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `PriceHistory`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `QuoteEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `ReactionEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `RequestEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `RewardMarket`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `Series`
    *Series model.*
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `Spread`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `Tag`
    *Tag model.*
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `TickSizeChangeEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `TimeseriesPoint`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `Token`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `TokenBidAsk`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `TokenBidAskDict`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(root: 'RootModelRootType', _fields_set: 'set[str] | None' = None) -> 'Self'`
        - Create a new model using the provided root object and update fields set.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `TokenValue`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `TokenValueDict`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(root: 'RootModelRootType', _fields_set: 'set[str] | None' = None) -> 'Self'`
        - Create a new model using the provided root object and update fields set.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `Trade`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `TradeEvent`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `User`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `UserMetric`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `UserRank`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

  ### Class: `ValueResponse`
    **Methods:**
      - `construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
      - `from_orm(obj: 'Any') -> 'Self'`
      - `model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'`
        - Creates a new instance of the `Model` class with validated data.
      - `model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation', *, union_format: "Literal['any_of', 'primitive_type_array']" = 'any_of') -> 'dict[str, Any]'`
        - Generates a JSON schema for a model class.
      - `model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'`
        - Compute the class name for parametrizations of generic classes.
      - `model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'MappingNamespace | None' = None) -> 'bool | None'`
        - Try to rebuild the pydantic-core schema for the model.
      - `model_validate(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate a pydantic model instance.
      - `model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - !!! abstract "Usage Documentation"
      - `model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, extra: 'ExtraValues | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, by_name: 'bool | None' = None) -> 'Self'`
        - Validate the given object with string data against the Pydantic model.
      - `parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `parse_obj(obj: 'Any') -> 'Self'`
      - `parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'`
      - `schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'`
      - `schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'`
      - `update_forward_refs(**localns: 'Any') -> 'None'`
      - `validate(value: 'Any') -> 'Self'`

### utilities

================================================================================
Summary
================================================================================

This reference was generated by exploring the installed `polymarket-apis` package.
For the most up-to-date information, refer to:
- PyPI: https://pypi.org/project/polymarket-apis/
- Package documentation (if available)
