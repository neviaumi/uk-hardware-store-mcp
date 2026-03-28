import pytest

from .mock_server import mock_server

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


__all__ = ["mock_server", "anyio_backend"]
