import pytest

from app.crawlers.screwfix_crawler import screwfix_crawler
from tests.crawler import TEST_SEARCH_KEYWORD
from tests.mock_server import mock_response_data

pytestmark = pytest.mark.anyio


async def test_product_search(mock_server):
    # Mock search results for Screwfix
    mock_server.expect_request("/screwfix/search").respond_with_data(
        mock_response_data("product_search_screwfix.html")
    )

    results = await screwfix_crawler.product_search(TEST_SEARCH_KEYWORD)

    assert isinstance(results, list)
    assert len(results) == 15

    # Verify first product
    first_item = results[0]
    assert (
        first_item["title"]
        == "Easydrive Hex Bolt Thread Cutting Coach Screws 6mm x 50mm 10 Pack"
    )
    assert first_item["price"] == "£5.29"
    # The URL is transformed to include the mock server's base URL
    assert first_item["url"].startswith(mock_server.url_for("/screwfix"))
    assert "Deep Coarse Thread" in first_item["description"]
    assert first_item["promo"] == "Buy 5+ Save 10% - View Offer"


async def test_product_detail(mock_server):
    # Mock product detail for Screwfix
    path = "/screwfix/p/m6-bolt/12345"
    mock_server.expect_request(path).respond_with_data(
        mock_response_data("product_detail_screwfix.html")
    )

    url = mock_server.url_for(path)
    result = await screwfix_crawler.product_detail(url)

    assert (
        result["title"]
        == "Easydrive Hex Bolt Thread Cutting Coach Screws 6mm x 50mm 10 Pack"
    )
    assert result["price"] == "£5.29"
    assert "Hex head" in result["description"]
    assert "A2 Stainless Steel" in result["detail"]
    assert "Partially Threaded" in result["detail"]
    assert result["promo"] == "Buy 5+ Save 10%"
