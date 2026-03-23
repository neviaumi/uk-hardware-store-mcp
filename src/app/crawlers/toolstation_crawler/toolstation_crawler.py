from typing import TypedDict
import urllib.parse
import uuid

from crawlee.crawlers import HttpCrawler
from crawlee.http_clients import HttpxHttpClient
from crawlee import Request
from crawlee.crawlers import HttpCrawlingContext
from crawlee.router import Router
from crawlee.storages import Dataset

import json

router = Router[HttpCrawlingContext]()
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
        f"{TOOLSTATION_API}/search/crs?{query}", label="toolstation product search", unique_key=str(uuid.uuid4())
    )
    dataset = await Dataset.open(name=request.unique_key)
    crawler = HttpCrawler(
        configure_logging=False, request_handler=router, http_client=HttpxHttpClient()
    )

    await crawler.run([request])
    result = [item for item in (await dataset.get_data()).items]
    crawler.stop()
    await dataset.drop()
    return result
