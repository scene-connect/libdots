"""
This type stub file was generated by pyright.
"""

from google.auth import _helpers
from google.auth.crypt import base

"""RSA verifier and signer that use the ``cryptography`` library.

This is a much faster implementation than the default (in
``google.auth.crypt._python_rsa``), which depends on the pure-Python
``rsa`` library.
"""
_CERTIFICATE_MARKER = ...
_BACKEND = ...
_PADDING = ...
_SHA256 = ...
class RSAVerifier(base.Verifier):
    """Verifies RSA cryptographic signatures using public keys.

    Args:
        public_key (
                cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey):
            The public key used to verify signatures.
    """
    def __init__(self, public_key) -> None:
        ...

    @_helpers.copy_docstring(base.Verifier)
    def verify(self, message, signature): # -> bool:
        ...

    @classmethod
    def from_string(cls, public_key): # -> Self:
        """Construct an Verifier instance from a public key or public
        certificate string.

        Args:
            public_key (Union[str, bytes]): The public key in PEM format or the
                x509 public key certificate.

        Returns:
            Verifier: The constructed verifier.

        Raises:
            ValueError: If the public key can't be parsed.
        """
        ...



class RSASigner(base.Signer, base.FromServiceAccountMixin):
    """Signs messages with an RSA private key.

    Args:
        private_key (
                cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey):
            The private key to sign with.
        key_id (str): Optional key ID used to identify this private key. This
            can be useful to associate the private key with its associated
            public key or certificate.
    """
    def __init__(self, private_key, key_id=...) -> None:
        ...

    @property
    @_helpers.copy_docstring(base.Signer)
    def key_id(self): # -> None:
        ...

    @_helpers.copy_docstring(base.Signer)
    def sign(self, message):
        ...

    @classmethod
    def from_string(cls, key, key_id=...): # -> Self:
        """Construct a RSASigner from a private key in PEM format.

        Args:
            key (Union[bytes, str]): Private key in PEM format.
            key_id (str): An optional key id used to identify the private key.

        Returns:
            google.auth.crypt._cryptography_rsa.RSASigner: The
            constructed signer.

        Raises:
            ValueError: If ``key`` is not ``bytes`` or ``str`` (unicode).
            UnicodeDecodeError: If ``key`` is ``bytes`` but cannot be decoded
                into a UTF-8 ``str``.
            ValueError: If ``cryptography`` "Could not deserialize key data."
        """
        ...

    def __getstate__(self): # -> dict[str, Any]:
        """Pickle helper that serializes the _key attribute."""
        ...

    def __setstate__(self, state): # -> None:
        """Pickle helper that deserializes the _key attribute."""
        ...
