import logging

from pytest_mock import MockerFixture

from libdots.io.input_data_inventory import InputDataInventory
from libdots.io.io_data import NewStep
from libdots.io.mqtt_client import MqttClient
from libdots.types import EsdlId
from tests.conftest import InputMessage
from tests.conftest import MyServiceCalc
from tests.conftest import OutputMessage


def test_do_step(mocker: MockerFixture, service_calc: MyServiceCalc):

    input_message = InputMessage(demand=10)
    output_message = OutputMessage(load=10)
    esdl_id: EsdlId = "1234"
    output_data = ({esdl_id: output_message},)
    new_step = NewStep()
    expected_input_data = {
        "new_step": new_step,
        f"{InputMessage.get_name()}_list": [input_message],
    }

    # mock the calculation function
    calculation_name = "calc"
    mock_calc_function = mocker.patch.object(
        service_calc, "calc_function", return_value=output_data
    )

    # setup the inventory
    # we're sneakily also testing its get_input_data method here
    # by setting the received data (input_data_dict) here
    inventory = InputDataInventory(
        service_calc.calculation_function_input_types, service_calc.service_name
    )
    spy_get_input_data = mocker.spy(inventory, "get_input_data")
    inventory.input_data_dict = {
        NewStep.get_name(): [new_step],
        InputMessage.get_name(): [input_message],
    }
    mock_set_calc_done = mocker.patch.object(inventory, "set_calc_done")

    sim_logger = logging.getLogger()
    mqtt_client = MqttClient(
        host="",
        port=123,
        qos=1,
        username="",
        password="",
        service_name="",
        input_data_inventory=inventory,
        service_calc=service_calc,
        sim_logger=sim_logger,
    )
    mock_send_io_data = mocker.patch.object(mqtt_client, "_send_io_data")

    mqtt_client._do_step(calculation_name)  # pyright:ignore[reportPrivateUsage]
    mock_calc_function.assert_called_once_with(calculation_name, expected_input_data)
    spy_get_input_data.assert_called_once_with(calculation_name)

    mock_send_io_data.assert_called_once_with(esdl_id, output_data[0][esdl_id])
    mock_set_calc_done.assert_called_once_with(calculation_name)
