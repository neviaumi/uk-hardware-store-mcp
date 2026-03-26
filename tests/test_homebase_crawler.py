import pytest
from app.crawlers.homebase_crawler import homebase_crawler

pytestmark = pytest.mark.anyio


async def test_product_search():
    results = await homebase_crawler.product_search("m8 hex bolt")
    assert isinstance(results, list)
    assert len(results) > 0
    for item in results:
        assert item["title"]
        assert item["price"]
        assert item["url"].startswith("https://www.homebase.co.uk")


async def test_product_detail():
    url = (
        "https://www.homebase.co.uk/en-uk/galvanised-netting-staple-20mm-50g/p/0160968"
    )
    result = await homebase_crawler.product_detail(url)
    assert result["title"]
    assert result["price"]
    assert result["detail"]
    assert "3 For 2 Ironmongery" in result["promo"]
