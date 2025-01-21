"""
This type stub file was generated by pyright.
"""

"""
Support functions for managing EObjects
"""
logger = ...
def clone(self): # -> Any:
    """
    Shallow copying or cloning an object
    It only copies the object's attributes (e.g. clone an object)
    Usage object.clone() or copy.copy(object) (as _copy__() is also implemented)
    :param self:
    :return: A clone of the object
    """
    ...

def deepcopy(self, memo=..., target_es=...):
    """
    Deep copying an EObject.
    Does not work yet for copying references from other resources than this one.
    """
    ...

