import logging
from abc import ABC
from abc import abstractmethod
from typing import Any

from dots_utilities.io.input_data_inventory import InputDataInventory
from dots_utilities.io.mqtt_client import MqttClient
from dots_utilities.io.mqtt_log_handler import MqttLogHandler
from dots_utilities.model.service_calc import CalculationFunction
from dots_utilities.model.service_calc import ServiceCalc


class Service(ABC):
    def __init__(self, config: dict[str, Any]):
        # initialize input data container and service calc
        service_calc = self.service_calc_class(
            simulation_id=config["SIMULATION_ID"],
            model_id=config["MODEL_ID"],
            influxdb_host=config["INFLUXDB_HOST"],
            influxdb_port=config["INFLUXDB_PORT"],
            influxdb_user=config["INFLUXDB_USER"],
            influxdb_password=config["INFLUXDB_PASSWORD"],
            influxdb_name=config["INFLUXDB_NAME"],
        )
        self.logger = logging.getLogger()
        mqtt_handler = MqttLogHandler(self.mqtt_client)
        self.logger.addHandler(mqtt_handler)

        input_data_inventory = InputDataInventory(
            service_calc.calculation_function_input_types, service_calc.service_name
        )

        # initialize mqtt client
        self.mqtt_client = MqttClient(
            host=config["MQTT_HOST"],
            port=config["MQTT_PORT"],
            qos=config["MQTT_QOS"],
            username=config["MQTT_USERNAME"],
            password=config["MQTT_PASSWORD"],
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
