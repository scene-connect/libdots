#  This work is based on original code developed and copyrighted by TNO 2023
#  and further developed and copyrighted by Scene Ltd in 2025.
#  Subsequent contributions are licensed to you by the developers of such code and are
#  made available under one or several contributor license agreements.
#
#  This work is licensed to you under the Apache License, Version 2.0.
#  You may obtain a copy of the license at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#      TNO         - Initial implementation of the dots calculation-service-generator
#      Scene Ltd   - Development of libdots
#  Manager:
#      Scene Ltd

"""
This module contains convenience functions to load static profiles from online sources.
Static profiles can be defined using the ESDL URIProfile block that points to a file.
These can be read by id in the calculation service, and the files in this module can be
used to read them.

For reading and validating csv files, `Pandera <https://pandera.readthedocs.io/en/latest/polars.html>`_
and `Polars <https://docs.pola.rs/user-guide/migration/pandas/>`_ are used.

"""
import typing
from io import BytesIO
from logging import getLogger
from typing import IO
from urllib.parse import urlparse

import google.cloud.storage as storage
import httpx
import polars as pl
from pandera.polars import DataFrameModel
from pandera.typing import polars as pa
from tenacity import retry
from tenacity import stop_after_attempt


def open_gcs_uri(uri: str) -> IO[bytes]:
    """Open Google Cloud Storage uri's (starting with gs://)"""
    logger = getLogger(__name__)
    logger.info("Downloading file from uri %s", uri)
    client = storage.Client()
    parsed_uri = urlparse(uri)
    bucket_name = parsed_uri.netloc
    fname = parsed_uri.path.lstrip("/")
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
    Open a file from a supported URI. Optionally the uri can contain
    python string formatting parameters to parametrize the uri.

    :param uri: The uri to read.
    :param params: A dictionary containing python string formatting values
        used in uri.

    Currently supported are:

        * gs:// Google Cloud Storage files
        * http(s):// Uses httpx to download the file

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
    uri: str,
    params: dict[str, str],
    model: type[T_PANDERA_MODEL],
    sort_by: str | list[str] | None = None,
) -> pa.DataFrame[T_PANDERA_MODEL]:
    """
    Open a csv file from a uri with a profile that matches the pandera `model`.
    :param uri: The uri sent to :py:func:`open_uri`
    :param params: The params sent to :py:func:`open_uri`
    :param sort_by: A string of list of strings of columns to sort the file by.

    .. code-block:: python

        from typing import Annotated

        import polars as pl

        # due to https://github.com/unionai-oss/pandera/issues/1899
        from pandera import Field  # pyright: ignore [reportUnknownVariableType]
        from pandera.polars import DataFrameModel
        from pandera.typing import Series


        from libdots.profiles import get_profile_csv_data


        class EnergyPriceProfile(DataFrameModel):
            datetime: Series[Annotated[pl.Datetime, "ns", "UTC"]] = Field(coerce=True)
            price: float = Field(coerce=True)


        energy_price_profile = get_profile_csv_data("https://example.com/my_file.csv", {}, EnergyPriceProfile)
    """
    data_file = open_uri(uri, params)
    if data_file is None:
        raise ValueError(f"No data file found for uri {uri}")
    data = pl.read_csv(data_file, try_parse_dates=True).lazy()
    if sort_by is not None:
        data = data.sort(by=sort_by)
    # instantiating also validates in pandera
    return pa.DataFrame[model](data.collect())
