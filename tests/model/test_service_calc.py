from collections.abc import Mapping
from collections.abc import Sequence
from typing import TypeAlias
from typing import TypedDict

from dots_utilities.io.io_data import IODataInterface
from dots_utilities.io.io_data import NewStep
from dots_utilities.model.service_calc import CalculationFunction
from dots_utilities.model.service_calc import ServiceCalc
from dots_utilities.types import EsdlId
from dots_utilities.types import ESDLObject
from dots_utilities.types import ServiceName


class OutputMessage(IODataInterface):

    def __init__(self, load: float):
        self.load = load

    @classmethod
    def get_name(cls):
        return "TestOutput"

    def get_values_as_serialized_protobuf(self) -> bytes:
        return b""

    def set_values_from_serialized_protobuf(self, serialized_message: bytes):
        pass

    @classmethod
    def get_main_topic(cls) -> str:
        return "test_output"

    @classmethod
    def get_variable_descr(cls) -> str:
        return "Some test data"


class InputMessage(OutputMessage):
    def __init__(self, demand: float):
        self.demand = demand


class InputData(TypedDict):
    list_test_input: Sequence[InputMessage]


OutputData: TypeAlias = tuple[Mapping[EsdlId, OutputMessage]]


class MyServiceCalc(ServiceCalc[CalculationFunction[InputData, OutputData]]):
    @property
    def calculation_functions(
        self,
    ) -> Mapping[str, CalculationFunction[InputData, OutputData]]:
        return {"calc": self.test_calc}

    def test_calc(self, new_step: NewStep, input_data: InputData) -> OutputData:
        esdl_id: EsdlId = "1234"
        output_data = OutputMessage(load=10)
        return ({esdl_id: output_data},)

    @property
    def receives_service_names(self) -> list[ServiceName]:
        return ["input_service"]

    def process_esdl_object(self, esdl_id: EsdlId, esdl_object: ESDLObject):
        pass


def test_calculation_function_input_types():
    svc = MyServiceCalc(
        simulation_id="",
        model_id="",
        influxdb_host="",
        influxdb_port=1,
        influxdb_password="",
        influxdb_user="",
        influxdb_name="",
    )
    assert svc.calculation_function_input_types == {"calc": [InputMessage]}
