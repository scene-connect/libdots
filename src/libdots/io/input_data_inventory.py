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
from threading import Lock

from ..types import EsdlId
from .io_data import IODataInterface
from .io_data import ModelParameters
from .io_data import NewStep


class InputDataInventory:
    def __init__(
        self,
        calculation_messages: dict[str, list[type[IODataInterface]]],
        service_name: str,
    ):
        self.lock = Lock()
        self.logger = logging.getLogger(__name__)
        self.service_name = service_name

        # required data class types per calculation
        self.calcs_input_classes = calculation_messages
        """
        example:
        self.calcs_input_classes: dict = {
            "post_battery": [NewStep, ChargeConsumption, Supply],
            "pre_battery": [NewStep, Load, PvOutput, Import, Export],
        }
        """

        # expected ESDL objects (id's), per calculation service (identified by main topic) providing input
        self._expected_esdl_ids_dict: dict[str, list[EsdlId]] | None = None

        # input_data dict with a list of IODataInterface instances per IO_class
        self.input_data_dict: dict[str, list[IODataInterface]] = {}
        self.delete_all_received_input_data()

        # keep track of which calculations are done
        self.calcs_done: list[str] = []
        self.calc_names_all_received: list[str] = []

    @property
    def expected_esdl_ids_dict(self) -> dict[str, list[EsdlId]]:
        if self._expected_esdl_ids_dict is None:
            raise ValueError(
                "expected_esdl_ids_dict not set. Please call set_expected_esdl_ids_for_input_data first."
            )
        return self._expected_esdl_ids_dict

    # reset input_data_dict to empty lists for each data type, and reset calcs_done
    def delete_all_received_input_data(self):
        self.lock.acquire()
        self.logger.debug("Removing all input data...")
        for calc_input_classes in self.calcs_input_classes.values():
            for input_class in calc_input_classes:
                self.input_data_dict[input_class.get_name()] = []
        self.calcs_done = []
        self.calc_names_all_received = []
        self.logger.debug("All input data removed!")
        self.lock.release()

    def set_expected_esdl_ids_for_input_data(
        self, connected_input_esdl_objects_dict: dict[str, dict[str, list[EsdlId]]]
    ):
        # add lifecyle main topic for NewStep
        self._expected_esdl_ids_dict = {"/lifecycle/dots-so/model": ["dots-so"]}

        for connected_input_esdl_objects in connected_input_esdl_objects_dict.values():
            for service_name, esdl_ids in connected_input_esdl_objects.items():
                for esdl_id in esdl_ids:
                    if (
                        f"/data/{service_name}/model"
                        not in self._expected_esdl_ids_dict
                    ):
                        self._expected_esdl_ids_dict[f"/data/{service_name}/model"] = [
                            esdl_id
                        ]
                    elif (
                        esdl_id
                        not in self._expected_esdl_ids_dict[
                            f"/data/{service_name}/model"
                        ]
                    ):
                        self._expected_esdl_ids_dict[
                            f"/data/{service_name}/model"
                        ].append(esdl_id)
        self.logger.debug(
            f" set expecting input ESDL objects for 'home_network_with_battery': {self._expected_esdl_ids_dict}"
        )

    # add input data and return a list of calculation names that have received all required input objects
    def add_input(
        self, main_topic: str, data_name: str, serialized_values: bytes
    ) -> list[str]:
        # lock data_inventory to avoid simultaneous editing and consequent problems with checking if all required input
        # data is present
        self.lock.acquire()

        # create a new IODataInterface instance from received data and add to input_data_dict
        input_class_instance = self._find_and_create_class(
            main_topic, data_name, serialized_values
        )

        if input_class_instance:
            if (
                not isinstance(input_class_instance, ModelParameters)
                and self._expected_esdl_ids_dict is None
            ):
                raise OSError("Input data received before model parameters were set")
            self.input_data_dict[data_name].append(input_class_instance)
            self.logger.debug(
                f" added '{data_name}' data for service '{self.service_name}': {input_class_instance.get_variable_descr()}"
            )

        # per calc, check if all input data is present
        non_executed_calc_names_input_received = (
            self._get_new_calcs_with_all_input_received()
        )

        self.lock.release()
        # return list of calc names that have received all required input data
        return non_executed_calc_names_input_received

    # for a specific calculation, get the needed input data:
    def get_input_data(
        self, calc_name: str
    ) -> dict[str, NewStep | list[IODataInterface]]:
        input_data: dict[str, NewStep | list[IODataInterface]] = {}
        for data_class in self.calcs_input_classes[calc_name]:
            if data_class == NewStep:
                data = self.input_data_dict[data_class.get_name()][0]
                if not isinstance(data, NewStep):
                    raise TypeError(
                        f"data type for new_step is {type(data)} instead of NewStep"
                    )
                input_data["new_step"] = data
            else:
                input_data[data_class.get_name() + "_list"] = self.input_data_dict[
                    data_class.get_name()
                ]
        return input_data

    def is_step_active(self) -> bool:
        return (
            "new_step" in self.input_data_dict
            and self.input_data_dict["new_step"] != []
        )

    def _find_and_create_class(
        self, main_topic: str, data_name: str, serialized_values: bytes
    ) -> IODataInterface | None:
        input_class_instance = (
            None  # avoid multiple adding (input can be used by multiple calculations)
        )

        for calc_input_classes in self.calcs_input_classes.values():
            for input_class in calc_input_classes:
                if (
                    input_class.get_main_topic() == main_topic
                    and input_class.get_name() == data_name
                    and not input_class_instance
                ):  # avoid multiple adding (multiple calculations can use input)
                    input_class_instance = self.create_new_class(
                        input_class, serialized_values
                    )

        if not input_class_instance:
            self.logger.debug(
                f"No data class could be found for topic '{main_topic}', data name '{data_name}'."
            )

        return input_class_instance

    def create_new_class(
        self, input_class: type[IODataInterface], serialized_values: bytes
    ) -> IODataInterface:
        try:
            input_data_class = input_class()
            if len(serialized_values) > 0:
                input_data_class.set_values_from_serialized_protobuf(serialized_values)
            return input_data_class
        except TypeError:
            self.lock.release()
            raise OSError(
                f"The data class '{input_class.get_name()}' does not have the correct variables."
                f"\nVariables required: {input_class.get_variable_descr()}"
            )

    def _get_new_calcs_with_all_input_received(self) -> list[str]:
        return_val: list[str] = []
        for calc_name, calc_input_classes in self.calcs_input_classes.items():
            if (
                calc_name not in self.calcs_done
            ):  # check if all input available per calculation
                all_received = True
                for (
                    input_class
                ) in (
                    calc_input_classes
                ):  # check if all input available per input data class
                    nr_of_data_class_objects_received = len(
                        self.input_data_dict[input_class.get_name()]
                    )
                    if (
                        self._expected_esdl_ids_dict is not None
                        and input_class.get_main_topic() in self._expected_esdl_ids_dict
                    ):
                        nr_of_data_class_objects_expected = len(
                            self._expected_esdl_ids_dict[input_class.get_main_topic()]
                        )
                    else:
                        nr_of_data_class_objects_expected = 0

                    if (
                        nr_of_data_class_objects_received
                        < nr_of_data_class_objects_expected
                    ):
                        all_received = False

                if all_received and calc_name not in self.calc_names_all_received:
                    self.calc_names_all_received.append(calc_name)
                    return_val.append(calc_name)
        return return_val

    def set_calc_done(self, calc_name: str):
        self.lock.acquire()
        self.calcs_done.append(calc_name)
        self.lock.release()

    def all_calcs_done(self):
        return len(self.calcs_done) == len(self.calcs_input_classes)
