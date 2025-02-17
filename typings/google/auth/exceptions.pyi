"""
This type stub file was generated by pyright.
"""

"""Exceptions used in the google.auth package."""
class GoogleAuthError(Exception):
    """Base class for all google.auth errors."""
    def __init__(self, *args, **kwargs) -> None:
        ...

    @property
    def retryable(self):
        ...



class TransportError(GoogleAuthError):
    """Used to indicate an error occurred during an HTTP request."""
    ...


class RefreshError(GoogleAuthError):
    """Used to indicate that an refreshing the credentials' access token
    failed."""
    ...


class UserAccessTokenError(GoogleAuthError):
    """Used to indicate ``gcloud auth print-access-token`` command failed."""
    ...


class DefaultCredentialsError(GoogleAuthError):
    """Used to indicate that acquiring default credentials failed."""
    ...


class MutualTLSChannelError(GoogleAuthError):
    """Used to indicate that mutual TLS channel creation is failed, or mutual
    TLS channel credentials is missing or invalid."""
    ...


class ClientCertError(GoogleAuthError):
    """Used to indicate that client certificate is missing or invalid."""
    @property
    def retryable(self): # -> Literal[False]:
        ...



class OAuthError(GoogleAuthError):
    """Used to indicate an error occurred during an OAuth related HTTP
    request."""
    ...


class ReauthFailError(RefreshError):
    """An exception for when reauth failed."""
    def __init__(self, message=..., **kwargs) -> None:
        ...



class ReauthSamlChallengeFailError(ReauthFailError):
    """An exception for SAML reauth challenge failures."""
    ...


class MalformedError(DefaultCredentialsError, ValueError):
    """An exception for malformed data."""
    ...


class InvalidResource(DefaultCredentialsError, ValueError):
    """An exception for URL error."""
    ...


class InvalidOperation(DefaultCredentialsError, ValueError):
    """An exception for invalid operation."""
    ...


class InvalidValue(DefaultCredentialsError, ValueError):
    """Used to wrap general ValueError of python."""
    ...


class InvalidType(DefaultCredentialsError, TypeError):
    """Used to wrap general TypeError of python."""
    ...


class OSError(DefaultCredentialsError, EnvironmentError):
    """Used to wrap EnvironmentError(OSError after python3.3)."""
    ...


class TimeoutError(GoogleAuthError):
    """Used to indicate a timeout error occurred during an HTTP request."""
    ...


class ResponseError(GoogleAuthError):
    """Used to indicate an error occurred when reading an HTTP response."""
    ...
