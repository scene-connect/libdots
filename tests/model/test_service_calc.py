from datetime import datetime
from datetime import timezone as tz
from typing import Annotated
from unittest.mock import MagicMock

from esdl import EnergyDemand
from esdl import EnergySystem
from pytest_mock import MockerFixture

from libdots.io.io_data import NewStep
from libdots.model.esdl_parser import ESDLParser
from libdots.types import CalculationServiceDescription
from libdots.types import EsdlId
from libdots.types import ModelParametersDescription
from tests.conftest import InputMessage
from tests.conftest import MyServiceCalc
from tests.conftest import OutputMessage


def test_calculation_function_input_types(
    service_calc: MyServiceCalc,
):
    assert service_calc.calculation_function_input_types == {
        "calc": [NewStep, InputMessage]
    }


def test_calculation_function(service_calc: MyServiceCalc):
    input_messages = [InputMessage(demand=10), InputMessage(demand=12)]
    input_data_dict = {"new_step": NewStep(), "test_input_list": input_messages}
    result = service_calc.calc_function("calc", input_data_dict=input_data_dict)
    assert result == ({"1234": OutputMessage(load=22)},)


def test_setup(
    mock_esdl_parser: Annotated[MagicMock, type[ESDLParser]],
    mocker: MockerFixture,
    service_calc: MyServiceCalc,
):
    energy_system = EnergySystem()
    energy_demand = EnergyDemand()
    esdl_id: EsdlId = "1234"
    service_calc.esdl_parser = mock_esdl_parser
    mock_get_energy_system = mock_esdl_parser.return_value.get_energy_system
    mock_get_energy_system.return_value = energy_system
    mock_get_model_esdl_object = mock_esdl_parser.return_value.get_model_esdl_object
    mock_get_model_esdl_object.return_value = energy_demand
    now = datetime.now(tz.utc)
    calculation_service: CalculationServiceDescription = {
        "esdl_type": "EnergyDemand",
        "calc_service_name": "my_service",
        "service_image_url": "foo",
    }
    model_parameters: ModelParametersDescription = {
        "esdl_ids": [esdl_id],
        "simulation_name": "testsimulation",
        "start_timestamp": now.timestamp(),
        "time_step_seconds": 60,
        "nr_of_time_steps": 1,
        "calculation_services": [calculation_service],
        "esdl_base64string": "",
    }
    process_esdl_object_spy = mocker.spy(service_calc, "process_esdl_object")

    # call setup
    service_calc.setup(model_parameters)

    assert service_calc.service_name == "my_service"
    assert service_calc.base_setup_called

    # check the esdl_parser was instantiated correctly (we mocked __new__)
    mock_esdl_parser.assert_called_once_with(
        ESDLParser, service_calc.receives_service_names
    )

    mock_get_energy_system.assert_called_once_with(
        model_parameters["esdl_base64string"]
    )
    mock_get_model_esdl_object.assert_called_once_with(esdl_id, energy_system)
    process_esdl_object_spy.assert_called_once_with(esdl_id, energy_demand)
