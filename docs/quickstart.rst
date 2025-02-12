Quickstart
==========

Introduction
------------

DOTS consists of the following components:

* `Simulation Orchestrator <https://github.com/dots-energy/simulation-orchestrator>`_: Web application accepting and starting simulations
* `Model Service Orchestrator <https://github.com/dots-energy/model-services-orchestrator>`_: Container starting the individual models
  services and coordinating the startup and termination
* :ref:`Model Service <model-service>`: The actual models that together make up the energy network described in the ESDL file.

This library is aimed at making Model Services easier to write and maintain. It is strictly typed and therefore
requires python 3.12 or higher. But it does not require the other components to run the same python version,
and can also be mixed with calculation services which use older python version and were generated with the
original `calculation service generator <https://github.com/dots-energy/calculation-service-generator>`_

.. _model-service:

Model Services
--------------

Model Services are the core models that contain the real logic of the different components of the energy network.
A model service:

* handles one or more ESDL types
* can take inputs from other Model Services
* can produce output to be used by other Model Services
* can run with multiple workers in parallel sharing the load of simulating multiple ESDL objects of the same type

Each model service consists of one Calculation Service, which can have one or more calculation functions.
Most Calculation Services contain only a single function which contains the logic. For this function you
can define the inputs it needs to receive before it can do its job, and it can also produce outputs to be sent
to other Model Services.

Service
^^^^^^^

The (Model) Service itself is very simple. It should inherit from :py:class:`BaseService <libdots.model.service.BaseService>` and only needs to implement
a single property:

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

This defines the service called `MyService` and defines that it uses the Calculation Service `MyServiceCalc`


Calculation Service
^^^^^^^^^^^^^^^^^^^

The Calculation Service is where the real magic happens. It should inherit from :py:class:`ServiceCalc <libdots.model.service_calc.ServiceCalc>`.

The Calculation Service has 4 distinct phases:

* **init**: Before we know anything, the model is instantiated
* **setup**: This is triggered by the first message from the Model Service Orchestrator which contains the ESDL model and related parameters.
  During this stage, the ESDL model is parsed and any preparatory work like reading static profiles from uri's specified in URIProfile
  blocks in the ESDL model can take place.
* **time steps**: Each time step is triggered by a new MQTT message to start the new time step. The Calculation Service then waits for all input data
  messages it needs from other Model Services to do its work. Once they have all been received it can start its calculation function(s)
  and send the output from them.
* **teardown**: After all time steps completed the data from all timesteps is saved in influxdb.

From that class it needs to implement the following methods/properties:

* A specific calculation function (or more then one)
* :py:meth:`base_setup <libdots.model.service_calc.ServiceCalc.base_setup>`
* :py:meth:`calculation_functions <libdots.model.service_calc.ServiceCalc.calculation_functions>`
* :py:meth:`process_esdl_object <libdots.model.service_calc.ServiceCalc.process_esdl_object>`
* :py:meth:`receives_service_names <libdots.model.service_calc.ServiceCalc.receives_service_names>`
* :py:meth:`service_name <libdots.model.service_calc.ServiceCalc.service_name>`

And it can optionally implement:

* :py:meth:`setup_influxdb_output <libdots.model.service_calc.ServiceCalc.setup_influxdb_output>`


