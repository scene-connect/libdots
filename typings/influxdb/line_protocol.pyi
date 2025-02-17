"""
This type stub file was generated by pyright.
"""

"""Define the line_protocol handler."""
EPOCH = ...
def quote_ident(value): # -> str:
    """Indent the quotes."""
    ...

def quote_literal(value): # -> str:
    """Quote provided literal."""
    ...

def make_line(measurement, tags=..., fields=..., time=..., precision=...): # -> str:
    """Extract the actual point from a given measurement line."""
    ...

def make_lines(data, precision=...): # -> LiteralString:
    """Extract points from given dict.

    Extracts the points from the given dict and returns a Unicode string
    matching the line protocol introduced in InfluxDB 0.9.0.
    """
    ...
