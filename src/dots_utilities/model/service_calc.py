import logging
import typing
from abc import ABC
from abc import abstractmethod
from collections.abc import Mapping
from collections.abc import Sequence
from datetime import datetime
from threading import Lock
from typing import Any
from typing import Generic
from typing import Literal
from typing import Protocol
from typing import TypeAlias
from typing import TypeVar

from esdl import EnergySystem
from esdl import URIProfile

from ..io.io_data import IODataInterface
from ..io.io_data import NewStep
from ..types import EsdlId
from ..types import ESDLObject
from ..types import ModelParametersDescription
from ..types import ServiceName
from .esdl_parser import ESDLParser
from .influxdb_connector import InfluxDBConnector

InputDataType: TypeAlias = Mapping[str, Sequence[IODataInterface]]
OutputDataType: TypeAlias = tuple[Mapping[EsdlId, IODataInterface], ...]

InputDataInterfaceT = TypeVar(
    "InputDataInterfaceT",
    # bound=InputDataType,
    contravariant=True,
)
OutputDataInterfaceT = TypeVar(
    "OutputDataInterfaceT",
    bound=OutputDataType,
    covariant=True,
)

"""
With python 3.14 https://peps.python.org/pep-0728/

class AllInputDataInterface(TypedDict, extra_items=Sequence[IODataInterface]):
    new_step: NewStep

"""
AllInputDataInterfaceT = Mapping[
    Literal["new_step"] | str, NewStep | Sequence[IODataInterface]
]


class CalculationFunction(Protocol[InputDataInterfaceT, OutputDataInterfaceT]):
    def __call__(
        self, new_step: NewStep, input_data: InputDataInterfaceT
    ) -> OutputDataInterfaceT: ...


CalculationFunctionT = TypeVar(
    "CalculationFunctionT", bound=CalculationFunction[Any, Any]
)


class ServiceCalc(ABC, Generic[CalculationFunctionT]):

    # filled during setup
    esdl_parser: ESDLParser
    simulation_name: str
    simulation_start_date: datetime
    time_step_seconds: int
    nr_of_time_steps: int
    esdl_energy_system: EnergySystem
    esdl_ids: list[EsdlId]
    service_name: ServiceName

    def __init__(
        self,
        simulation_id: str,
        model_id: str,
        influxdb_host: str,
        influxdb_port: int,
        influxdb_user: str,
        influxdb_password: str,
        influxdb_name: str,
    ):
        self.simulation_id = simulation_id
        self.model_id = model_id
        self.lock = Lock()
        self.logger = logging.getLogger(__name__)

        # set in setup()
        self.esdl_objects: dict[EsdlId, ESDLObject] = {}

        # per ESDL object:
        #     a dictionary with, per calculation service, a list of connected ESDL objects
        self.connected_input_esdl_objects_dict: dict[
            EsdlId, dict[ServiceName, list[EsdlId]]
        ] = {}

        self.connected_output_esdl_objects_dict: dict[
            EsdlId, dict[ServiceName, list[EsdlId]]
        ] = {}

        # for writing to influx db
        self.influxdb_client: InfluxDBConnector = InfluxDBConnector(
            influxdb_host,
            str(influxdb_port),
            influxdb_user,
            influxdb_password,
            influxdb_name,
        )

    @property
    @abstractmethod
    def calculation_functions(
        self,
    ) -> Mapping[str, CalculationFunctionT]:
        """Should return a dictionary mapping calculation function names to actual class methods."""
        pass

    @property
    @abstractmethod
    def receives_service_names(self) -> list[str]:
        """Should return a list of service names that this calculation service should receive data from."""
        return []

    @abstractmethod
    def process_esdl_object(self, esdl_id: EsdlId, esdl_object: ESDLObject):
        pass

    def setup_influxdb_output(self):
        pass

    # setup is called upon receiving 'ModelParameters' message
    def setup(
        self,
        model_parameters: ModelParametersDescription,
    ):
        self.simulation_name = model_parameters["simulation_name"]

        self.simulation_start_date = datetime.fromtimestamp(
            model_parameters["start_timestamp"]
        )
        self.time_step_seconds = int(model_parameters["time_step_seconds"])
        self.nr_of_time_steps = int(model_parameters["nr_of_time_steps"])
        self.esdl_parser = ESDLParser(self.receives_service_names)

        # get esdl uuids and system
        self.esdl_ids = model_parameters["esdl_ids"]
        self.esdl_energy_system = self.esdl_parser.get_energy_system(
            model_parameters["esdl_base64string"]
        )

        # get esdl objects and connected services for all esdl object in the model
        for esdl_id in self.esdl_ids:
            esdl_object = self.esdl_parser.get_model_esdl_object(
                esdl_id, self.esdl_energy_system
            )
            # run additional code for each esdl object
            self.process_esdl_object(esdl_id, esdl_object)

            # store the esdl object
            self.esdl_objects[esdl_id] = esdl_object
            # find connected esdl objects
            self.connected_input_esdl_objects_dict[esdl_id] = (
                self.esdl_parser.get_connected_input_esdl_objects(
                    esdl_id,
                    model_parameters["calculation_services"],
                    self.esdl_energy_system,
                )
            )

            self.connected_output_esdl_objects_dict[esdl_id] = (
                self.esdl_parser.get_connected_output_esdl_objects(
                    esdl_id,
                    model_parameters["calculation_services"],
                    self.esdl_energy_system,
                )
            )
        self.setup_influxdb_output()

    # write_to_influxdb is called upon 'SimulationDone' message
    def write_to_influxdb(self):
        if (
            self.influxdb_client and self.influxdb_client.simulation_id
        ):  # only if created and initialized
            self.logger.debug("Write to influx db")
            self.influxdb_client.write_output()

    def get_profile_uri_by_id(self, id: str) -> str:
        assert self.esdl_energy_system is not None
        for profile in self.esdl_energy_system.energySystemInformation.profiles.profile:
            if isinstance(profile, URIProfile) and profile.id == id:
                return profile.URI
        raise ValueError("No base URIProfile found with id {str}")

    # entry calculation function for redirection
    def calc_function(
        self,
        calc_name: str,
        input_data_dict: AllInputDataInterfaceT,
    ):
        try:
            # don't allow concurrent calculations on a service
            self.lock.acquire()
            if "new_step" not in input_data_dict or not isinstance(
                input_data_dict["new_step"], NewStep
            ):
                raise ValueError("new_step is missing or wrong type")
            new_step: NewStep = input_data_dict["new_step"]
            input_data_dict = dict(input_data_dict)
            del input_data_dict["new_step"]
            output_data_tuple = self.calculation_functions[calc_name](
                new_step,
                typing.cast(Mapping[str, Sequence[IODataInterface]], input_data_dict),
            )
            self.lock.release()
            return output_data_tuple
        except Exception as e:
            self.lock.release()
            raise e
