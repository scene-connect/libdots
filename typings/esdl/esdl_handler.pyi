"""
This type stub file was generated by pyright.
"""

from io import BytesIO
from typing import Any
from typing import Dict

from esdl import esdl
from pyecore.ecore import EObject
from pyecore.resources import URI
from pyecore.resources.resource import Resource

"""
This type stub file was generated by pyright.
"""

class EnergySystemHandler:
    def __init__(self, energy_system=...) -> None: ...
    def load_file(self, uri_or_filename: str) -> esdl.EnergySystem:
        """Loads a file in a new resource set"""
        ...

    def load_uri(self, uri) -> esdl.EnergySystem:
        """Loads a new resource in a new resourceSet"""
        ...

    def add_uri(self, uri) -> esdl.EnergySystem:
        """Adds the specified URI to the resource set, i.e. load extra resources that the resource can refer to."""
        ...

    def load_from_string(self, esdl_string: str) -> esdl.EnergySystem: ...
    def to_string(self) -> str:
        """
        To serialize an energy system in a resource, we use a StringURI to save it to a string instead of a file
        :return: XML string of the current resource/ESDL file that is loaded.
        """
        ...

    def to_bytesio(self) -> BytesIO:
        """Returns a BytesIO stream for the energy system"""
        ...

    def get_external_reference(self, url: str, object_id: str = ...):
        """
        Support function to create a reference to an external ESDL/EDD file.

        :param url: web address e.g. a URL from the EDR, https://drive.esdl.hesi.energy/store/resource/edr/Public/Key figures/Emissiefactoren energiedragers 2017.edd
        :param object_id: Optional, the id of the object in the file to refer to, if not specified, it will return the root of the file.
        :return: EObject returning the root of the document, or the object that is specified by the id found in that file

        Be aware that when assigning an external reference to a containment relation, the content from the external reference
        will be moved (not copied) to the resource that it is assigned to. If you want the reference to be external,
        only use this for references (no diamond), not containment relations (a diamond in the ESDL UML diagram)
        """
        ...

    def save(self, filename=...):
        """Add the resource to the resourceSet when saving"""
        ...

    def save_as(self, filename):
        """Saves the resource under a different filename"""
        ...

    def get_energy_system(self) -> esdl.EnergySystem: ...
    def get_by_id(self, object_id) -> EObject: ...
    def get_by_id_slow(self, object_id) -> EObject: ...
    def update_uuid_dict(self, es: esdl.EnergySystem = ...) -> None:
        """
        Update the Resource's uuid_dict of a specific energy system
        This might be necessary when e.g. deepcopying an object in an resource that has references to other parts of that
        resource that are not being deepcopied.
        :param es: energy system that needs a uuid_dict update, if None, the current self.energy_system is used
        """
        ...

    def add_object(self, obj): ...
    def remove_object(self, obj): ...
    def remove_obj_by_id(self, obj_id): ...
    def get_all_instances_of_type(self, esdl_type): ...
    @staticmethod
    def instantiate_esdltype(className: str) -> EObject:
        """
        Instantiates a new instance of an ESDL class className and returns it.
        E.g. ip:InPort = instantiate_esdltype("InPort")
        """
        ...

    @staticmethod
    def resolve_fragment(resource: Resource, fragment: str):
        """
        Resolves a URI fragment (e.g. '//@instance.0/@area/@asset.0/@port.0') to the associated object
        and returns the object.
        This is used for objects that have no ID attribute
        """
        ...

    @staticmethod
    def attr_to_dict(esdl_object) -> Dict[str, Any]:
        """Creates a dict of all the attributes of an ESDL object, useful for printing/debugging"""
        ...

    @staticmethod
    def generate_uuid() -> str:
        """Creates a uuid: useful for generating unique IDs"""
        ...

    def create_empty_energy_system(
        self, name, es_description=..., inst_title=..., area_title=...
    ) -> esdl.EnergySystem:
        """
        Creates a new empty Energy System (EnergySystem + Instance + Area) and adds it to the resource set
        :param name:
        :param es_description: Optional
        :param inst_title: optional, default "Instance0"
        :param area_title:
        :return: the created empty Energy System
        """
        ...

    def __getstate__(self): ...
    def __setstate__(self, state): ...
    @staticmethod
    def version():
        """Returns the version of pyESDL"""
        ...

__version__ = ...

class StringURI(URI):
    def __init__(self, uri, text=...) -> None:
        """
        Creates a new StringURI to be used for a resource. By setting text it can convert that XML text to a
        python class model, when doing a resource.load(uri). If text is empty and the associated resource is not,
        resource.save(uri) will convert the resource to XML. Use uri.getvalue() to return the string representation of
        this resource.
        :param uri: the file name of this ESDL, should be unique in this resource set.
        :param text: XML string to convert to a resource (pyEcore classes)
        """
        ...

    def getvalue(self):
        """
        :return: the XML as a string of this ESDL resource
        """
        ...

    def create_instream(self): ...
    def create_outstream(self): ...
    def get_stream(self): ...
