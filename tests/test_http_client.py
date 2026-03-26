import app.crawlers.http_client as http_client

import pytest

pytestmark = pytest.mark.anyio


async def test_http_client_creation():
    async with http_client.create_client() as client:
        response = await client.get("https://mpf34eb04c75c941ceaf.free.beeceptor.com")
        assert response.status_code == 200