.. code-block:: python

    import random
    from collections.abc import Mapping
    from datetime import datetime
    from datetime import timezone as tz
    from typing import Any
    from typing import TypeAlias
    from typing import override

    from libdots.io.io_data import NewStep
    from libdots.model.service_calc import CalculationFunction
    from libdots.model.service_calc import ServiceCalc
    from libdots.types import EsdlId
    from libdots.types import ESDLObject
    from libdots.types import ServiceName

    from ..io.io_data import Load


    # The input data type we are expecting for this service and the output data type we are producing.
    BaseLoadOutputData: TypeAlias = tuple[Mapping[EsdlId, Load]] # We are returning a type of type Load
    BaseLoadInputData: TypeAlias = Mapping[str, Any]  # we're not expecting any input data


    class BaseLoadServiceCalc(
        ServiceCalc[CalculationFunction[BaseLoadInputData, BaseLoadOutputData]]
    ):
        """
        Define that we inherit from a ServiceCalc implementing a single CalculationFunction,
        with its respective Input and Output data types that it consumes/produces from MQTT messages.
        """

        @property
        @override
        def service_name(self):
            return "base_loads"

        @override
        def base_setup(self):
            """Nothing to do in this case"""
            pass

        @override
        def process_esdl_object(self, esdl_id: EsdlId, esdl_object: ESDLObject):
            """
            Run during setup for each esdl object this service calc should process.

            In this case there is no pre-processing to be done.
            """

        @override
        def setup_influxdb_output(self):
            """
            If we want to store data in influxdb for this Calculation Service, this is where we set that up.
            InfluxDB will get tags for the model_id, simulation_id, etc. And `profile_output_data_names` are the
            fields it will record per time step and per esdl object.
            """

            profile_output_data_names = ["base_load"]
            self.influxdb_client.init_profile_output_data(
                self.simulation_id,
                self.model_id,
                type(list(self.esdl_objects.values())[0]).__name__.lower(), # class name of the esdl objects
                self.simulation_start_date,
                self.time_step_seconds,
                self.nr_of_time_steps,
                self.esdl_ids, # ids of the different esdl objects serviced by this Model Service
                profile_output_data_names,
                self.esdl_objects, # the esdl objects themselves
            )

        @property
        @override
        def calculation_functions(
            self,
        ) -> Mapping[str, CalculationFunction[BaseLoadInputData, BaseLoadOutputData]]:
            """The calculation function name and actual function that this Calculation Service provides."""
            return {"base_loads": self.base_loads}

        @property
        @override
        def receives_service_names(
            self,
        ) -> list[ServiceName]:
            """
            A list of Model Services that we are expecting input from. In this case we are not expecting any
            input.
            """
            return []

        def base_loads(
            self, new_step: NewStep, input_data: BaseLoadInputData
        ) -> BaseLoadOutputData:
            """This is the meat of the model. In this case we are sending a random value between 0 and 10kW."""
            self.logger.info("calculation 'base_loads' started")

            start_datetime = datetime.fromtimestamp(
                new_step.parameters_dict["start_time_stamp"], tz=tz.utc
            )

            # load per esdl object
            load_dict: dict[EsdlId, Load] = {}

            for (
                esdl_id
            ) in self.esdl_ids:  # loop over all ESDL objects in this Model Service instance
                self.logger.debug(
                    "getting base load for esdl_id %s at %s",
                    esdl_id,
                    start_datetime,
                )
                load = random.randint(0,10000) #random load in kW
                # write to influx db:
                time_step_nr = int(new_step.parameters_dict["time_step_nr"])
                self.influxdb_client.set_time_step_data_point(
                    esdl_id, "base_load", time_step_nr, load
                )

                load_dict[esdl_id] = Load(esdl_id, load)

            self.logger.info("calculation 'base_loads' finished")

            # return the data as a tuple of dictionaries. This is sent as output mqtt messages.
            return (load_dict,)

Receiving input data
^^^^^^^^^^^^^^^^^^^^

*TODO*

Reading static profile data
^^^^^^^^^^^^^^^^^^^^^^^^^^^

*TODO*

Generating input/output MQTT message types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Define protobuf messages for instance in ``my_model.io.message_definitions``
You can then compile them into python classes with
.. code-block:: bash

    python3 -m grpc_tools.protoc -I=my_model/io/message_definitions --python_out=my_model/io/messages --pyi_out=./my_model/io/messages  my_model/io/message_definitions/*.proto

This produces python classes and type stubs in ``my_model.io.messages``.
The script in ``./scripts/compile_protobuf.sh`` is a reference you can use.

Once you have those types, you need to turn those into a class inheriting from :py:class:`IODataInterface <libdots.io.io_data.IODataInterface>`
to be used as input/output data from the Calculation Service.

This is an example for our ``Load`` object used above as output:

..code-block:: python

    from typing import override

    from libdots.io.io_data import IODataInterface
    from libdots.types import EsdlId

    from . import messages


    class Load(IODataInterface):

        # Attributes for this message.
        kw: float
        origin_esdl_id: EsdlId # source esdl_id of the ESDL object this message came from.

        def __init__(self, origin_esdl_id: EsdlId | None = None, kw: float | None = None):
            if origin_esdl_id is not None:
                self.origin_esdl_id = origin_esdl_id
            if kw is not None:
                self.kw = kw

        @override
        def set_values_from_serialized_protobuf(self, serialized_message: bytes):
            """Generate the protobuf messages from this object."""
            config_data = messages.Load()
            config_data.ParseFromString(serialized_message)
            self.origin_esdl_id = config_data.origin_esdl_id
            self.kw = config_data.kw

        @override
        def get_values_as_serialized_protobuf(self) -> bytes:
            """Load the protobuf messages into the object,"""
            protobuf_message = messages.Load()
            protobuf_message.origin_esdl_id = self.origin_esdl_id
            protobuf_message.kw = self.kw
            return protobuf_message.SerializeToString()

        @classmethod
        @override
        def get_name(cls) -> str:
            return "load"

        @classmethod
        @override
        def get_main_topic(cls) -> str:
            """The topic to send data on"""
            return "/data/base_loads/model"

        @classmbuethod
        @override
        def get_variable_descr(cls) -> str:
            """Text description of the attributes."""
            return "{'kw': 'float'}"
