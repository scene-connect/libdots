"""
This type stub file was generated by pyright.
"""

import abc
from dataclasses import dataclass
from typing import Optional
from google.auth import _helpers, external_account

"""AWS Credentials and AWS Signature V4 Request Signer.

This module provides credentials to access Google Cloud resources from Amazon
Web Services (AWS) workloads. These credentials are recommended over the
use of service account credentials in AWS as they do not involve the management
of long-live service account private keys.

AWS Credentials are initialized using external_account arguments which are
typically loaded from the external credentials JSON file.

This module also provides a definition for an abstract AWS security credentials supplier.
This supplier can be implemented to return valid AWS security credentials and an AWS region
and used to create AWS credentials. The credentials will then call the
supplier instead of using pre-defined methods such as calling the EC2 metadata endpoints.

This module also provides a basic implementation of the
`AWS Signature Version 4`_ request signing algorithm.

AWS Credentials use serialized signed requests to the
`AWS STS GetCallerIdentity`_ API that can be exchanged for Google access tokens
via the GCP STS endpoint.

.. _AWS Signature Version 4: https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html
.. _AWS STS GetCallerIdentity: https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html
"""
_AWS_ALGORITHM = ...
_AWS_REQUEST_TYPE = ...
_AWS_SECURITY_TOKEN_HEADER = ...
_AWS_DATE_HEADER = ...
_DEFAULT_AWS_REGIONAL_CREDENTIAL_VERIFICATION_URL = ...
_IMDSV2_SESSION_TOKEN_TTL_SECONDS = ...
class RequestSigner:
    """Implements an AWS request signer based on the AWS Signature Version 4 signing
    process.
    https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html
    """
    def __init__(self, region_name) -> None:
        """Instantiates an AWS request signer used to compute authenticated signed
        requests to AWS APIs based on the AWS Signature Version 4 signing process.

        Args:
            region_name (str): The AWS region to use.
        """
        ...

    def get_request_options(self, aws_security_credentials, url, method, request_payload=..., additional_headers=...): # -> dict[str, Any | dict[str, str | Any | None]]:
        """Generates the signed request for the provided HTTP request for calling
        an AWS API. This follows the steps described at:
        https://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html

        Args:
            aws_security_credentials (AWSSecurityCredentials): The AWS security credentials.
            url (str): The AWS service URL containing the canonical URI and
                query string.
            method (str): The HTTP method used to call this API.
            request_payload (Optional[str]): The optional request payload if
                available.
            additional_headers (Optional[Mapping[str, str]]): The optional
                additional headers needed for the requested AWS API.

        Returns:
            Mapping[str, str]: The AWS signed request dictionary object.
        """
        ...



@dataclass
class AwsSecurityCredentials:
    """A class that models AWS security credentials with an optional session token.

        Attributes:
            access_key_id (str): The AWS security credentials access key id.
            secret_access_key (str): The AWS security credentials secret access key.
            session_token (Optional[str]): The optional AWS security credentials session token. This should be set when using temporary credentials.
    """
    access_key_id: str
    secret_access_key: str
    session_token: Optional[str] = ...


class AwsSecurityCredentialsSupplier(metaclass=abc.ABCMeta):
    """Base class for AWS security credential suppliers. This can be implemented with custom logic to retrieve
    AWS security credentials to exchange for a Google Cloud access token. The AWS external account credential does
    not cache the AWS security credentials, so caching logic should be added in the implementation.
    """
    @abc.abstractmethod
    def get_aws_security_credentials(self, context, request):
        """Returns the AWS security credentials for the requested context.

        .. warning: This is not cached by the calling Google credential, so caching logic should be implemented in the supplier.

        Args:
            context (google.auth.externalaccount.SupplierContext): The context object
                containing information about the requested audience and subject token type.
            request (google.auth.transport.Request): The object used to make
                HTTP requests.

        Raises:
            google.auth.exceptions.RefreshError: If an error is encountered during
                security credential retrieval logic.

        Returns:
            AwsSecurityCredentials: The requested AWS security credentials.
        """
        ...

    @abc.abstractmethod
    def get_aws_region(self, context, request):
        """Returns the AWS region for the requested context.

        Args:
            context (google.auth.externalaccount.SupplierContext): The context object
                containing information about the requested audience and subject token type.
            request (google.auth.transport.Request): The object used to make
                HTTP requests.

        Raises:
            google.auth.exceptions.RefreshError: If an error is encountered during
                region retrieval logic.

        Returns:
            str: The AWS region.
        """
        ...



