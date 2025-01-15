import typing
from io import BytesIO
from logging import getLogger
from typing import IO
from urllib.parse import urlparse

import polars as pl
from pandera.polars import DataFrameModel
from pandera.typing.polars import DataFrame
from pandera.typing.polars import LazyFrame

try:
    # make using google storage optional
    import google.cloud.storage as storage
except ImportError:  # pragma: no cover
    pass

import httpx
from tenacity import retry
from tenacity import stop_after_attempt


def open_gcs_uri(uri: str) -> IO[bytes]:
    """Open Google Cloud Storage uri's (starting with gs://)"""
    logger = getLogger(__name__)
    logger.info("Downloading file from uri %s", uri)
    client = storage.Client()  # type:ignore[reportPossiblyUnboundVariable]
    parsed_uri = urlparse(uri)
    bucket_name = parsed_uri.netloc
    fname = parsed_uri.path
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(fname)
    file = BytesIO()
    blob.download_to_file(file_obj=file)
    file.seek(0)
    return file


@retry(stop=stop_after_attempt(3))
def open_http_uri(uri: str) -> IO[bytes]:
    """Open HTTP(S) uri's"""
    logger = getLogger(__name__)
    logger.info("Downloading file from uri %s", uri)
    resp = httpx.get(uri, timeout=60)
    resp.raise_for_status()
    file = BytesIO(resp.read())
    file.seek(0)
    return file


def open_uri(uri: str, params: dict[str, str]) -> IO[bytes] | None:
    """
    Open a file from a supported uri.
    Currently supported are:
        gs:// Google Cloud Storage files
        http(s):// Uses httpx to download the file
    """
    uri = uri.format(**params)
    parsed_uri = urlparse(uri)
    match parsed_uri.scheme:
        case "gs":
            return open_gcs_uri(uri)
        case "http":
            return open_http_uri(uri)
        case "https":
            return open_http_uri(uri)
        case _:
            raise NotImplementedError(f"Scheme {parsed_uri.scheme} is not supported.")


T_PANDERA_MODEL = typing.TypeVar("T_PANDERA_MODEL", bound=DataFrameModel)


def get_profile_csv_data(
    uri: str, params: dict[str, str], model: type[T_PANDERA_MODEL]
) -> DataFrame[T_PANDERA_MODEL]:
    """
    Open a csv file from a uri with a profile that matches the pandera `model`.
    """
    data_file = open_uri(uri, params)
    if data_file is None:
        raise ValueError(f"No data file found for uri {uri}")
    data = pl.read_csv(data_file).lazy()
    # unfortunately pandera specifies the return type of validate as DataFrameBase instead of LazyFrame or DataFrame
    validated_data = typing.cast(LazyFrame[model], model.validate(data))
    return typing.cast(DataFrame[model], validated_data.collect())
