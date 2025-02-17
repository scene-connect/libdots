"""
This type stub file was generated by pyright.
"""

from enum import Enum, unique

"""
This module gives the "listener" classes for the PyEcore notification layer.
The main class to create a new listener is "EObserver" which is triggered
each time a modification is perfomed on an observed element.
"""
class ENotifer:
    def __init__(self, **kwargs) -> None:
        ...

    def notify(self, notification): # -> None:
        ...



@unique
class Kind(Enum):
    ADD = ...
    ADD_MANY = ...
    MOVE = ...
    REMOVE = ...
    REMOVE_MANY = ...
    SET = ...
    UNSET = ...


class Notification:
    def __init__(self, notifier=..., kind=..., old=..., new=..., feature=...) -> None:
        ...

    def __repr__(self): # -> str:
        ...



class EObserver:
    def __init__(self, notifier=..., notifyChanged=...) -> None:
        ...

    def observe(self, notifier): # -> None:
        ...

    def notifyChanged(self, notification): # -> None:
        ...
