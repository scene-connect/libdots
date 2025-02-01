from typing import Any as _Any
from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class UnhealthyModelStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOPROGRESS: _ClassVar[UnhealthyModelStatus]

class TerminationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUCCESSFULL: _ClassVar[TerminationStatus]
    FAILED: _ClassVar[TerminationStatus]

NOPROGRESS: UnhealthyModelStatus
SUCCESSFULL: TerminationStatus
FAILED: TerminationStatus

class EnvironmentVariable(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(
        self, name: _Optional[str] = ..., value: _Optional[str] = ...
    ) -> None: ...

class ModelConfiguration(_message.Message):
    __slots__ = ("modelID", "imageUrl", "environmentVariables")
    MODELID_FIELD_NUMBER: _ClassVar[int]
    IMAGEURL_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTVARIABLES_FIELD_NUMBER: _ClassVar[int]
    modelID: str
    imageUrl: str
    environmentVariables: _containers.RepeatedCompositeFieldContainer[
        EnvironmentVariable
    ]
    def __init__(
        self,
        modelID: _Optional[str] = ...,
        imageUrl: _Optional[str] = ...,
        environmentVariables: _Optional[
            _Iterable[_Union[EnvironmentVariable, _Mapping[str, _Any]]]
        ] = ...,
    ) -> None: ...

class DeployModels(_message.Message):
    __slots__ = ("simulatorId", "modelConfigurations", "keepLogsHours")
    SIMULATORID_FIELD_NUMBER: _ClassVar[int]
    MODELCONFIGURATIONS_FIELD_NUMBER: _ClassVar[int]
    KEEPLOGSHOURS_FIELD_NUMBER: _ClassVar[int]
    simulatorId: str
    modelConfigurations: _containers.RepeatedCompositeFieldContainer[ModelConfiguration]
    keepLogsHours: float
    def __init__(
        self,
        simulatorId: _Optional[str] = ...,
        modelConfigurations: _Optional[
            _Iterable[_Union[ModelConfiguration, _Mapping[str, _Any]]]
        ] = ...,
        keepLogsHours: _Optional[float] = ...,
    ) -> None: ...

class ReadyForProcessing(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ModelsReady(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ModelParameters(_message.Message):
    __slots__ = ("parameters_dict",)
    PARAMETERS_DICT_FIELD_NUMBER: _ClassVar[int]
    parameters_dict: str
    def __init__(self, parameters_dict: _Optional[str] = ...) -> None: ...

class Parameterized(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NewStep(_message.Message):
    __slots__ = ("parameters_dict",)
    PARAMETERS_DICT_FIELD_NUMBER: _ClassVar[int]
    parameters_dict: str
    def __init__(self, parameters_dict: _Optional[str] = ...) -> None: ...

class CalculationsDone(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ErrorOccurred(_message.Message):
    __slots__ = ("error_message",)
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    def __init__(self, error_message: _Optional[str] = ...) -> None: ...

class SimulationDone(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UnhealthyModel(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: UnhealthyModelStatus
    def __init__(
        self, status: _Optional[_Union[UnhealthyModelStatus, str]] = ...
    ) -> None: ...

class ModelHasTerminated(_message.Message):
    __slots__ = ("status", "exitCode")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXITCODE_FIELD_NUMBER: _ClassVar[int]
    status: TerminationStatus
    exitCode: int
    def __init__(
        self,
        status: _Optional[_Union[TerminationStatus, str]] = ...,
        exitCode: _Optional[int] = ...,
    ) -> None: ...

class AllModelsHaveTerminated(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
