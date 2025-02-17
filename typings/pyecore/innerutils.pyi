"""
This type stub file was generated by pyright.
"""

from contextlib import contextmanager

"""
This module gives decorators, functions and variables that are shared among the
different modules.
"""
class InternalSet(dict):
    add = ...


@contextmanager
def ignored(*exceptions): # -> Generator[None, Any, None]:
    """Gives a convenient way of ignoring exceptions.

    Obviously took from a Raymond Hettinger tweet
    """
    ...

javaTransMap = ...
def parse_date(str_date): # -> datetime:
    ...
