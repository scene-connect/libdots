from contextlib import nullcontext
from io import BytesIO
from typing import IO
from unittest.mock import MagicMock

import pandera.polars as pa
import polars as pd
import pytest
import respx
import tenacity
from httpx import Response
from pytest_mock import MockFixture

from libdots import profiles


@pytest.mark.parametrize(
    "uri,function,params,expected_uri,expected_error",
    [
        (
            "gs://some-bucket/some-file.csv",
            "open_gcs_uri",
            {},
            "gs://some-bucket/some-file.csv",
            None,
        ),
        (
            "https://some-bucket/some-file.csv",
            "open_http_uri",
            {},
            "https://some-bucket/some-file.csv",
            None,
        ),
        (
            "https://some-bucket/some-file.csv",
            "open_http_uri",
            {},
            "https://some-bucket/some-file.csv",
            None,
        ),
        (
            "http://some-bucket/some{test}-file.csv",
            "open_http_uri",
            {"test": "-foobar"},
            "http://some-bucket/some-foobar-file.csv",
            None,
        ),
        (
            "unknown://some-bucket/some-file.csv",
            "open_http_uri",
            {},
            "",
            NotImplementedError,
        ),
        ("invalid", "open_http_uri", {}, "", NotImplementedError),
    ],
)
def test_open_uri(
    uri: str,
    function: str,
    params: dict[str, str],
    expected_uri: str,
    expected_error: type[Exception] | None,
    mocker: MockFixture,
):
    """Tests that open_uri accepts various uri's and calls the right function depending on the scheme."""
    data = BytesIO()
    mocked_function = mocker.patch.object(profiles, function, return_value=data)
    if expected_error is None:
        ctx = nullcontext()  # no error so empty context
    else:
        ctx = pytest.raises(expected_error)
    with ctx:
        assert profiles.open_uri(uri, params) == data
        mocked_function.assert_called_once_with(expected_uri)


def test_open_gcs_uri(
    mocker: MockFixture,
):
    """Test that opening a gcs_uri uses the google cloud storage libary"""
    bucket_name = "test_bucket"
    file_name = "/a/b/c.csv"
    uri = f"gs://{bucket_name}/{file_name.lstrip('/')}"
    expected_data = b"test"
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_bucket.blob.return_value = mock_blob

    def mock_write(file_obj: IO[bytes]):
        file_obj.write(expected_data)

    mock_blob.download_to_file.side_effect = mock_write
    mock_storage = mocker.patch.object(
        profiles.storage, "Client", return_value=mock_client
    )
    mock_client.get_bucket.return_value = mock_bucket
    data = profiles.open_gcs_uri(uri)
    assert data.read() == expected_data
    mock_storage.assert_called_once_with()
    mock_client.get_bucket.assert_called_once_with(bucket_name)
    mock_bucket.blob.assert_called_once_with(file_name.lstrip("/"))
    mock_blob.download_to_file.assert_called_once()


def test_open_https_uri(respx_mock: respx.MockRouter):
    """Test that httpx is used to download http(s) files."""
    uri = "https://test.com/a/b/c.csv"
    mock_route = respx_mock.get(uri)
    data = BytesIO(b"test")
    mock_route.mock(return_value=Response(status_code=200, content=data))
    actual_data = profiles.open_http_uri(uri)
    assert actual_data.read() == data.getvalue()
    assert mock_route.called
    assert mock_route.call_count == 1


def test_open_https_uri_retry_errors(respx_mock: respx.MockRouter):
    """Test that httpx is used to download http(s) files."""
    uri = "https://test.com/a/b/c.csv"
    mock_route = respx_mock.get(uri)
    mock_route.mock(return_value=Response(status_code=404))
    with pytest.raises(tenacity.RetryError):
        profiles.open_http_uri(uri)
    assert mock_route.called
    assert mock_route.call_count == 3


def test_get_profile_csv_data(
    mocker: MockFixture,
):
    """Test that get_profile_data gets the file in the uri, and validates the resulting csv correctly."""
    raw_data = pd.DataFrame({"id": [1, 2], "cola": ["test1", "test2"]})
    data = BytesIO(raw_data.write_csv().encode("utf-8"))
    mock_open_uri = mocker.patch.object(profiles, "open_uri", return_value=data)
    uri = "https://test.com/a/b/c.csv"

    class TestModel(pa.DataFrameModel):
        id: int
        cola: str

    params: dict[str, str] = {}
    assert profiles.get_profile_csv_data(uri, params, TestModel).equals(raw_data)
    mock_open_uri.assert_called_once_with(uri, params)


def test_get_profile_no_csv_data(
    mocker: MockFixture,
):
    """Test that get_profile_data gets the file in the uri, and validates the resulting csv correctly."""
    mock_open_uri = mocker.patch.object(profiles, "open_uri", return_value=None)
    uri = "https://test.com/a/b/c.csv"

    class TestModel(pa.DataFrameModel):
        id: int
        cola: str

    params: dict[str, str] = {}
    with pytest.raises(ValueError, match=f"No data file found for uri {uri}"):
        profiles.get_profile_csv_data(uri, params, TestModel)
    mock_open_uri.assert_called_once_with(uri, params)


def test_get_profile_invalid_csv_data(
    mocker: MockFixture,
):
    """Test that get_profile_data gets the file in the uri, and validates the resulting csv correctly."""
    raw_data = pd.DataFrame({"cola": ["test1", "test2"]})
    data = BytesIO(raw_data.write_csv().encode("utf-8"))
    mock_open_uri = mocker.patch.object(profiles, "open_uri", return_value=data)
    uri = "https://test.com/a/b/c.csv"

    class TestModel(pa.DataFrameModel):
        id: int
        cola: str

    params: dict[str, str] = {}
    with pytest.raises(pa.errors.SchemaError, match="column 'id' not in dataframe"):
        profiles.get_profile_csv_data(uri, params, TestModel)
    mock_open_uri.assert_called_once_with(uri, params)
