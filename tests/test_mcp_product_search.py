import json

import pytest
from mcp.client.session import ClientSession
from mcp.client.stdio import (
    StdioServerParameters,
    get_default_environment,
    stdio_client,
)

from app.mcp_server import Provider
from tests import skip_if_ci
from tests.crawler import TEST_SEARCH_KEYWORD

pytestmark = pytest.mark.anyio


@pytest.fixture
def mcp_server_config():
    with open("mcp.json") as f:
        yield json.load(f)["mcpServers"]


@pytest.fixture
async def mcp_client_session(mcp_server_config):
    env = get_default_environment()
    server_params = StdioServerParameters(
        command=mcp_server_config["test"]["command"],
        args=mcp_server_config["test"]["args"],
        env=env,
    )
    async with stdio_client(server_params) as (read_stream, write_stream):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            yield session


@pytest.mark.parametrize("provider", list(Provider))
@skip_if_ci
async def test_search_products(mcp_client_session, provider):
    """Test the unified search_products tool across all providers."""
    # Call the search_products tool with the ProductsSearchRequest payload
    tool_result = await mcp_client_session.call_tool(
        "search_products",
        {"request": {"keyword": TEST_SEARCH_KEYWORD, "provider": provider.value}},
    )

    assert tool_result.isError is False, f"Tool call for {provider} should not error"
    response = tool_result.structuredContent.get("result", [])
    assert len(response) > 0, f"Tool call response for {provider} should not be empty"

    # Check that each product has expected fields
    for product in response:
        assert "title" in product
        assert "price" in product
        assert "url" in product
