import pytest

from app.crawlers.the_range_crawler import the_range_crawler
from tests.crawler import TEST_SEARCH_KEYWORD
from tests.mock_server import mock_response_data

pytestmark = pytest.mark.anyio


async def test_product_search(mock_server):
    mock_server.expect_request("/the-range/search").respond_with_data(
        mock_response_data("product_search_the_range.html")
    )
    results = await the_range_crawler.product_search(TEST_SEARCH_KEYWORD)
    assert isinstance(results, list)
    assert len(results) == 3
    first_item = results[0]
    assert first_item["title"] == "Hex Bolt Nut and Washer"
    assert first_item["price"] == "£1.99"
    assert "hex-bolt-nut-and-washer" in first_item["url"]


async def test_product_detail(mock_server):
    path = "/the-range/garden/garden-machinery-and-power-tools/pressure-washers/saber-2000w-pressure-washer"
    mock_server.expect_request(path).respond_with_data(
        mock_response_data("product_detail_the_range.html")
    )
    url = mock_server.url_for(path)
    result = await the_range_crawler.product_detail(url)
    assert result["title"] == "Saber 2000W Pressure Washer - Black and Orange"
    assert result["price"] == "£99.99"
    assert "160 bar" in result["detail"]
    assert "Save £40.00" in result["promo"]
