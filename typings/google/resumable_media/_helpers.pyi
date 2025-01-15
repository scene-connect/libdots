"""
This type stub file was generated by pyright.
"""

"""Shared utilities used by both downloads and uploads."""
RANGE_HEADER = ...
CONTENT_RANGE_HEADER = ...
CONTENT_ENCODING_HEADER = ...
_SLOW_CRC32C_WARNING = ...
_GENERATION_HEADER = ...
_HASH_HEADER = ...
_STORED_CONTENT_ENCODING_HEADER = ...
_MISSING_CHECKSUM = ...
_LOGGER = ...
def do_nothing(): # -> None:
    """Simple default callback."""
    ...

def header_required(response, name, get_headers, callback=...):
    """Checks that a specific header is in a headers dictionary.

    Args:
        response (object): An HTTP response object, expected to have a
            ``headers`` attribute that is a ``Mapping[str, str]``.
        name (str): The name of a required header.
        get_headers (Callable[Any, Mapping[str, str]]): Helper to get headers
            from an HTTP response.
        callback (Optional[Callable]): A callback that takes no arguments,
            to be executed when an exception is being raised.

    Returns:
        str: The desired header.

    Raises:
        ~google.resumable_media.common.InvalidResponse: If the header
            is missing.
    """
    ...

def require_status_code(response, status_codes, get_status_code, callback=...):
    """Require a response has a status code among a list.

    Args:
        response (object): The HTTP response object.
        status_codes (tuple): The acceptable status codes.
        get_status_code (Callable[Any, int]): Helper to get a status code
            from a response.
        callback (Optional[Callable]): A callback that takes no arguments,
            to be executed when an exception is being raised.

    Returns:
        int: The status code.

    Raises:
        ~google.resumable_media.common.InvalidResponse: If the status code
            is not one of the values in ``status_codes``.
    """
    ...

def calculate_retry_wait(base_wait, max_sleep, multiplier=...): # -> tuple[Any, Any]:
    """Calculate the amount of time to wait before a retry attempt.

    Wait time grows exponentially with the number of attempts, until
    ``max_sleep``.

    A random amount of jitter (between 0 and 1 seconds) is added to spread out
    retry attempts from different clients.

    Args:
        base_wait (float): The "base" wait time (i.e. without any jitter)
            that will be multiplied until it reaches the maximum sleep.
        max_sleep (float): Maximum value that a sleep time is allowed to be.
        multiplier (float): Multiplier to apply to the base wait.

    Returns:
        Tuple[float, float]: The new base wait time as well as the wait time
        to be applied (with a random amount of jitter between 0 and 1 seconds
        added).
    """
    ...

def prepare_checksum_digest(digest_bytestring): # -> str:
    """Convert a checksum object into a digest encoded for an HTTP header.

    Args:
        bytes: A checksum digest bytestring.

    Returns:
        str: A base64 string representation of the input.
    """
    ...

def add_query_parameters(media_url, query_params): # -> str:
    """Add query parameters to a base url.

    Args:
        media_url (str): The URL containing the media to be downloaded.
        query_params (dict): Names and values of the query parameters to add.

    Returns:
        str: URL with additional query strings appended.
    """
    ...

class _DoNothingHash:
    """Do-nothing hash object.

    Intended as a stand-in for ``hashlib.md5`` or a crc32c checksum
    implementation in cases where it isn't necessary to compute the hash.
    """
    def update(self, unused_chunk): # -> None:
        """Do-nothing ``update`` method.

        Intended to match the interface of ``hashlib.md5`` and other checksums.

        Args:
            unused_chunk (bytes): A chunk of data.
        """
        ...
