from typing import TypedDict
import urllib.parse
from parsel import Selector

import app.crawlers.http_client as http_client
from app.crawlers.utils import clean_html

SCREWFIX_URL = "https://www.screwfix.com"


class ProductDetailResponse(TypedDict):
    title: str
    price: str
    detail: str
    description: str
    promo: str | None


async def product_detail(url: str) -> ProductDetailResponse:
    async with http_client.create_client() as client:
        response = await client.get(url)

    selector = Selector(text=response.text)

    promo_message = selector.css("[data-qaid='promo-message']::text").get()
    bulk_saves = clean_html(selector.css("[data-qaid='bulk-save-table']").get())

    return {
        "title": selector.css("[data-qaid='pdp-product-name'] *::text").get() or "",
        "price": "".join(selector.css("[data-qaid='pdp-price'] *::text").getall()[:-1])
        or "",
        "description": selector.css("[data-qaid='pdp-product-overview']::text").get()
        or "",
        "detail": clean_html(selector.css("[data-qaid='pdp-tabpanel-2'] table").get())
        or "",
        "promo": promo_message if promo_message is not None else bulk_saves,
    }


class ProductSearchResponse(TypedDict):
    title: str
    price: str
    url: str
    promo: str | None
    description: str  # Adding description to match the original pushed dataset fields


async def product_search(keyword: str) -> list[ProductSearchResponse]:
    query = urllib.parse.urlencode({"search": keyword})
    url = f"{SCREWFIX_URL}/search?{query}"

    async with http_client.create_client() as client:
        response = await client.get(url)

    selector = Selector(text=response.text)

    # Context-level selectors from original crawler
    promo_message_ctx = selector.css("[data-qaid='promo-banner'] *::text").get()
    bulk_saves_ctx = selector.css("[data-qaid='bulksave-banner'] *::text").get()

    results = []
    for product in selector.css("[data-qaid='product-card']"):
        product_url = product.css("[data-qaid='product_description']::attr(href)").get()
        title = product.css("[data-qaid='product_description'] span::text").get()
        price = product.css("[data-qaid='price']::text").get()
        description = clean_html(product.css("[data-qaid='bullets']").get())

        results.append(
            {
                "title": title or "",
                "price": price or "",
                "url": f"{SCREWFIX_URL}{product_url}" if product_url else "",
                "promo": promo_message_ctx
                if promo_message_ctx is not None
                else bulk_saves_ctx,
                "description": description or "",
            }
        )

    return results
