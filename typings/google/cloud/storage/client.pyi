"""
This type stub file was generated by pyright.
"""

from google.cloud.client import ClientWithProject
from google.cloud.storage import Bucket
from google.cloud.storage._opentelemetry_tracing import create_trace_span

"""Client for interacting with the Google Cloud Storage API."""
_marker = ...

class Client(ClientWithProject):
    """Client to bundle configuration needed for API requests.

    :type project: str or None
    :param project: the project which the client acts on behalf of. Will be
                    passed when creating a topic.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed (and if no ``_http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type _http: :class:`~requests.Session`
    :param _http: (Optional) HTTP object to make requests. Can be any object
                  that defines ``request()`` with the same interface as
                  :meth:`requests.Session.request`. If not passed, an
                  ``_http`` object is created that is bound to the
                  ``credentials`` for the current object.
                  This parameter should be considered private, and could
                  change in the future.

    :type client_info: :class:`~google.api_core.client_info.ClientInfo`
    :param client_info:
        The client info used to send a user-agent string along with API
        requests. If ``None``, then default info will be used. Generally,
        you only need to set this if you're developing your own library
        or partner tool.

    :type client_options: :class:`~google.api_core.client_options.ClientOptions` or :class:`dict`
    :param client_options: (Optional) Client options used to set user options on the client.
        A non-default universe domain or api endpoint should be set through client_options.

    :type use_auth_w_custom_endpoint: bool
    :param use_auth_w_custom_endpoint:
        (Optional) Whether authentication is required under custom endpoints.
        If false, uses AnonymousCredentials and bypasses authentication.
        Defaults to True. Note this is only used when a custom endpoint is set in conjunction.

    :type extra_headers: dict
    :param extra_headers:
        (Optional) Custom headers to be sent with the requests attached to the client.
        For example, you can add custom audit logging headers.
    """

    SCOPE = ...
    def __init__(
        self,
        project=...,
        credentials=...,
        _http=...,
        client_info=...,
        client_options=...,
        use_auth_w_custom_endpoint=...,
        extra_headers=...,
    ) -> None: ...
    @classmethod
    def create_anonymous_client(cls):  # -> Self:
        """Factory: return client with anonymous credentials.

        .. note::

           Such a client has only limited access to "public" buckets:
           listing their contents and downloading their blobs.

        :rtype: :class:`google.cloud.storage.client.Client`
        :returns: Instance w/ anonymous credentials and no project.
        """
        ...

    @property
    def universe_domain(self):  # -> str:
        ...

    @property
    def api_endpoint(self): ...
    @property
    def current_batch(self):  # -> None:
        """Currently-active batch.

        :rtype: :class:`google.cloud.storage.batch.Batch` or ``NoneType`` (if
                no batch is active).
        :returns: The batch at the top of the batch stack.
        """
        ...

    @create_trace_span(name="Storage.Client.getServiceAccountEmail")
    def get_service_account_email(self, project=..., timeout=..., retry=...):
        """Get the email address of the project's GCS service account

        :type project: str
        :param project:
            (Optional) Project ID to use for retreiving GCS service account
            email address.  Defaults to the client's project.
        :type timeout: float or tuple
        :param timeout:
            (Optional) The amount of time, in seconds, to wait
            for the server response.  See: :ref:`configuring_timeouts`

        :type retry: google.api_core.retry.Retry or google.cloud.storage.retry.ConditionalRetryPolicy
        :param retry:
            (Optional) How to retry the RPC. See: :ref:`configuring_retries`

        :rtype: str
        :returns: service account email address
        """
        ...

    def bucket(self, bucket_name, user_project=..., generation=...) -> Bucket:
        """Factory constructor for bucket object.

        .. note::
          This will not make an HTTP request; it simply instantiates
          a bucket object owned by this client.

        :type bucket_name: str
        :param bucket_name: The name of the bucket to be instantiated.

        :type user_project: str
        :param user_project: (Optional) The project ID to be billed for API
                             requests made via the bucket.

        :type generation: int
        :param generation: (Optional) If present, selects a specific revision of
                           this bucket.

        :rtype: :class:`google.cloud.storage.bucket.Bucket`
        :returns: The bucket object created.
        """
        ...

    def batch(self, raise_exception=...):  # -> Batch:
        """Factory constructor for batch object.

        .. note::
          This will not make an HTTP request; it simply instantiates
          a batch object owned by this client.

        :type raise_exception: bool
        :param raise_exception:
            (Optional) Defaults to True. If True, instead of adding exceptions
            to the list of return responses, the final exception will be raised.
            Note that exceptions are unwrapped after all operations are complete
            in success or failure, and only the last exception is raised.

        :rtype: :class:`google.cloud.storage.batch.Batch`
        :returns: The batch object created.
        """
        ...

    @create_trace_span(name="Storage.Client.getBucket")
    def get_bucket(
        self,
        bucket_or_name: str | Bucket,
        timeout: int = ...,
        if_metageneration_match=...,
        if_metageneration_not_match=...,
        retry=...,
        *,
        generation=...,
        soft_deleted=...
    ) -> Bucket:
        """Retrieve a bucket via a GET request.

        See [API reference docs](https://cloud.google.com/storage/docs/json_api/v1/buckets/get) and a [code sample](https://cloud.google.com/storage/docs/samples/storage-get-bucket-metadata#storage_get_bucket_metadata-python).

        Args:
            bucket_or_name (Union[ \
                :class:`~google.cloud.storage.bucket.Bucket`, \
                 str, \
            ]):
                The bucket resource to pass or name to create.

            timeout (Optional[Union[float, Tuple[float, float]]]):
                The amount of time, in seconds, to wait for the server response.

                Can also be passed as a tuple (connect_timeout, read_timeout).
                See :meth:`requests.Session.request` documentation for details.

            if_metageneration_match (Optional[int]):
                Make the operation conditional on whether the
                bucket's current metageneration matches the given value.

            if_metageneration_not_match (Optional[int]):
                Make the operation conditional on whether the bucket's
                current metageneration does not match the given value.

            retry (Optional[Union[google.api_core.retry.Retry, google.cloud.storage.retry.ConditionalRetryPolicy]]):
                How to retry the RPC. A None value will disable retries.
                A google.api_core.retry.Retry value will enable retries, and the object will
                define retriable response codes and errors and configure backoff and timeout options.

                A google.cloud.storage.retry.ConditionalRetryPolicy value wraps a Retry object and
                activates it only if certain conditions are met. This class exists to provide safe defaults
                for RPC calls that are not technically safe to retry normally (due to potential data
                duplication or other side-effects) but become safe to retry if a condition such as
                if_metageneration_match is set.

                See the retry.py source code and docstrings in this package (google.cloud.storage.retry) for
                information on retry types and how to configure them.

            generation (Optional[int]):
                The generation of the bucket. The generation can be used to
                specify a specific soft-deleted version of the bucket, in
                conjunction with the ``soft_deleted`` argument below. If
                ``soft_deleted`` is not True, the generation is unused.

            soft_deleted (Optional[bool]):
                If True, looks for a soft-deleted bucket. Will only return
                the bucket metadata if the bucket exists and is in a
                soft-deleted state. The bucket ``generation`` is required if
                ``soft_deleted`` is set to True.
                See: https://cloud.google.com/storage/docs/soft-delete

        Returns:
            google.cloud.storage.bucket.Bucket
                The bucket matching the name provided.

        Raises:
            google.cloud.exceptions.NotFound
                If the bucket is not found.
        """
        ...

    @create_trace_span(name="Storage.Client.lookupBucket")
    def lookup_bucket(
        self,
        bucket_name,
        timeout=...,
        if_metageneration_match=...,
        if_metageneration_not_match=...,
        retry=...,
    ):  # -> Bucket | None:
        """Get a bucket by name, returning None if not found.

        You can use this if you would rather check for a None value
        than catching a NotFound exception.

        :type bucket_name: str
        :param bucket_name: The name of the bucket to get.

        :type timeout: float or tuple
        :param timeout:
            (Optional) The amount of time, in seconds, to wait
            for the server response.  See: :ref:`configuring_timeouts`

        :type if_metageneration_match: long
        :param if_metageneration_match: (Optional) Make the operation conditional on whether the
                                        blob's current metageneration matches the given value.

        :type if_metageneration_not_match: long
        :param if_metageneration_not_match: (Optional) Make the operation conditional on whether the
                                            blob's current metageneration does not match the given value.

        :type retry: google.api_core.retry.Retry or google.cloud.storage.retry.ConditionalRetryPolicy
        :param retry:
            (Optional) How to retry the RPC. See: :ref:`configuring_retries`

        :rtype: :class:`google.cloud.storage.bucket.Bucket` or ``NoneType``
        :returns: The bucket matching the name provided or None if not found.
        """
        ...

    @create_trace_span(name="Storage.Client.createBucket")
    def create_bucket(
        self,
        bucket_or_name,
        requester_pays=...,
        project=...,
        user_project=...,
        location=...,
        data_locations=...,
        predefined_acl=...,
        predefined_default_object_acl=...,
        enable_object_retention=...,
        timeout=...,
        retry=...,
    ):  # -> Bucket:
        """Create a new bucket via a POST request.

        See [API reference docs](https://cloud.google.com/storage/docs/json_api/v1/buckets/insert) and a [code sample](https://cloud.google.com/storage/docs/samples/storage-create-bucket#storage_create_bucket-python).

        Args:
            bucket_or_name (Union[ \
                :class:`~google.cloud.storage.bucket.Bucket`, \
                 str, \
            ]):
                The bucket resource to pass or name to create.
            requester_pays (bool):
                DEPRECATED. Use Bucket().requester_pays instead.
                (Optional) Whether requester pays for API requests for
                this bucket and its blobs.
            project (str):
                (Optional) The project under which the bucket is to be created.
                If not passed, uses the project set on the client.
            user_project (str):
                (Optional) The project ID to be billed for API requests
                made via created bucket.
            location (str):
                (Optional) The location of the bucket. If not passed,
                the default location, US, will be used. If specifying a dual-region,
                `data_locations` should be set in conjunction. See:
                https://cloud.google.com/storage/docs/locations
            data_locations (list of str):
                (Optional) The list of regional locations of a custom dual-region bucket.
                Dual-regions require exactly 2 regional locations. See:
                https://cloud.google.com/storage/docs/locations
            predefined_acl (str):
                (Optional) Name of predefined ACL to apply to bucket. See:
                https://cloud.google.com/storage/docs/access-control/lists#predefined-acl
            predefined_default_object_acl (str):
                (Optional) Name of predefined ACL to apply to bucket's objects. See:
                https://cloud.google.com/storage/docs/access-control/lists#predefined-acl
            enable_object_retention (bool):
                (Optional) Whether object retention should be enabled on this bucket. See:
                https://cloud.google.com/storage/docs/object-lock
            timeout (Optional[Union[float, Tuple[float, float]]]):
                The amount of time, in seconds, to wait for the server response.

                Can also be passed as a tuple (connect_timeout, read_timeout).
                See :meth:`requests.Session.request` documentation for details.

            retry (Optional[Union[google.api_core.retry.Retry, google.cloud.storage.retry.ConditionalRetryPolicy]]):
                How to retry the RPC. A None value will disable retries.
                A google.api_core.retry.Retry value will enable retries, and the object will
                define retriable response codes and errors and configure backoff and timeout options.

                A google.cloud.storage.retry.ConditionalRetryPolicy value wraps a Retry object and
                activates it only if certain conditions are met. This class exists to provide safe defaults
                for RPC calls that are not technically safe to retry normally (due to potential data
                duplication or other side-effects) but become safe to retry if a condition such as
                if_metageneration_match is set.

                See the retry.py source code and docstrings in this package (google.cloud.storage.retry) for
                information on retry types and how to configure them.

        Returns:
            google.cloud.storage.bucket.Bucket
                The newly created bucket.

        Raises:
            google.cloud.exceptions.Conflict
                If the bucket already exists.
        """
        ...

    @create_trace_span(name="Storage.Client.downloadBlobToFile")
    def download_blob_to_file(
        self,
        blob_or_uri,
        file_obj,
        start=...,
        end=...,
        raw_download=...,
        if_etag_match=...,
        if_etag_not_match=...,
        if_generation_match=...,
        if_generation_not_match=...,
        if_metageneration_match=...,
        if_metageneration_not_match=...,
        timeout=...,
        checksum=...,
        retry=...,
    ):  # -> None:
        """Download the contents of a blob object or blob URI into a file-like object.

        See https://cloud.google.com/storage/docs/downloading-objects

        Args:
            blob_or_uri (Union[ \
            :class:`~google.cloud.storage.blob.Blob`, \
             str, \
            ]):
                The blob resource to pass or URI to download.

            file_obj (file):
                A file handle to which to write the blob's data.

            start (int):
                (Optional) The first byte in a range to be downloaded.

            end (int):
                (Optional) The last byte in a range to be downloaded.

            raw_download (bool):
                (Optional) If true, download the object without any expansion.

            if_etag_match (Union[str, Set[str]]):
                (Optional) See :ref:`using-if-etag-match`

            if_etag_not_match (Union[str, Set[str]]):
                (Optional) See :ref:`using-if-etag-not-match`

            if_generation_match (long):
                (Optional) See :ref:`using-if-generation-match`

            if_generation_not_match (long):
                (Optional) See :ref:`using-if-generation-not-match`

            if_metageneration_match (long):
                (Optional) See :ref:`using-if-metageneration-match`

            if_metageneration_not_match (long):
                (Optional) See :ref:`using-if-metageneration-not-match`

            timeout ([Union[float, Tuple[float, float]]]):
                (Optional) The amount of time, in seconds, to wait
                for the server response.  See: :ref:`configuring_timeouts`

            checksum (str):
                (Optional) The type of checksum to compute to verify the integrity
                of the object. The response headers must contain a checksum of the
                requested type. If the headers lack an appropriate checksum (for
                instance in the case of transcoded or ranged downloads where the
                remote service does not know the correct checksum, including
                downloads where chunk_size is set) an INFO-level log will be
                emitted. Supported values are "md5", "crc32c" and None. The default
                is "md5".
            retry (google.api_core.retry.Retry or google.cloud.storage.retry.ConditionalRetryPolicy)
                (Optional) How to retry the RPC. A None value will disable
                retries. A google.api_core.retry.Retry value will enable retries,
                and the object will define retriable response codes and errors and
                configure backoff and timeout options.

                A google.cloud.storage.retry.ConditionalRetryPolicy value wraps a
                Retry object and activates it only if certain conditions are met.
                This class exists to provide safe defaults for RPC calls that are
                not technically safe to retry normally (due to potential data
                duplication or other side-effects) but become safe to retry if a
                condition such as if_metageneration_match is set.

                See the retry.py source code and docstrings in this package
                (google.cloud.storage.retry) for information on retry types and how
                to configure them.

                Media operations (downloads and uploads) do not support non-default
                predicates in a Retry object. The default will always be used. Other
                configuration changes for Retry objects such as delays and deadlines
                are respected.
        """
        ...

    @create_trace_span(name="Storage.Client.listBlobs")
    def list_blobs(
        self,
        bucket_or_name,
        max_results=...,
        page_token=...,
        prefix=...,
        delimiter=...,
        start_offset=...,
        end_offset=...,
        include_trailing_delimiter=...,
        versions=...,
        projection=...,
        fields=...,
        page_size=...,
        timeout=...,
        retry=...,
        match_glob=...,
        include_folders_as_prefixes=...,
        soft_deleted=...,
    ):  # -> HTTPIterator:
        """Return an iterator used to find blobs in the bucket.

        If :attr:`user_project` is set, bills the API request to that project.

        .. note::
          List prefixes (directories) in a bucket using a prefix and delimiter.
          See a [code sample](https://cloud.google.com/storage/docs/samples/storage-list-files-with-prefix#storage_list_files_with_prefix-python)
          listing objects using a prefix filter.

        Args:
            bucket_or_name (Union[ \
                :class:`~google.cloud.storage.bucket.Bucket`, \
                 str, \
            ]):
                The bucket resource to pass or name to create.

            max_results (int):
                (Optional) The maximum number of blobs to return.

            page_token (str):
                (Optional) If present, return the next batch of blobs, using the
                value, which must correspond to the ``nextPageToken`` value
                returned in the previous response.  Deprecated: use the ``pages``
                property of the returned iterator instead of manually passing the
                token.

            prefix (str):
                (Optional) Prefix used to filter blobs.

            delimiter (str):
                (Optional) Delimiter, used with ``prefix`` to
                emulate hierarchy.

            start_offset (str):
                (Optional) Filter results to objects whose names are
                lexicographically equal to or after ``startOffset``. If
                ``endOffset`` is also set, the objects listed will have names
                between ``startOffset`` (inclusive) and ``endOffset``
                (exclusive).

            end_offset (str):
                (Optional) Filter results to objects whose names are
                lexicographically before ``endOffset``. If ``startOffset`` is
                also set, the objects listed will have names between
                ``startOffset`` (inclusive) and ``endOffset`` (exclusive).

            include_trailing_delimiter (boolean):
                (Optional) If true, objects that end in exactly one instance of
                ``delimiter`` will have their metadata included in ``items`` in
                addition to ``prefixes``.

            versions (bool):
                (Optional) Whether object versions should be returned
                as separate blobs.

            projection (str):
                (Optional) If used, must be 'full' or 'noAcl'.
                Defaults to ``'noAcl'``. Specifies the set of
                properties to return.

            fields (str):
                (Optional) Selector specifying which fields to include
                in a partial response. Must be a list of fields. For
                example to get a partial response with just the next
                page token and the name and language of each blob returned:
                ``'items(name,contentLanguage),nextPageToken'``.
                See: https://cloud.google.com/storage/docs/json_api/v1/parameters#fields

            page_size (int):
                (Optional) Maximum number of blobs to return in each page.
                Defaults to a value set by the API.

            timeout (Optional[Union[float, Tuple[float, float]]]):
                The amount of time, in seconds, to wait for the server response.

                Can also be passed as a tuple (connect_timeout, read_timeout).
                See :meth:`requests.Session.request` documentation for details.

            retry (Optional[Union[google.api_core.retry.Retry, google.cloud.storage.retry.ConditionalRetryPolicy]]):
                How to retry the RPC. A None value will disable retries.
                A google.api_core.retry.Retry value will enable retries, and the object will
                define retriable response codes and errors and configure backoff and timeout options.

                A google.cloud.storage.retry.ConditionalRetryPolicy value wraps a Retry object and
                activates it only if certain conditions are met. This class exists to provide safe defaults
                for RPC calls that are not technically safe to retry normally (due to potential data
                duplication or other side-effects) but become safe to retry if a condition such as
                if_metageneration_match is set.

                See the retry.py source code and docstrings in this package (google.cloud.storage.retry) for
                information on retry types and how to configure them.

            match_glob (str):
                (Optional) A glob pattern used to filter results (for example, foo*bar).
                The string value must be UTF-8 encoded. See:
                https://cloud.google.com/storage/docs/json_api/v1/objects/list#list-object-glob

            include_folders_as_prefixes (bool):
                (Optional) If true, includes Folders and Managed Folders in the set of
                ``prefixes`` returned by the query. Only applicable if ``delimiter`` is set to /.
                See: https://cloud.google.com/storage/docs/managed-folders

            soft_deleted (bool):
                (Optional) If true, only soft-deleted objects will be listed as distinct results in order of increasing
                generation number. This parameter can only be used successfully if the bucket has a soft delete policy.
                Note ``soft_deleted`` and ``versions`` cannot be set to True simultaneously. See:
                https://cloud.google.com/storage/docs/soft-delete

        Returns:
            Iterator of all :class:`~google.cloud.storage.blob.Blob`
            in this bucket matching the arguments. The RPC call
            returns a response when the iterator is consumed.

            As part of the response, you'll also get back an iterator.prefixes entity that lists object names
            up to and including the requested delimiter. Duplicate entries are omitted from this list.
        """
        ...

    @create_trace_span(name="Storage.Client.listBuckets")
    def list_buckets(
        self,
        max_results=...,
        page_token=...,
        prefix=...,
        projection=...,
        fields=...,
        project=...,
        page_size=...,
        timeout=...,
        retry=...,
        *,
        soft_deleted=...
    ):  # -> HTTPIterator:
        """Get all buckets in the project associated to the client.

        This will not populate the list of blobs available in each
        bucket.

        See [API reference docs](https://cloud.google.com/storage/docs/json_api/v1/buckets/list) and a [code sample](https://cloud.google.com/storage/docs/samples/storage-list-buckets#storage_list_buckets-python).

        :type max_results: int
        :param max_results: (Optional) The maximum number of buckets to return.

        :type page_token: str
        :param page_token:
            (Optional) If present, return the next batch of buckets, using the
            value, which must correspond to the ``nextPageToken`` value
            returned in the previous response.  Deprecated: use the ``pages``
            property of the returned iterator instead of manually passing the
            token.

        :type prefix: str
        :param prefix: (Optional) Filter results to buckets whose names begin
                       with this prefix.

        :type projection: str
        :param projection:
            (Optional) Specifies the set of properties to return. If used, must
            be 'full' or 'noAcl'. Defaults to 'noAcl'.

        :type fields: str
        :param fields:
            (Optional) Selector specifying which fields to include in a partial
            response. Must be a list of fields. For example to get a partial
            response with just the next page token and the language of each
            bucket returned: 'items/id,nextPageToken'

        :type project: str
        :param project: (Optional) The project whose buckets are to be listed.
                        If not passed, uses the project set on the client.

        :type page_size: int
        :param page_size: (Optional) Maximum number of buckets to return in each page.
            Defaults to a value set by the API.

        :type timeout: float or tuple
        :param timeout:
            (Optional) The amount of time, in seconds, to wait
            for the server response.  See: :ref:`configuring_timeouts`

        :type retry: google.api_core.retry.Retry or google.cloud.storage.retry.ConditionalRetryPolicy
        :param retry:
            (Optional) How to retry the RPC. See: :ref:`configuring_retries`

        :type soft_deleted: bool
        :param soft_deleted:
            (Optional) If true, only soft-deleted buckets will be listed as distinct results in order of increasing
            generation number. This parameter can only be used successfully if the bucket has a soft delete policy.
            See: https://cloud.google.com/storage/docs/soft-delete

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :raises ValueError: if both ``project`` is ``None`` and the client's
                            project is also ``None``.
        :returns: Iterator of all :class:`~google.cloud.storage.bucket.Bucket`
                  belonging to this project.
        """
        ...

    def restore_bucket(
        self,
        bucket_name,
        generation,
        projection=...,
        if_metageneration_match=...,
        if_metageneration_not_match=...,
        timeout=...,
        retry=...,
    ):  # -> Bucket:
        """Restores a soft-deleted bucket.

        :type bucket_name: str
        :param bucket_name: The name of the bucket to be restored.

        :type generation: int
        :param generation: Selects the specific revision of the bucket.

        :type projection: str
        :param projection:
            (Optional) Specifies the set of properties to return. If used, must
            be 'full' or 'noAcl'. Defaults to 'noAcl'.

        if_metageneration_match (Optional[int]):
            Make the operation conditional on whether the
            blob's current metageneration matches the given value.

        if_metageneration_not_match (Optional[int]):
            Make the operation conditional on whether the blob's
            current metageneration does not match the given value.

        :type timeout: float or tuple
        :param timeout:
            (Optional) The amount of time, in seconds, to wait
            for the server response.  See: :ref:`configuring_timeouts`

        :type retry: google.api_core.retry.Retry or google.cloud.storage.retry.ConditionalRetryPolicy
        :param retry:
            (Optional) How to retry the RPC.

            Users can configure non-default retry behavior. A ``None`` value will
            disable retries. See [Configuring Retries](https://cloud.google.com/python/docs/reference/storage/latest/retry_timeout).

        :rtype: :class:`google.cloud.storage.bucket.Bucket`
        :returns: The restored Bucket.
        """
        ...

    @create_trace_span(name="Storage.Client.createHmacKey")
    def create_hmac_key(
        self,
        service_account_email,
        project_id=...,
        user_project=...,
        timeout=...,
        retry=...,
    ):  # -> tuple[HMACKeyMetadata, Any]:
        """Create an HMAC key for a service account.

        :type service_account_email: str
        :param service_account_email: e-mail address of the service account

        :type project_id: str
        :param project_id: (Optional) Explicit project ID for the key.
            Defaults to the client's project.

        :type user_project: str
        :param user_project: (Optional) This parameter is currently ignored.

        :type timeout: float or tuple
        :param timeout:
            (Optional) The amount of time, in seconds, to wait
            for the server response.  See: :ref:`configuring_timeouts`

        :type retry: google.api_core.retry.Retry or google.cloud.storage.retry.ConditionalRetryPolicy
        :param retry: (Optional) How to retry the RPC. A None value will disable retries.
            A google.api_core.retry.Retry value will enable retries, and the object will
            define retriable response codes and errors and configure backoff and timeout options.

            A google.cloud.storage.retry.ConditionalRetryPolicy value wraps a Retry object and
            activates it only if certain conditions are met. This class exists to provide safe defaults
            for RPC calls that are not technically safe to retry normally (due to potential data
            duplication or other side-effects) but become safe to retry if a condition such as
            if_metageneration_match is set.

            See the retry.py source code and docstrings in this package (google.cloud.storage.retry) for
            information on retry types and how to configure them.

        :rtype:
            Tuple[:class:`~google.cloud.storage.hmac_key.HMACKeyMetadata`, str]
        :returns: metadata for the created key, plus the bytes of the key's secret, which is an 40-character base64-encoded string.
        """
        ...

    @create_trace_span(name="Storage.Client.listHmacKeys")
    def list_hmac_keys(
        self,
        max_results=...,
        service_account_email=...,
        show_deleted_keys=...,
        project_id=...,
        user_project=...,
        timeout=...,
        retry=...,
    ):  # -> HTTPIterator:
        """List HMAC keys for a project.

        :type max_results: int
        :param max_results:
            (Optional) Max number of keys to return in a given page.

        :type service_account_email: str
        :param service_account_email:
            (Optional) Limit keys to those created by the given service account.

        :type show_deleted_keys: bool
        :param show_deleted_keys:
            (Optional) Included deleted keys in the list. Default is to
            exclude them.

        :type project_id: str
        :param project_id: (Optional) Explicit project ID for the key.
            Defaults to the client's project.

        :type user_project: str
        :param user_project: (Optional) This parameter is currently ignored.

        :type timeout: float or tuple
        :param timeout:
            (Optional) The amount of time, in seconds, to wait
            for the server response.  See: :ref:`configuring_timeouts`

        :type retry: google.api_core.retry.Retry or google.cloud.storage.retry.ConditionalRetryPolicy
        :param retry:
            (Optional) How to retry the RPC. See: :ref:`configuring_retries`

        :rtype:
            Tuple[:class:`~google.cloud.storage.hmac_key.HMACKeyMetadata`, str]
        :returns: metadata for the created key, plus the bytes of the key's secret, which is an 40-character base64-encoded string.
        """
        ...

    @create_trace_span(name="Storage.Client.getHmacKeyMetadata")
    def get_hmac_key_metadata(
        self, access_id, project_id=..., user_project=..., timeout=...
    ):  # -> HMACKeyMetadata:
        """Return a metadata instance for the given HMAC key.

        :type access_id: str
        :param access_id: Unique ID of an existing key.

        :type project_id: str
        :param project_id: (Optional) Project ID of an existing key.
            Defaults to client's project.

        :type timeout: float or tuple
        :param timeout:
            (Optional) The amount of time, in seconds, to wait
            for the server response.  See: :ref:`configuring_timeouts`

        :type user_project: str
        :param user_project: (Optional) This parameter is currently ignored.
        """
        ...

    def generate_signed_post_policy_v4(
        self,
        bucket_name,
        blob_name,
        expiration,
        conditions=...,
        fields=...,
        credentials=...,
        virtual_hosted_style=...,
        bucket_bound_hostname=...,
        scheme=...,
        service_account_email=...,
        access_token=...,
    ):  # -> dict[str, str | dict[Any, Any]]:
        """Generate a V4 signed policy object. Generated policy object allows user to upload objects with a POST request.

        .. note::

            Assumes ``credentials`` implements the
            :class:`google.auth.credentials.Signing` interface. Also assumes
            ``credentials`` has a ``service_account_email`` property which
            identifies the credentials.

        See a [code sample](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_generate_signed_post_policy_v4.py).

        :type bucket_name: str
        :param bucket_name: Bucket name.

        :type blob_name: str
        :param blob_name: Object name.

        :type expiration: Union[Integer, datetime.datetime, datetime.timedelta]
        :param expiration: Policy expiration time. If a ``datetime`` instance is
                           passed without an explicit ``tzinfo`` set,  it will be
                           assumed to be ``UTC``.

        :type conditions: list
        :param conditions: (Optional) List of POST policy conditions, which are
                           used to restrict what is allowed in the request.

        :type fields: dict
        :param fields: (Optional) Additional elements to include into request.

        :type credentials: :class:`google.auth.credentials.Signing`
        :param credentials: (Optional) Credentials object with an associated private
                            key to sign text.

        :type virtual_hosted_style: bool
        :param virtual_hosted_style:
            (Optional) If True, construct the URL relative to the bucket
            virtual hostname, e.g., '<bucket-name>.storage.googleapis.com'.
            Incompatible with bucket_bound_hostname.

        :type bucket_bound_hostname: str
        :param bucket_bound_hostname:
            (Optional) If passed, construct the URL relative to the bucket-bound hostname.
            Value can be bare or with a scheme, e.g., 'example.com' or 'http://example.com'.
            Incompatible with virtual_hosted_style.
            See: https://cloud.google.com/storage/docs/request-endpoints#cname

        :type scheme: str
        :param scheme:
            (Optional) If ``bucket_bound_hostname`` is passed as a bare hostname, use
            this value as a scheme. ``https`` will work only when using a CDN.
            Defaults to ``"http"``.

        :type service_account_email: str
        :param service_account_email: (Optional) E-mail address of the service account.

        :type access_token: str
        :param access_token: (Optional) Access token for a service account.

        :raises: :exc:`ValueError` when mutually exclusive arguments are used.

        :rtype: dict
        :returns: Signed POST policy.
        """
        ...
