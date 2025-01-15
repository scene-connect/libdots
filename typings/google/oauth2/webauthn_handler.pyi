"""
This type stub file was generated by pyright.
"""

import abc
from google.oauth2.webauthn_types import GetRequest, GetResponse

class WebAuthnHandler(abc.ABC):
    @abc.abstractmethod
    def is_available(self) -> bool:
        """Check whether this WebAuthn handler is available"""
        ...

    @abc.abstractmethod
    def get(self, get_request: GetRequest) -> GetResponse:
        """WebAuthn get (assertion)"""
        ...



class PluginHandler(WebAuthnHandler):
    """Offloads WebAuthn get reqeust to a pluggable command-line tool.

    Offloads WebAuthn get to a plugin which takes the form of a
    command-line tool. The command-line tool is configurable via the
    PluginHandler._ENV_VAR environment variable.

    The WebAuthn plugin should implement the following interface:

    Communication occurs over stdin/stdout, and messages are both sent and
    received in the form:

    [4 bytes - payload size (little-endian)][variable bytes - json payload]
    """
    _ENV_VAR = ...
    def is_available(self) -> bool:
        ...

    def get(self, get_request: GetRequest) -> GetResponse:
        ...
