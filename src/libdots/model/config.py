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
    """
    The configuration of the calculation service.
    This uses `pydantic_settings <https://docs.pydantic.dev/latest/concepts/pydantic_settings/>`_
    with `dotenv <https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support>`_ support.
    Configuration values are (case-insensitive) read from:

        * environment variables
        * .env
        * .env.docker

    If you're using pyright's strict typing in your library, you need to add an ignore
    statement when instantiating it. pydantic-settings reads the missing
    parameters from environment variables so the missing parameters can be
    safely ignored.

        .. code-block:: python

            config = ServiceConfig() # pyright:ignore[reportCallIssue]
    """

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
    """:meta private:"""

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
