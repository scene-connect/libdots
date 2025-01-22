#  This work is based on original code developed and copyrighted by TNO 2023.
#  Subsequent contributions are licensed to you by the developers of such code and are
#  made available to the Project under one or several contributor license agreements.
#
#  This work is licensed to you under the Apache License, Version 2.0.
#  You may obtain a copy of the license at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#      TNO         - Initial implementation
#  Manager:
#      TNO


from typing import TypedDict

from esdl import DataSource
from esdl import EnergySystem
from esdl import GenericProfile
from esdl import Item

EsdlId = str
ServiceName = str

ESDLObject = Item | EnergySystem | GenericProfile | DataSource


class CalculationServiceDescription(TypedDict):
    esdl_type: str
    calc_service_name: str
    service_image_url: str


class ModelParametersDescription(TypedDict):
    simulation_name: str
    start_timestamp: float
    time_step_seconds: int
    nr_of_time_steps: int
    esdl_ids: list[EsdlId]
    calculation_services: list[CalculationServiceDescription]
    esdl_base64string: str