class _DefaultAwsSecurityCredentialsSupplier(AwsSecurityCredentialsSupplier):
    """Default implementation of AWS security credentials supplier. Supports retrieving
    credentials and region via EC2 metadata endpoints and environment variables.
    """
    def __init__(self, credential_source) -> None:
        ...

    @_helpers.copy_docstring(AwsSecurityCredentialsSupplier)
    def get_aws_security_credentials(self, context, request): # -> AwsSecurityCredentials:
        ...

    @_helpers.copy_docstring(AwsSecurityCredentialsSupplier)
    def get_aws_region(self, context, request): # -> str:
        ...



class Credentials(external_account.Credentials):
    """AWS external account credentials.
    This is used to exchange serialized AWS signature v4 signed requests to
    AWS STS GetCallerIdentity service for Google access tokens.
    """
    def __init__(self, audience, subject_token_type, token_url=..., credential_source=..., aws_security_credentials_supplier=..., *args, **kwargs) -> None:
        """Instantiates an AWS workload external account credentials object.

        Args:
            audience (str): The STS audience field.
            subject_token_type (str): The subject token type based on the Oauth2.0 token exchange spec.
                Expected values include::

                    “urn:ietf:params:aws:token-type:aws4_request”

            token_url (Optional [str]): The STS endpoint URL. If not provided, will default to "https://sts.googleapis.com/v1/token".
            credential_source (Optional [Mapping]): The credential source dictionary used
                to provide instructions on how to retrieve external credential to be exchanged for Google access tokens.
                Either a credential source or an AWS security credentials supplier must be provided.

                Example credential_source for AWS credential::

                    {
                        "environment_id": "aws1",
                        "regional_cred_verification_url": "https://sts.{region}.amazonaws.com?Action=GetCallerIdentity&Version=2011-06-15",
                        "region_url": "http://169.254.169.254/latest/meta-data/placement/availability-zone",
                        "url": "http://169.254.169.254/latest/meta-data/iam/security-credentials",
                        imdsv2_session_token_url": "http://169.254.169.254/latest/api/token"
                    }

            aws_security_credentials_supplier (Optional [AwsSecurityCredentialsSupplier]): Optional AWS security credentials supplier.
                This will be called to supply valid AWS security credentails which will then
                be exchanged for Google access tokens. Either an AWS security credentials supplier
                or a credential source must be provided.
            args (List): Optional positional arguments passed into the underlying :meth:`~external_account.Credentials.__init__` method.
            kwargs (Mapping): Optional keyword arguments passed into the underlying :meth:`~external_account.Credentials.__init__` method.

        Raises:
            google.auth.exceptions.RefreshError: If an error is encountered during
                access token retrieval logic.
            ValueError: For invalid parameters.

        .. note:: Typically one of the helper constructors
            :meth:`from_file` or
            :meth:`from_info` are used instead of calling the constructor directly.
        """
        ...

    def retrieve_subject_token(self, request):
        """Retrieves the subject token using the credential_source object.
        The subject token is a serialized `AWS GetCallerIdentity signed request`_.

        The logic is summarized as:

        Retrieve the AWS region from the AWS_REGION or AWS_DEFAULT_REGION
        environment variable or from the AWS metadata server availability-zone
        if not found in the environment variable.

        Check AWS credentials in environment variables. If not found, retrieve
        from the AWS metadata server security-credentials endpoint.

        When retrieving AWS credentials from the metadata server
        security-credentials endpoint, the AWS role needs to be determined by
        calling the security-credentials endpoint without any argument. Then the
        credentials can be retrieved via: security-credentials/role_name

        Generate the signed request to AWS STS GetCallerIdentity action.

        Inject x-goog-cloud-target-resource into header and serialize the
        signed request. This will be the subject-token to pass to GCP STS.

        .. _AWS GetCallerIdentity signed request:
            https://cloud.google.com/iam/docs/access-resources-aws#exchange-token

        Args:
            request (google.auth.transport.Request): A callable used to make
                HTTP requests.
        Returns:
            str: The retrieved subject token.
        """
        ...

    @classmethod
    def from_info(cls, info, **kwargs): # -> Self:
        """Creates an AWS Credentials instance from parsed external account info.

        Args:
            info (Mapping[str, str]): The AWS external account info in Google
                format.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.aws.Credentials: The constructed credentials.

        Raises:
            ValueError: For invalid parameters.
        """
        ...

    @classmethod
    def from_file(cls, filename, **kwargs): # -> Self:
        """Creates an AWS Credentials instance from an external account json file.

        Args:
            filename (str): The path to the AWS external account json file.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.aws.Credentials: The constructed credentials.
        """
        ...
