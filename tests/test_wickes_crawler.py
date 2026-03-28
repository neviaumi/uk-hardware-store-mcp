import pytest

from app.crawlers.wickes_crawler import wickes_crawler
from tests.crawler import TEST_SEARCH_KEYWORD
from tests.mock_server import mock_response_data

pytestmark = pytest.mark.anyio


async def test_product_search(mock_server):
    mock_server.expect_request("/wickes/search").respond_with_data(
        mock_response_data("product_search_wickes.html")
    )
    results = await wickes_crawler.product_search(TEST_SEARCH_KEYWORD)
    assert isinstance(results, list)
    assert len(results) > 0
    for item in results:
        assert item["title"]
        assert item["price"]
        assert item["url"].startswith(mock_server.url_for("/wickes"))


async def test_product_detail(mock_server):
    path = "/wickes/Rawlplug-RBL2-RAWLBOLT-with-Loose-Bolt---M6-x-70mm/p/300702"
    mock_server.expect_request(path).respond_with_data(
        mock_response_data("product_detail_wickes.html")
    )
    url = mock_server.url_for(path)
    result = await wickes_crawler.product_detail(url)
    assert result["title"]
    assert result["price"]
    assert result["description"]
    assert result["detail"]
    # Check if promo exists or not based on captured HTML (usually Rawlbolts don't have promos in this context)
    assert "promo" in result
