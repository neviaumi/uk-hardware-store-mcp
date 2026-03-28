import pytest

from app.crawlers.diy_dot_com_crawler import diy_dot_com_crawler
from tests.crawler import TEST_SEARCH_KEYWORD
from tests.mock_server import mock_response_data

pytestmark = pytest.mark.anyio


async def test_product_search(mock_server):
    mock_server.expect_request("/b&q/search").respond_with_data(
        mock_response_data("product_search_diy_dot_com.html")
    )
    results = await diy_dot_com_crawler.product_search(TEST_SEARCH_KEYWORD)
    assert isinstance(results, list)
    assert len(results) > 0
    for item in results:
        assert item["title"]
        assert item["price"]
        assert item["url"].startswith(mock_server.url_for("/b&q/"))


async def test_product_detail(mock_server):
    path = "/b&q/departments/m8-x-60mm-hex-set-screws-fully-threaded-hex-bolt-stainless-steel-a2-din-933-pack-of-20/5056747705963_BQ.prd"
    mock_server.expect_request(path).respond_with_data(
        mock_response_data("product_detail_diy_dot_com.html")
    )
    url = mock_server.url_for(path)
    result = await diy_dot_com_crawler.product_detail(url)
    assert result["title"]
    assert result["price"]
    assert result["detail"]
    assert result["promo"] is None
