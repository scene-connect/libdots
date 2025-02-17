"""
This type stub file was generated by pyright.
"""

from google.auth import _helpers
from google.auth.crypt import base

"""Pure-Python RSA cryptography implementation.

Uses the ``rsa``, ``pyasn1`` and ``pyasn1_modules`` packages
to parse PEM files storing PKCS#1 or PKCS#8 keys as well as
certificates. There is no support for p12 files.
"""
_POW2 = ...
_CERTIFICATE_MARKER = ...
_PKCS1_MARKER = ...
_PKCS8_MARKER = ...
_PKCS8_SPEC = ...
class RSAVerifier(base.Verifier):
    """Verifies RSA cryptographic signatures using public keys.

    Args:
        public_key (rsa.key.PublicKey): The public key used to verify
            signatures.
    """
    def __init__(self, public_key) -> None:
        ...

    @_helpers.copy_docstring(base.Verifier)
    def verify(self, message, signature): # -> Literal[False]:
        ...

    @classmethod
    def from_string(cls, public_key): # -> Self:
        """Construct an Verifier instance from a public key or public
        certificate string.

        Args:
            public_key (Union[str, bytes]): The public key in PEM format or the
                x509 public key certificate.

        Returns:
            google.auth.crypt._python_rsa.RSAVerifier: The constructed verifier.

        Raises:
            ValueError: If the public_key can't be parsed.
        """
        ...



class RSASigner(base.Signer, base.FromServiceAccountMixin):
    """Signs messages with an RSA private key.

    Args:
        private_key (rsa.key.PrivateKey): The private key to sign with.
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
        """Construct an Signer instance from a private key in PEM format.

        Args:
            key (str): Private key in PEM format.
            key_id (str): An optional key id used to identify the private key.

        Returns:
            google.auth.crypt.Signer: The constructed signer.

        Raises:
            ValueError: If the key cannot be parsed as PKCS#1 or PKCS#8 in
                PEM format.
        """
        ...
