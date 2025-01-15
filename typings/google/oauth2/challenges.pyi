"""
This type stub file was generated by pyright.
"""

import abc
from google.auth import _helpers

""" Challenges for reauthentication.
"""
REAUTH_ORIGIN = ...
SAML_CHALLENGE_MESSAGE = ...
WEBAUTHN_TIMEOUT_MS = ...
def get_user_password(text): # -> str:
    """Get password from user.

    Override this function with a different logic if you are using this library
    outside a CLI.

    Args:
        text (str): message for the password prompt.

    Returns:
        str: password string.
    """
    ...

class ReauthChallenge(metaclass=abc.ABCMeta):
    """Base class for reauth challenges."""
    @property
    @abc.abstractmethod
    def name(self):
        """Returns the name of the challenge."""
        ...

    @property
    @abc.abstractmethod
    def is_locally_eligible(self):
        """Returns true if a challenge is supported locally on this machine."""
        ...

    @abc.abstractmethod
    def obtain_challenge_input(self, metadata):
        """Performs logic required to obtain credentials and returns it.

        Args:
            metadata (Mapping): challenge metadata returned in the 'challenges' field in
                the initial reauth request. Includes the 'challengeType' field
                and other challenge-specific fields.

        Returns:
            response that will be send to the reauth service as the content of
            the 'proposalResponse' field in the request body. Usually a dict
            with the keys specific to the challenge. For example,
            ``{'credential': password}`` for password challenge.
        """
        ...



class PasswordChallenge(ReauthChallenge):
    """Challenge that asks for user's password."""
    @property
    def name(self): # -> Literal['PASSWORD']:
        ...

    @property
    def is_locally_eligible(self): # -> Literal[True]:
        ...

    @_helpers.copy_docstring(ReauthChallenge)
    def obtain_challenge_input(self, unused_metadata): # -> dict[str, str]:
        ...



class SecurityKeyChallenge(ReauthChallenge):
    """Challenge that asks for user's security key touch."""
    @property
    def name(self): # -> Literal['SECURITY_KEY']:
        ...

    @property
    def is_locally_eligible(self): # -> Literal[True]:
        ...

    @_helpers.copy_docstring(ReauthChallenge)
    def obtain_challenge_input(self, metadata): # -> dict[str, dict[str, Any | int]] | dict[str, Any] | None:
        ...



class SamlChallenge(ReauthChallenge):
    """Challenge that asks the users to browse to their ID Providers.

    Currently SAML challenge is not supported. When obtaining the challenge
    input, exception will be raised to instruct the users to run
    `gcloud auth login` for reauthentication.
    """
    @property
    def name(self): # -> Literal['SAML']:
        ...

    @property
    def is_locally_eligible(self): # -> Literal[True]:
        ...

    def obtain_challenge_input(self, metadata):
        ...



AVAILABLE_CHALLENGES = ...
