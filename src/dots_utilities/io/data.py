from abc import ABC
from abc import abstractmethod


class IODataInterface(ABC):
    def set_values_from_serialized_protobuf(self, serialized_message: bytes):
        """Set values from protobuf message"""
        pass

    @abstractmethod
    def get_values_as_serialized_protobuf(self) -> bytes:
        """Get dictionary with all variables"""
        pass

    @abstractmethod
    @classmethod
    def get_name(cls) -> str:
        """Get data name"""
        pass

    @abstractmethod
    @classmethod
    def get_main_topic(cls) -> str:
        """Get MQTT topic"""
        pass

    @abstractmethod
    @classmethod
    def get_variable_descr(cls) -> str:
        """ "Get variables description"""
        pass
