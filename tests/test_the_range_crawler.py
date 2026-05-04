import pytest

from app.crawlers.the_range_crawler import the_range_crawler
from tests import skip_if_ci
from tests.crawler import TEST_SEARCH_KEYWORD

pytestmark = pytest.mark.anyio


@skip_if_ci
async def test_product_search():
    results = await the_range_crawler.product_search(TEST_SEARCH_KEYWORD)
    assert isinstance(results, list)
    assert len(results) > 0
    first_item = results[0]
    assert first_item.title
    assert first_item.price
    assert first_item.url
    assert first_item.source == "The Range"


@skip_if_ci
async def test_product_detail():
    url = "https://www.therange.co.uk/garden/garden-machinery-and-power-tools/pressure-washers/saber-2000w-pressure-washer"

    result = await the_range_crawler.product_detail(url)
    assert result.title
    assert result.price
    assert isinstance(result.detail, str)
    assert result.source == "The Range"
