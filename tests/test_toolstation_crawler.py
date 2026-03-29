import pytest

from app.crawlers import toolstation_crawler
from tests.crawler import TEST_SEARCH_KEYWORD
from tests.mock_server import mock_response_data, mock_response_json

pytestmark = pytest.mark.anyio


async def test_product_detail(mock_server):
    # Mock product detail for Screwfix
    path = "/toolstation/wessex-led-gu10-dimmable-bulbs/pAB374"
    mock_server.expect_request(path).respond_with_data(
        mock_response_data("product_detail_toolstation.html")
    )

    url = mock_server.url_for(path)
    result = await toolstation_crawler.product_detail(url)

    assert result["title"] == "Wessex LED GU10 Dimmable Bulbs 3W Cool White 345lm"
    assert result["price"] == "£12.55"
    assert (
        "long-lasting performance and reliability with effective illumination."
        in result["description"]
    )
    assert "Wessex Electrical" in result["detail"]
    assert "GU10" in result["detail"]
    assert result["promo"] == "15% Off"


async def test_product_search(mock_server):
    # Mock search results for Screwfix
    mock_server.expect_request("/toolstation/api/search/crs").respond_with_json(
        mock_response_json("product_search_toolstation.json")
    )

    results = await toolstation_crawler.product_search(TEST_SEARCH_KEYWORD)

    assert isinstance(results, list)
    assert len(results) == 24

    # Verify first product
    first_item = results[0]
    assert first_item["title"] == "Stainless Steel Socket Button Screw M6 x 20mm"
    assert first_item["price"] == "£5.58"
    # The URL is transformed to include the mock server's base URL
    assert first_item["url"].startswith(mock_server.url_for("/toolstation"))
    assert first_item["promo"] is None
