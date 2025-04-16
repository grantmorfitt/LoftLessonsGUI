from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BooleanOldNew(_message.Message):
    __slots__ = ["new_value", "old_value"]
    NEW_VALUE_FIELD_NUMBER: _ClassVar[int]
    OLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    new_value: bool
    old_value: bool
    def __init__(self, old_value: bool = ..., new_value: bool = ...) -> None: ...

class Double2(_message.Message):
    __slots__ = ["value_0", "value_1"]
    VALUE_0_FIELD_NUMBER: _ClassVar[int]
    VALUE_1_FIELD_NUMBER: _ClassVar[int]
    value_0: float
    value_1: float
    def __init__(self, value_0: _Optional[float] = ..., value_1: _Optional[float] = ...) -> None: ...

class Double2OldNew(_message.Message):
    __slots__ = ["new_value", "old_value"]
    NEW_VALUE_FIELD_NUMBER: _ClassVar[int]
    OLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    new_value: Double2
    old_value: Double2
    def __init__(self, old_value: _Optional[_Union[Double2, _Mapping]] = ..., new_value: _Optional[_Union[Double2, _Mapping]] = ...) -> None: ...

class Double3(_message.Message):
    __slots__ = ["value_0", "value_1", "value_2"]
    VALUE_0_FIELD_NUMBER: _ClassVar[int]
    VALUE_1_FIELD_NUMBER: _ClassVar[int]
    VALUE_2_FIELD_NUMBER: _ClassVar[int]
    value_0: float
    value_1: float
    value_2: float
    def __init__(self, value_0: _Optional[float] = ..., value_1: _Optional[float] = ..., value_2: _Optional[float] = ...) -> None: ...

class Double3OldNew(_message.Message):
    __slots__ = ["new_value", "old_value"]
    NEW_VALUE_FIELD_NUMBER: _ClassVar[int]
    OLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    new_value: Double3
    old_value: Double3
    def __init__(self, old_value: _Optional[_Union[Double3, _Mapping]] = ..., new_value: _Optional[_Union[Double3, _Mapping]] = ...) -> None: ...

class Double4(_message.Message):
    __slots__ = ["value_0", "value_1", "value_2", "value_3"]
    VALUE_0_FIELD_NUMBER: _ClassVar[int]
    VALUE_1_FIELD_NUMBER: _ClassVar[int]
    VALUE_2_FIELD_NUMBER: _ClassVar[int]
    VALUE_3_FIELD_NUMBER: _ClassVar[int]
    value_0: float
    value_1: float
    value_2: float
    value_3: float
    def __init__(self, value_0: _Optional[float] = ..., value_1: _Optional[float] = ..., value_2: _Optional[float] = ..., value_3: _Optional[float] = ...) -> None: ...

class Double4OldNew(_message.Message):
    __slots__ = ["new_value", "old_value"]
    NEW_VALUE_FIELD_NUMBER: _ClassVar[int]
    OLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    new_value: Double4
    old_value: Double4
    def __init__(self, old_value: _Optional[_Union[Double4, _Mapping]] = ..., new_value: _Optional[_Union[Double4, _Mapping]] = ...) -> None: ...

class Double5(_message.Message):
    __slots__ = ["value_0", "value_1", "value_2", "value_3", "value_4"]
    VALUE_0_FIELD_NUMBER: _ClassVar[int]
    VALUE_1_FIELD_NUMBER: _ClassVar[int]
    VALUE_2_FIELD_NUMBER: _ClassVar[int]
    VALUE_3_FIELD_NUMBER: _ClassVar[int]
    VALUE_4_FIELD_NUMBER: _ClassVar[int]
    value_0: float
    value_1: float
    value_2: float
    value_3: float
    value_4: float
    def __init__(self, value_0: _Optional[float] = ..., value_1: _Optional[float] = ..., value_2: _Optional[float] = ..., value_3: _Optional[float] = ..., value_4: _Optional[float] = ...) -> None: ...

class Double5OldNew(_message.Message):
    __slots__ = ["new_value", "old_value"]
    NEW_VALUE_FIELD_NUMBER: _ClassVar[int]
    OLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    new_value: Double5
    old_value: Double5
    def __init__(self, old_value: _Optional[_Union[Double5, _Mapping]] = ..., new_value: _Optional[_Union[Double5, _Mapping]] = ...) -> None: ...

class DoubleOldNew(_message.Message):
    __slots__ = ["new_value", "old_value"]
    NEW_VALUE_FIELD_NUMBER: _ClassVar[int]
    OLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    new_value: float
    old_value: float
    def __init__(self, old_value: _Optional[float] = ..., new_value: _Optional[float] = ...) -> None: ...

class Int32OldNew(_message.Message):
    __slots__ = ["new_value", "old_value"]
    NEW_VALUE_FIELD_NUMBER: _ClassVar[int]
    OLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    new_value: int
    old_value: int
    def __init__(self, old_value: _Optional[int] = ..., new_value: _Optional[int] = ...) -> None: ...

