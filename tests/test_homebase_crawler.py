import pytest

from app.crawlers.homebase_crawler import homebase_crawler
from tests.crawler import TEST_SEARCH_KEYWORD
from tests.mock_server import mock_response_data

pytestmark = pytest.mark.anyio


async def test_product_search(mock_server):
    mock_server.expect_request("/homebase/en-uk/search").respond_with_data(
        mock_response_data("product_search_homebase.html")
    )
    results = await homebase_crawler.product_search(TEST_SEARCH_KEYWORD)
    assert isinstance(results, list)
    assert len(results) > 0
    for item in results:
        assert item["title"]
        assert item["price"]
        assert item["url"].startswith(mock_server.url_for("/homebase/en-uk"))


async def test_product_detail(mock_server):
    path = "/homebase/en-uk/zinc-plated-hex-bolt-nut-m8-x-100mm-4-pack/p/0507028"
    mock_server.expect_request(path).respond_with_data(
        mock_response_data("product_detail_homebase.html")
    )
    url = mock_server.url_for(path)
    result = await homebase_crawler.product_detail(url)
    assert result["title"]
    assert result["price"]
    assert result["detail"]
    assert "3 For 2 Ironmongery" in result["promo"]
