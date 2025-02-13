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
import logging
from abc import ABC
from abc import abstractmethod
from typing import Any

from libdots.io.input_data_inventory import InputDataInventory
from libdots.io.mqtt_client import MqttClient
from libdots.io.mqtt_log_handler import MqttLogHandler
from libdots.model.config import ServiceConfig
from libdots.model.service_calc import CalculationFunction
from libdots.model.service_calc import ServiceCalc


class BaseService(ABC):
    """
    Abstract Base Class for the actual Service object.
    This object needs to be overriden and its :py:attr:`service_calc_class` property implemented.

    This can be done like this:

        .. code-block:: python

            from typing import override

            from libdots.model.config import ServiceConfig
            from libdots.model.service import BaseService
            from libdots.model.service_calc import CalculationFunction
            from libdots.model.service_calc import ServiceCalc
            from .service_cal import MyServiceCalc

            class MyService(BaseService):
                @property
                @override
                def service_calc_class(self):
                    return MyServiceCalc

            config = ServiceConfig() # pyright:ignore[reportCallIssue]
            service = MyService(config)
            service.start()
    """

    def __init__(self, config: ServiceConfig):
        # initialize input data container and service calc
        self.service_calc = self.service_calc_class(
            simulation_id=config.simulation_id,
            model_id=config.model_id,
            influxdb_host=config.influxdb_host,
            influxdb_port=config.influxdb_port,
            influxdb_user=config.influxdb_user,
            influxdb_password=config.influxdb_password.get_secret_value(),
            influxdb_name=config.influxdb_name,
        )
        self.logger = logging.getLogger()

        self.input_data_inventory = InputDataInventory(
            self.service_calc.calculation_function_input_types,
            self.service_calc.service_name,
        )

        # initialize mqtt client
        self.mqtt_client = MqttClient(
            host=config.mqtt_host,
            port=config.mqtt_port,
            qos=config.mqtt_qos,
            username=config.mqtt_username,
            password=config.mqtt_password.get_secret_value(),
            input_data_inventory=self.input_data_inventory,
            service_calc=self.service_calc,
            service_name=self.service_calc.service_name,
            sim_logger=self.logger,
        )
        mqtt_handler = MqttLogHandler(self.mqtt_client)
        self.logger.addHandler(mqtt_handler)

    @property
    @abstractmethod
    def service_calc_class(self) -> type[ServiceCalc[CalculationFunction[Any, Any]]]:
        """
        Return the class (type not instance) to be instantiated in this Service.
        """
        pass

    def start(self):
        self.mqtt_client.wait_for_data()
