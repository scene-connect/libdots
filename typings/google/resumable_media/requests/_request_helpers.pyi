"""
This type stub file was generated by pyright.
"""

"""Shared utilities used by both downloads and uploads.

This utilities are explicitly catered to ``requests``-like transports.
"""
_DEFAULT_RETRY_STRATEGY = ...
_SINGLE_GET_CHUNK_SIZE = ...
_DEFAULT_CONNECT_TIMEOUT = ...
_DEFAULT_READ_TIMEOUT = ...
_CONNECTION_ERROR_CLASSES = ...
class RequestsMixin:
    """Mix-in class implementing ``requests``-specific behavior.

    These are methods that are more general purpose, with implementations
    specific to the types defined in ``requests``.
    """
    ...


class RawRequestsMixin(RequestsMixin):
    ...


def wait_and_retry(func, get_status_code, retry_strategy):
    """Attempts to retry a call to ``func`` until success.

    Expects ``func`` to return an HTTP response and uses ``get_status_code``
    to check if the response is retry-able.

    ``func`` is expected to raise a failure status code as a
    common.InvalidResponse, at which point this method will check the code
    against the common.RETRIABLE list of retriable status codes.

    Will retry until :meth:`~.RetryStrategy.retry_allowed` (on the current
    ``retry_strategy``) returns :data:`False`. Uses
    :func:`_helpers.calculate_retry_wait` to double the wait time (with jitter)
    after each attempt.

    Args:
        func (Callable): A callable that takes no arguments and produces
            an HTTP response which will be checked as retry-able.
        get_status_code (Callable[Any, int]): Helper to get a status code
            from a response.
        retry_strategy (~google.resumable_media.common.RetryStrategy): The
            strategy to use if the request fails and must be retried.

    Returns:
        object: The return value of ``func``.
    """
    ...
