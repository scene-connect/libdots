#  This work is based on original code developed and copyrighted by TNO 2023
#  and further developed and copyrighted by Scene Ltd in 2025.
#  Subsequent contributions are licensed to you by the developers of such code and are
#  made available under one or several contributor license agreements.
#
#  This work is licensed to you under the Apache License, Version 2.0.
#  You may obtain a copy of the license at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#      TNO         - Initial implementation of the dots calculation-service-generator
#      Scene Ltd   - Development of libdots
#  Manager:
#      Scene Ltd
from collections.abc import Mapping
from collections.abc import Sequence
from typing import Any
from typing import TypeAlias
from typing import TypedDict
from typing import override
from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr
from pytest_mock import MockerFixture

from libdots.io.io_data import IODataInterface
from libdots.io.io_data import NewStep
from libdots.model import service_calc
from libdots.model.config import ServiceConfig
from libdots.model.esdl_parser import ESDLParser
from libdots.model.service_calc import CalculationFunction
from libdots.model.service_calc import ServiceCalc
from libdots.types import EsdlId
from libdots.types import ESDLObject
from libdots.types import ServiceName


class OutputMessage(IODataInterface):
    """An example service, input_data and messages."""

    def __init__(self, load: float):
        self.load = load

    @classmethod
    @override
    def get_name(cls) -> str:
        return "test_output"

    @override
    def get_values_as_serialized_protobuf(self) -> bytes:
        return b""

    @override
    def set_values_from_serialized_protobuf(self, serialized_message: bytes):
        pass

    @classmethod
    @override
    def get_main_topic(cls) -> str:
        return "test_output"

    @classmethod
    @override
    def get_variable_descr(cls) -> str:
        return "Some test data"

    def __eq__(self, other: Any):
        return isinstance(other, OutputMessage) and other.load == self.load


class InputMessage(OutputMessage):
    def __init__(self, demand: float):
        self.demand = demand

    @classmethod
    @override
    def get_name(cls) -> str:
        return "test_input"


class InputData(TypedDict):
    test_input_list: Sequence[InputMessage]


OutputData: TypeAlias = tuple[Mapping[EsdlId, OutputMessage]]


class MyServiceCalc(ServiceCalc[CalculationFunction[InputData, OutputData]]):
    base_setup_called: bool

    @property
    @override
    def service_name(self) -> ServiceName:
        return "my_service"

    @override
    def base_setup(self):
        self.base_setup_called = True
        pass

    @property
    def calculation_functions(
        self,
    ) -> Mapping[str, CalculationFunction[InputData, OutputData]]:
        return {"calc": self.test_calc}

    def test_calc(self, new_step: NewStep, input_data: InputData) -> OutputData:
        esdl_id: EsdlId = "1234"
        list_demand = [item.demand for item in input_data["test_input_list"]]
        output_data = OutputMessage(load=sum(list_demand))
        return ({esdl_id: output_data},)

    @property
    def receives_service_names(self) -> list[ServiceName]:
        return ["input_service"]

    def process_esdl_object(self, esdl_id: EsdlId, esdl_object: ESDLObject):
        pass


@pytest.fixture
def mock_esdl_parser(mocker: MockerFixture):
    mock_esdl_parser = MagicMock(spec=ESDLParser)
    mock_esdl_parser_class = mocker.patch.object(
        service_calc.ESDLParser,
        "__new__",
        return_value=mock_esdl_parser,
    )
    return mock_esdl_parser_class


@pytest.fixture(name="service_calc")
def service_calc_fixture() -> MyServiceCalc:
    svc = MyServiceCalc(
        simulation_id="",
        model_id="",
        influxdb_host="",
        influxdb_port=1,
        influxdb_password="",
        influxdb_user="",
        influxdb_name="",
    )
    return svc


@pytest.fixture
def config() -> ServiceConfig:
    return ServiceConfig(
        simulation_id="1234",
        model_id="1234",
        influxdb_host="",
        influxdb_port=4321,
        influxdb_user="",
        influxdb_name="",
        influxdb_password=SecretStr(""),
        mqtt_qos=0,
        mqtt_host="localhost",
        mqtt_port=1234,
        mqtt_username="",
        mqtt_password=SecretStr(""),
    )