class ReadStatesRequest(_message.Message):
    __slots__ = ["state_ids", "updated_later_than"]
    STATE_IDS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_LATER_THAN_FIELD_NUMBER: _ClassVar[int]
    state_ids: _containers.RepeatedScalarFieldContainer[int]
    updated_later_than: int
    def __init__(self, state_ids: _Optional[_Iterable[int]] = ..., updated_later_than: _Optional[int] = ...) -> None: ...

class StateEvent(_message.Message):
    __slots__ = ["boolean_change", "double2_change", "double3_change", "double4_change", "double5_change", "double_change", "int32_change", "state_id", "string_change"]
    BOOLEAN_CHANGE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE2_CHANGE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE3_CHANGE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE4_CHANGE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE5_CHANGE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    INT32_CHANGE_FIELD_NUMBER: _ClassVar[int]
    STATE_ID_FIELD_NUMBER: _ClassVar[int]
    STRING_CHANGE_FIELD_NUMBER: _ClassVar[int]
    boolean_change: BooleanOldNew
    double2_change: Double2OldNew
    double3_change: Double3OldNew
    double4_change: Double4OldNew
    double5_change: Double5OldNew
    double_change: DoubleOldNew
    int32_change: Int32OldNew
    state_id: int
    string_change: StringOldNew
    def __init__(self, state_id: _Optional[int] = ..., boolean_change: _Optional[_Union[BooleanOldNew, _Mapping]] = ..., int32_change: _Optional[_Union[Int32OldNew, _Mapping]] = ..., double_change: _Optional[_Union[DoubleOldNew, _Mapping]] = ..., string_change: _Optional[_Union[StringOldNew, _Mapping]] = ..., double2_change: _Optional[_Union[Double2OldNew, _Mapping]] = ..., double3_change: _Optional[_Union[Double3OldNew, _Mapping]] = ..., double4_change: _Optional[_Union[Double4OldNew, _Mapping]] = ..., double5_change: _Optional[_Union[Double5OldNew, _Mapping]] = ...) -> None: ...

class StateStreamValues(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[StateValue]
    def __init__(self, values: _Optional[_Iterable[_Union[StateValue, _Mapping]]] = ...) -> None: ...

class StateValue(_message.Message):
    __slots__ = ["boolean_value", "double2_value", "double3_value", "double4_value", "double5_value", "double_value", "int32_value", "state_id", "string_value"]
    BOOLEAN_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE2_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE3_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE4_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE5_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    STATE_ID_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    boolean_value: bool
    double2_value: Double2
    double3_value: Double3
    double4_value: Double4
    double5_value: Double5
    double_value: float
    int32_value: int
    state_id: int
    string_value: str
    def __init__(self, state_id: _Optional[int] = ..., boolean_value: bool = ..., int32_value: _Optional[int] = ..., double_value: _Optional[float] = ..., string_value: _Optional[str] = ..., double2_value: _Optional[_Union[Double2, _Mapping]] = ..., double3_value: _Optional[_Union[Double3, _Mapping]] = ..., double4_value: _Optional[_Union[Double4, _Mapping]] = ..., double5_value: _Optional[_Union[Double5, _Mapping]] = ...) -> None: ...

class StateValues(_message.Message):
    __slots__ = ["read_time", "values"]
    READ_TIME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    read_time: int
    values: _containers.RepeatedCompositeFieldContainer[StateValue]
    def __init__(self, read_time: _Optional[int] = ..., values: _Optional[_Iterable[_Union[StateValue, _Mapping]]] = ...) -> None: ...

class StringOldNew(_message.Message):
    __slots__ = ["new_value", "old_value"]
    NEW_VALUE_FIELD_NUMBER: _ClassVar[int]
    OLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    new_value: str
    old_value: str
    def __init__(self, old_value: _Optional[str] = ..., new_value: _Optional[str] = ...) -> None: ...

class SubscribeStateChangeEventsRequest(_message.Message):
    __slots__ = ["state_ids"]
    STATE_IDS_FIELD_NUMBER: _ClassVar[int]
    state_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, state_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class SubscribeStatesRequest(_message.Message):
    __slots__ = ["minimum_notification_interval_ms", "notify_empty_change_sets", "notify_unchanged", "state_ids"]
    MINIMUM_NOTIFICATION_INTERVAL_MS_FIELD_NUMBER: _ClassVar[int]
    NOTIFY_EMPTY_CHANGE_SETS_FIELD_NUMBER: _ClassVar[int]
    NOTIFY_UNCHANGED_FIELD_NUMBER: _ClassVar[int]
    STATE_IDS_FIELD_NUMBER: _ClassVar[int]
    minimum_notification_interval_ms: int
    notify_empty_change_sets: bool
    notify_unchanged: bool
    state_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, state_ids: _Optional[_Iterable[int]] = ..., notify_empty_change_sets: bool = ..., notify_unchanged: bool = ..., minimum_notification_interval_ms: _Optional[int] = ...) -> None: ...

class WriteStatesRequest(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[StateValue]
    def __init__(self, values: _Optional[_Iterable[_Union[StateValue, _Mapping]]] = ...) -> None: ...
