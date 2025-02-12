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
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class ServiceConfig(BaseSettings):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "warn",
        "error",
        "fatal",
        "critical",
        "DEBUG",
        "INFO",
        "WARNING",
        "WARN",
        "ERROR",
        "FATAL",
        "CRITICAL",
    ] = "info"
    model_config = SettingsConfigDict(env_file=[".env", ".env.docker"])
    simulation_id: str
    model_id: str
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_qos: int = 0
    mqtt_username: str = ""
    mqtt_password: SecretStr = SecretStr("")
    influxdb_host: str = ""
    influxdb_port: int = 8086
    influxdb_user: str = ""
    influxdb_password: SecretStr = SecretStr("")
    influxdb_name: str = ""
