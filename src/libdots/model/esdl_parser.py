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
from base64 import b64decode

from esdl import EnergySystem
from esdl import esdl
from esdl.esdl_handler import EnergySystemHandler

from ..types import CalculationServiceDescription
from ..types import EsdlId
from ..types import ESDLObject
from ..types import ServiceName


class ESDLParser:
    def __init__(self, receives_service_names_list: list[ServiceName]):
        self.receives_service_names_list = receives_service_names_list
        self.logger = logging.getLogger(__name__)

    def get_energy_system(self, esdl_base64string: str) -> EnergySystem:
        esdl_string = b64decode(esdl_base64string + b"==".decode("utf-8")).decode(
            "utf-8"
        )
        esh = EnergySystemHandler()
        esh.load_from_string(esdl_string)
        return esh.get_energy_system()

    def get_model_esdl_object(
        self, esdl_id: EsdlId, energy_system: EnergySystem
    ) -> ESDLObject:
        if energy_system.id == esdl_id:
            return energy_system
        # Iterate over all contents of the EnergySystem
        for obj in energy_system.eAllContents():
            if isinstance(obj, ESDLObject) and obj.id == esdl_id:
                return obj
        raise OSError(f"ESDL_ID '{esdl_id}' not found in provided ESDL file")

    def get_connected_input_esdl_objects(
        self,
        esdl_id: EsdlId,
        calculation_services: list[CalculationServiceDescription],
        energy_system: EnergySystem,
    ) -> dict[str, list[EsdlId]]:
        model_esdl_obj = self.get_model_esdl_object(esdl_id, energy_system)

        connected_input_esdl_objects: dict[str, list[EsdlId]] = {}

        if isinstance(model_esdl_obj, esdl.EnergyAsset):
            self.add_calc_services_from_ports(
                calculation_services, connected_input_esdl_objects, model_esdl_obj
            )
            self.add_calc_services_from_non_connected_objects(
                calculation_services, connected_input_esdl_objects, energy_system
            )
        else:
            self.add_calc_services_from_all_objects(
                calculation_services, connected_input_esdl_objects, energy_system
            )
        return connected_input_esdl_objects

    def get_connected_output_esdl_objects(
        self,
        esdl_id: EsdlId,
        calculation_services: list[CalculationServiceDescription],
        energy_system: EnergySystem,
    ) -> dict[str, list[EsdlId]]:
        model_esdl_obj = self.get_model_esdl_object(esdl_id, energy_system)

        connected_output_esdl_objects: dict[str, list[EsdlId]] = {}

        if isinstance(model_esdl_obj, esdl.EnergyAsset):
            self.add_calc_services_from_output_ports(
                calculation_services, connected_output_esdl_objects, model_esdl_obj
            )
        return connected_output_esdl_objects

    def add_calc_services_from_ports(
        self,
        calculation_services: list[CalculationServiceDescription],
        connected_input_esdl_objects: dict[str, list[EsdlId]],
        model_esdl_asset: esdl.EnergyAsset,
    ):
        # Iterate over all ports of this asset
        for port in model_esdl_asset.port:
            # only InPorts to find connected receiving services
            if isinstance(port, esdl.InPort):
                # Iterate over all connected ports of this port
                for connected_port in port.connectedTo:
                    # Get the asset to which the connected port belongs to
                    connected_asset = connected_port.eContainer()
                    self.add_esdl_object(
                        connected_input_esdl_objects,
                        connected_asset,
                        calculation_services,
                    )

    def add_calc_services_from_output_ports(
        self,
        calculation_services: list[CalculationServiceDescription],
        connected_input_esdl_objects: dict[str, list[EsdlId]],
        model_esdl_asset: esdl.EnergyAsset,
    ):
        # Iterate over all ports of this asset
        for port in model_esdl_asset.port:
            # only InPorts to find connected receiving services
            if isinstance(port, esdl.OutPort):
                # Iterate over all connected ports of this port
                for connected_port in port.connectedTo:
                    # Get the asset to which the connected port belongs to
                    connected_asset = connected_port.eContainer()
                    self.add_esdl_object(
                        connected_input_esdl_objects,
                        connected_asset,
                        calculation_services,
                    )

    def add_calc_services_from_non_connected_objects(
        self,
        calculation_services: list[CalculationServiceDescription],
        connected_input_esdl_objects: dict[str, list[EsdlId]],
        energy_system: ESDLObject,
    ):
        for esdl_obj in energy_system.eAllContents():
            if not isinstance(esdl_obj, esdl.EnergyAsset) and isinstance(
                esdl_obj, ESDLObject
            ):
                self.add_esdl_object(
                    connected_input_esdl_objects, esdl_obj, calculation_services
                )
        self.add_esdl_object(
            connected_input_esdl_objects, energy_system, calculation_services
        )

    def add_calc_services_from_all_objects(
        self,
        calculation_services: list[CalculationServiceDescription],
        connected_input_esdl_objects: dict[str, list[EsdlId]],
        energy_system: esdl.EnergySystem,
    ):
        for esdl_obj in energy_system.eAllContents():
            if isinstance(esdl_obj, ESDLObject):
                self.add_esdl_object(
                    connected_input_esdl_objects, esdl_obj, calculation_services
                )

    def add_esdl_object(
        self,
        connected_input_esdl_objects: dict[str, list[EsdlId]],
        esdl_obj: ESDLObject,
        calculation_services: list[CalculationServiceDescription],
    ):
        # find calculation service for ESDL object type
        current_esdl_type = type(esdl_obj).__name__

        calc_service = next(
            (
                calc_service
                for calc_service in calculation_services
                if calc_service["esdl_type"] == current_esdl_type
            ),
            None,
        )

        if (
            calc_service
            and calc_service["calc_service_name"] in self.receives_service_names_list
        ):
            service_name = calc_service["calc_service_name"]
            esdl_id = f"{str(esdl_obj.id)}"
            if service_name not in tuple(connected_input_esdl_objects):
                connected_input_esdl_objects[service_name] = [esdl_id]
            elif esdl_id not in connected_input_esdl_objects[service_name]:
                connected_input_esdl_objects[service_name].append(esdl_id)
        else:
            self.logger.debug(
                "No calculation service found for ESDL type %s", current_esdl_type
            )
