"""
This type stub file was generated by pyright.
"""

from contextlib import contextmanager

"""Manages OpenTelemetry tracing span creation and handling. This is a PREVIEW FEATURE: Coverage and functionality may change."""
ENABLE_OTEL_TRACES_ENV_VAR = ...
_DEFAULT_ENABLE_OTEL_TRACES_VALUE = ...
enable_otel_traces = ...
logger = ...
HAS_OPENTELEMETRY = ...
_default_attributes = ...
_cloud_trace_adoption_attrs = ...
@contextmanager
def create_trace_span(name, attributes=..., client=..., api_request=..., retry=...): # -> Generator[Any | None, Any, None]:
    """Creates a context manager for a new span and set it as the current span
    in the configured tracer. If no configuration exists yields None."""
    ...
