from logging import Logger
from typing import cast
from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from zuos_python_package_template import main


def test_hello(
    mocker: MockerFixture,
):
    """That that hello prints a greeting."""
    defaultLogger = cast(Logger, MagicMock())
    defaultLogger.debug = MagicMock()
    mock_get_logger = mocker.patch.object(main.logging, "getLogger")

    mock_get_logger.return_value = defaultLogger

    main.hello("Howard")
    mock_get_logger.assert_called_once()
    defaultLogger.debug.assert_called_once_with(
        "Hi Howard! May you live long and prosper 🖖"
    )
