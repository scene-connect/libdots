import logging
from abc import ABC
from abc import abstractmethod
from typing import Any

from dots_utilities.io.input_data_inventory import InputDataInventory
from dots_utilities.io.mqtt_client import MqttClient
from dots_utilities.io.mqtt_log_handler import MqttLogHandler
from dots_utilities.model.config import ServiceConfig
from dots_utilities.model.service_calc import CalculationFunction
from dots_utilities.model.service_calc import ServiceCalc


class BaseService(ABC):
    def __init__(self, config: ServiceConfig):
        # initialize input data container and service calc
        service_calc = self.service_calc_class(
            simulation_id=config.simulation_id,
            model_id=config.model_id,
            influxdb_host=config.influxdb_host,
            influxdb_port=config.influxdb_port,
            influxdb_user=config.influxdb_user,
            influxdb_password=config.influxdb_password.get_secret_value(),
            influxdb_name=config.influxdb_name,
        )
        self.logger = logging.getLogger()
        mqtt_handler = MqttLogHandler(self.mqtt_client)
        self.logger.addHandler(mqtt_handler)

        input_data_inventory = InputDataInventory(
            service_calc.calculation_function_input_types, service_calc.service_name
        )

        # initialize mqtt client
        self.mqtt_client = MqttClient(
            host=config.mqtt_host,
            port=config.mqtt_port,
            qos=config.mqtt_qos,
            username=config.mqtt_username,
            password=config.mqtt_password.get_secret_value(),
            input_data_inventory=input_data_inventory,
            service_calc=service_calc,
            service_name=service_calc.service_name,
            sim_logger=self.logger,
        )

    @property
    @abstractmethod
    def service_calc_class(self) -> type[ServiceCalc[CalculationFunction[Any, Any]]]:
        pass

    def start(self):
        self.mqtt_client.wait_for_data()
