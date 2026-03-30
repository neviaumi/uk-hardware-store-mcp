import urllib.parse
from typing import TypedDict

from parsel import Selector

import app.config as config
import app.crawlers.http_client as http_client
from app.crawlers.utils import clean_html, clean_text


class ProductDetailResponse(TypedDict):
    title: str
    price: str
    detail: str
    promo: str | None


async def product_detail(url: str) -> ProductDetailResponse:
    async with http_client.create_client() as client:
        response = await client.get(url)

    selector = Selector(text=response.text)

    # Title is in h1#product-dyn-title
    title = selector.css("h1#product-dyn-title::text").get() or ""
    # Price for detail is in div#min_price
    price = selector.css("#product-dyn-price #min_price::text").get() or ""

    promo_node = selector.css("#product-price-saving")
    promo_text = clean_text(promo_node.css("*::text").getall()) if promo_node else None

    desc_nodes = selector.css("#product-dyn-desc, #product-specification")
    detail_html = " ".join(desc_nodes.getall()) if desc_nodes else ""

    return {
        "title": title.strip(),
        "price": price,
        "detail": clean_html(detail_html),
        "promo": promo_text,
    }


class ProductSearchResponse(TypedDict):
    title: str
    price: str
    url: str


async def product_search(keyword: str) -> list[ProductSearchResponse]:
    query = urllib.parse.urlencode(
        {
            "q": keyword,
            "sort": "relevance",
            "attributes.Available_To_Order": "TRUE",
            "page": "1",
        }
    )
    url = f"{config.THE_RANGE_URL}/search?{query}"

    async with http_client.create_client() as client:
        response = await client.get(url)

    selector = Selector(text=response.text)
    results = []

    for item in selector.css('article[data-testid="product-card"]'):
        title = item.css('[data-testid="product-name"]::text').get() or ""
        url_path = item.css('[data-testid="product-name"]::attr(href)').get() or ""
        price = item.css('[class*="priceSection"] span::text').get() or ""

        results.append(
            {
                "title": title.strip(),
                "price": price,
                "url": urllib.parse.urljoin(config.THE_RANGE_URL, url_path)
                if url_path
                else "",
            }
        )

    return results
