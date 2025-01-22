"""
This type stub file was generated by pyright.
"""

"""Module to prepare the resultset."""
_sentinel = ...
class ResultSet:
    """A wrapper around a single InfluxDB query result."""
    def __init__(self, series, raise_errors=...) -> None:
        """Initialize the ResultSet."""
        ...

    @property
    def raw(self): # -> Any:
        """Raw JSON from InfluxDB."""
        ...

    @raw.setter
    def raw(self, value): # -> None:
        ...

    @property
    def error(self):
        """Error returned by InfluxDB."""
        ...

    def __getitem__(self, key): # -> Generator[dict[Any, Any], Any, None]:
        """Retrieve the series name or specific set based on key.

        :param key: Either a series name, or a tags_dict, or
                    a 2-tuple(series_name, tags_dict).
                    If the series name is None (or not given) then any serie
                    matching the eventual given tags will be given its points
                    one after the other.
                    To get the points of every series in this resultset then
                    you have to provide None as key.
        :return: A generator yielding `Point`s matching the given key.
        NB:
        The order in which the points are yielded is actually undefined but
        it might change..
        """
        ...

    def get_points(self, measurement=..., tags=...): # -> Generator[dict[Any, Any], Any, None]:
        """Return a generator for all the points that match the given filters.

        :param measurement: The measurement name
        :type measurement: str

        :param tags: Tags to look for
        :type tags: dict

        :return: Points generator
        """
        ...

    def __repr__(self): # -> LiteralString:
        """Representation of ResultSet object."""
        ...

    def __iter__(self): # -> Generator[list[dict[Any, Any]], Any, None]:
        """Yield one dict instance per series result."""
        ...

    def __len__(self): # -> int:
        """Return the len of the keys in the ResultSet."""
        ...

    def keys(self): # -> list[Any]:
        """Return the list of keys in the ResultSet.

        :return: List of keys. Keys are tuples (series_name, tags)
        """
        ...

    def items(self): # -> list[Any]:
        """Return the set of items from the ResultSet.

        :return: List of tuples, (key, generator)
        """
        ...

    @staticmethod
    def point_from_cols_vals(cols, vals): # -> dict[Any, Any]:
        """Create a dict from columns and values lists.

        :param cols: List of columns
        :param vals: List of values
        :return: Dict where keys are columns.
        """
        ...
