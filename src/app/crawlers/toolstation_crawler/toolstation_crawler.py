from typing import TypedDict
import urllib.parse
import uuid

from crawlee import Request
from crawlee.crawlers import HttpCrawlingContext
from app.crawlers.base.crawlers import router, run_crawler_with_result

import json

TOOLSTATION_API = "https://www.toolstation.com/api"


@router.handler(label="toolstation product search")
async def toolstation_product_search_handler(context: HttpCrawlingContext) -> None:
    body = json.loads(await context.http_response.read())

    def _extract_product(product):
        return {
            "title": product["title"].strip(),
            "price": f"£{product['price']}",
            "url": product["url"].strip(),
            "promo": product["weboverlaytext"]
            if "for" in product.get("weboverlaytext", "")
            else None,
        }

    for product in body["response"]["docs"]:
        await context.push_data(
            _extract_product(product), dataset_name=context.request.unique_key
        )


class ProductSearchResponse(TypedDict):
    title: str
    price: str
    url: str
    promo: str | None


async def product_search(keyword: str) -> list[ProductSearchResponse]:
    query = urllib.parse.urlencode(
        {
            "request_type": "search",
            "q": keyword,
            "start": "0",
            "search_type": "keyword",
            "skipCache": "true",
        }
    )
    request = Request.from_url(
        f"{TOOLSTATION_API}/search/crs?{query}",
        label="toolstation product search",
        unique_key=str(uuid.uuid4()),
    )
    return await run_crawler_with_result(request, "api")
