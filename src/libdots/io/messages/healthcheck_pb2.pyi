from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class HealthStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HEALTHY: _ClassVar[HealthStatus]
    UNHEALTHY: _ClassVar[HealthStatus]

HEALTHY: HealthStatus
UNHEALTHY: HealthStatus

class PingHealthSOToMSO(_message.Message):
    __slots__ = ("healthy", "reasons", "activeSimulations")
    HEALTHY_FIELD_NUMBER: _ClassVar[int]
    REASONS_FIELD_NUMBER: _ClassVar[int]
    ACTIVESIMULATIONS_FIELD_NUMBER: _ClassVar[int]
    healthy: HealthStatus
    reasons: _containers.RepeatedScalarFieldContainer[str]
    activeSimulations: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        healthy: _Optional[_Union[HealthStatus, str]] = ...,
        reasons: _Optional[_Iterable[str]] = ...,
        activeSimulations: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class PongHealthMSOToSO(_message.Message):
    __slots__ = ("healthy", "reasons")
    HEALTHY_FIELD_NUMBER: _ClassVar[int]
    REASONS_FIELD_NUMBER: _ClassVar[int]
    healthy: HealthStatus
    reasons: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        healthy: _Optional[_Union[HealthStatus, str]] = ...,
        reasons: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class PingHealthMSOToModel(_message.Message):
    __slots__ = ("healthy", "reasons")
    HEALTHY_FIELD_NUMBER: _ClassVar[int]
    REASONS_FIELD_NUMBER: _ClassVar[int]
    healthy: HealthStatus
    reasons: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        healthy: _Optional[_Union[HealthStatus, str]] = ...,
        reasons: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class PongHealthModelToMSO(_message.Message):
    __slots__ = ("healthy", "reasons", "numberOfBids", "numberOfAllocations")
    HEALTHY_FIELD_NUMBER: _ClassVar[int]
    REASONS_FIELD_NUMBER: _ClassVar[int]
    NUMBEROFBIDS_FIELD_NUMBER: _ClassVar[int]
    NUMBEROFALLOCATIONS_FIELD_NUMBER: _ClassVar[int]
    healthy: HealthStatus
    reasons: _containers.RepeatedScalarFieldContainer[str]
    numberOfBids: int
    numberOfAllocations: int
    def __init__(
        self,
        healthy: _Optional[_Union[HealthStatus, str]] = ...,
        reasons: _Optional[_Iterable[str]] = ...,
        numberOfBids: _Optional[int] = ...,
        numberOfAllocations: _Optional[int] = ...,
    ) -> None: ...
