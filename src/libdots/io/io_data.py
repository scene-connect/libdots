import json
from abc import ABC
from abc import abstractmethod
from typing import override

from libdots.types import ModelParametersDescription
from libdots.types import TimeStepDescription

from .messages import lifecycle_pb2


class IODataInterface(ABC):

    @abstractmethod
    def set_values_from_serialized_protobuf(self, serialized_message: bytes):
        """Set values from protobuf message"""
        pass

    @abstractmethod
    def get_values_as_serialized_protobuf(self) -> bytes:
        """Get dictionary with all variables"""
        pass

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """Get data name"""
        pass

    @classmethod
    @abstractmethod
    def get_main_topic(cls) -> str:
        """Get MQTT topic"""
        pass

    @classmethod
    @abstractmethod
    def get_variable_descr(cls) -> str:
        """ "Get variables description"""
        pass


class ModelParameters(IODataInterface):
    parameters_dict: ModelParametersDescription

    @override
    def set_values_from_serialized_protobuf(self, serialized_message: bytes):
        config_data = lifecycle_pb2.ModelParameters()
        config_data.ParseFromString(serialized_message)
        self.parameters_dict = json.loads(config_data.parameters_dict)

    @override
    def get_values_as_serialized_protobuf(self) -> bytes:
        protobuf_message = lifecycle_pb2.ModelParameters()
        protobuf_message.parameters_dict = json.dumps(self.parameters_dict)
        return protobuf_message.SerializeToString()

    @classmethod
    @override
    def get_name(cls) -> str:
        return "model_parameters"

    @classmethod
    @override
    def get_main_topic(cls) -> str:
        return "/lifecycle/dots-so/model"

    @classmethod
    @override
    def get_variable_descr(cls) -> str:
        return "{parameters_dict': 'dict'}"


class NewStep(IODataInterface):
    parameters_dict: TimeStepDescription

    @override
    def set_values_from_serialized_protobuf(self, serialized_message: bytes):
        config_data = lifecycle_pb2.NewStep()
        config_data.ParseFromString(serialized_message)
        self.parameters_dict = json.loads(config_data.parameters_dict)

    @override
    def get_values_as_serialized_protobuf(self) -> bytes:
        protobuf_message = lifecycle_pb2.NewStep()
        protobuf_message.parameters_dict = json.dumps(self.parameters_dict)
        return protobuf_message.SerializeToString()

    @classmethod
    @override
    def get_name(cls) -> str:
        return "new_step"

    @classmethod
    @override
    def get_main_topic(cls) -> str:
        return "/lifecycle/dots-so/model"

    @classmethod
    @override
    def get_variable_descr(cls) -> str:
        return "{'parameters_dict': 'dict'}"
