import app.crawlers.diy_dot_com_crawler as diy_dot_com_crawler

import pytest

pytestmark = pytest.mark.anyio


async def test_product_detail():
    response = await diy_dot_com_crawler.product_detail(
        "https://www.diy.com/departments/m6-6mm-x-6mm-pack-of-50-din-933-hexagon-head-bolts-high-tensile-steel-grade-8-8-zinc-m06a/5059629684691_BQ.prd"
    )
    assert "style" not in response["detail"]
    assert "class" not in response["detail"]
