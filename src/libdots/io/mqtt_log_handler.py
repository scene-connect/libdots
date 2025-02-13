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
from logging import Formatter
from logging import Handler
from logging import LogRecord

from .mqtt_client import MqttClient


class MqttLogHandler(Handler):
    def __init__(self, client: MqttClient):
        super().__init__()
        formatter = Formatter(
            fmt="%(asctime)s [%(threadName)s][%(filename)s:%(lineno)d][%(levelname)s]: %(message)s"
        )
        super().setFormatter(formatter)
        self.client = client

    def emit(self, record: LogRecord):
        if record.levelno >= logging.INFO:
            self.client.send_log(self.format(record))
