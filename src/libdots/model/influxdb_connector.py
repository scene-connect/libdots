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
from collections.abc import Iterable
from datetime import datetime
from datetime import timedelta
from datetime import timezone as tz
from typing import Any

import numpy
from influxdb import InfluxDBClient

from ..types import EsdlId
from ..types import ESDLObject


class InfluxDBConnector:
    """A connector writes data to an InfluxDB database."""

    def __init__(
        self,
        influx_host: str,
        influx_port: str,
        influx_user: str,
        influx_password: str,
        influx_database_name: str,
    ):
        self.influx_host: str = influx_host.split("//")[-1]
        self.influx_port: str = influx_port
        self.influx_database_name: str = influx_database_name
        self.influx_user: str = influx_user
        self.influx_password: str = influx_password
        self.logger = logging.getLogger(__name__)

        self.logger.debug(f"influx server: {self.influx_host}")
        self.logger.debug(f"influx port: {self.influx_port}")
        self.logger.debug(f"influx database: {self.influx_database_name}")

        self._client: InfluxDBClient | None = None
        self.simulation_id: str | None = None
        self.model_id: str | None = None
        self.esdl_type: str | None = None
        self.start_date: datetime | None = None
        self.time_step_seconds: int | None = None
        self.nr_of_time_steps: int | None = None
        self.profile_output_data: dict[
            EsdlId,
            dict[str, list[Any] | numpy.typing.NDArray[Any]],
        ] = {}
        self.summary_output_data: dict[EsdlId, dict[str, float]] = {}
        self.esdl_objects: dict[EsdlId, ESDLObject] | None = None

    @property
    def client(self) -> InfluxDBClient:
        if self._client is None:
            self._client = self.connect()
        return self._client

    def connect(self) -> InfluxDBClient:
        try:
            self.logger.debug("Connecting InfluxDBClient")
            client = InfluxDBClient(
                host=self.influx_host,
                port=int(self.influx_port),
                database=self.influx_database_name,
                username=self.influx_user,
                password=self.influx_password,
            )
            self.logger.debug(f"InfluxDBClient ping: {client.ping()}")
            return client
        except Exception as e:
            self.logger.debug(f"Failed to connect to influx db: {e}")
            raise

    def query(self, query: str):

        return self.client.query(query)

    def create_database(self):
        self.client.create_database(self.influx_database_name)

    def write(self, msgs: list[dict[str, Iterable[Any]]]):

        # Send message to database.
        self.client.write_points(
            msgs, database=self.influx_database_name, time_precision="s"
        )

    def close(self):
        if self._client is not None:
            self._client.close()
        self._client = None

    def init_profile_output_data(
        self,
        simulation_id: str,
        model_id: str,
        esdl_type: str,
        start_date: datetime,
        time_step_seconds: int,
        nr_of_time_steps: int,
        esdl_ids: list[EsdlId],
        output_names: list[str],
        esdl_objects: dict[EsdlId, ESDLObject],
    ):
        self.simulation_id = simulation_id
        self.esdl_type = esdl_type
        self.model_id = model_id
        self.start_date = start_date
        self.time_step_seconds = time_step_seconds
        self.nr_of_time_steps = nr_of_time_steps
        for esdl_id in esdl_ids:
            self.profile_output_data[esdl_id] = {}
            for output_name in output_names:
                self.profile_output_data[esdl_id][output_name] = numpy.zeros(
                    self.nr_of_time_steps
                )
            self.summary_output_data[esdl_id] = {}
        self.esdl_objects = esdl_objects

    def set_time_step_data_point(
        self, esdl_id: EsdlId, output_name: str, time_step_nr: int, value: float
    ):
        if numpy.isnan(value):
            self.logger.warning("Value for %s is nan, changing to 0.0", output_name)
            value = 0.0
        self.profile_output_data[esdl_id][output_name][time_step_nr - 1] = float(value)

    def set_summary_data_point(self, esdl_id: EsdlId, output_name: str, value: float):
        self.summary_output_data[esdl_id][output_name] = value

    def write_output(self):
        points: list[Any] = []
        first_timestamp: str | None = None
        assert self.nr_of_time_steps is not None, "We do not have a nr_of_time_steps"
        assert self.time_step_seconds is not None, "We do not have a time_step_seconds"
        assert self.start_date is not None, "We do not have a start_date"

        for i_step in range(self.nr_of_time_steps):
            step_time = (
                (
                    self.start_date
                    + timedelta(seconds=(i_step + 2) * self.time_step_seconds)
                )
                .astimezone(tz.utc)
                .strftime("%Y-%m-%dT%H:%M:%SZ")
            )
            if first_timestamp is None:
                first_timestamp = step_time

            for (
                esdl_id,
                esdl_object_profile_output_data,
            ) in self.profile_output_data.items():
                fields = {}
                for output_name in esdl_object_profile_output_data.keys():
                    if i_step < len(esdl_object_profile_output_data[output_name]):
                        fields[output_name] = esdl_object_profile_output_data[
                            output_name
                        ][i_step]
                    else:  # allow data writing even if simulation was terminated
                        fields[output_name] = 0.0
                self.add_measurement(points, esdl_id, step_time, fields)

        if self.summary_output_data and first_timestamp is not None:
            for (
                esdl_id,
                esdl_object_summary_output_data,
            ) in self.summary_output_data.items():
                fields: dict[str, Any] = {}
                for output_name in esdl_object_summary_output_data.keys():
                    fields[output_name] = esdl_object_summary_output_data[output_name]
                if fields:
                    self.add_measurement(points, esdl_id, first_timestamp, fields)

        self.logger.info(
            f"InfluxDB writing {len(points)} points to measurement '{self.esdl_type}'"
            f" with tag simulationRun {self.simulation_id}"
        )
        self.write(points)

    def add_measurement(
        self,
        points: list[dict[str, Any]],
        esdl_id: EsdlId,
        timestamp: str,
        fields: dict[str, Any],
    ):
        try:
            assert self.esdl_objects is not None
            if hasattr(self.esdl_objects[esdl_id], "name"):
                esdl_name = self.esdl_objects[esdl_id].name
            else:
                esdl_name = self.esdl_type
            item = {
                "measurement": f"{self.esdl_type}",
                "tags": {
                    "simulation_id": self.simulation_id,
                    "model_id": self.model_id,
                    "esdl_id": esdl_id,
                    "esdl_name": esdl_name,
                },
                "time": timestamp,
                "fields": fields,
            }
            points.append(item)
        except Exception as e:
            self.logger.debug(f"Exception: {e} {e.args}")
