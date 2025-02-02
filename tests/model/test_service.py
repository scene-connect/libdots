from typing import override
from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from libdots.model import service as lib_service
from libdots.model.config import ServiceConfig
from tests.conftest import MyServiceCalc


def test_service_init(mocker: MockerFixture, config: ServiceConfig):
    mock_service_calc = MagicMock()
    mock_service_calc.service_name = "test_service"
    mock_service_calc.calculation_function_input_types = ["foo"]
    mock_service_calc_class = MagicMock(return_value=mock_service_calc)

    class MyService(lib_service.BaseService):
        @property
        @override
        def service_calc_class(self) -> type[MyServiceCalc]:
            return mock_service_calc_class  # pyright:ignore[reportReturnType]

    mock_mqtt_client = MagicMock()
    mock_mqtt_client_class = mocker.patch.object(
        lib_service, "MqttClient", return_value=mock_mqtt_client
    )
    mock_input_data_inventory_class = mocker.patch.object(
        lib_service, "InputDataInventory", return_value=MagicMock()
    )

    service = MyService(config)
    mock_input_data_inventory_class.assert_called_once_with(
        mock_service_calc.calculation_function_input_types,
        mock_service_calc.service_name,
    )
    mock_mqtt_client_class.assert_called_once_with(
        host=config.mqtt_host,
        port=config.mqtt_port,
        qos=config.mqtt_qos,
        username=config.mqtt_username,
        password=config.mqtt_password.get_secret_value(),
        input_data_inventory=service.input_data_inventory,
        service_calc=mock_service_calc,
        service_name=mock_service_calc.service_name,
        sim_logger=service.logger,
    )
