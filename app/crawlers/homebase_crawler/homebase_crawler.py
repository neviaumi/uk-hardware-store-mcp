from typing import TypedDict
import urllib.parse
from parsel import Selector

import app.crawlers.http_client as http_client
from app.crawlers.utils import clean_html, clean_text

HOMEBASE_API = "https://www.homebase.co.uk/en-uk"


class ProductDetailResponse(TypedDict):
    title: str
    price: str
    detail: str
    promo: str | None


async def product_detail(url: str) -> ProductDetailResponse:
    async with http_client.create_client() as client:
        response = await client.get(url)

    selector = Selector(text=response.text)

    # Title is in h1.name
    title = selector.css("h1.name::text").get() or ""
    # Price for detail is in .pdp-price
    price = (
        selector.css(".pdp-price::text").get()
        or selector.css("[itemprop='price']::attr(content)").get()
        or ""
    )

    # If title still empty, try data attribute on a parent div
    if not title:
        title = (
            selector.css(".product-details-container::attr(data-product-name)").get()
            or ""
        )

    promo_node = selector.css(".product-promo")
    promo_text = (
        clean_text(promo_node[0].css("*::text").getall()) if promo_node else None
    )

    return {
        "title": title.strip(),
        "price": price.strip(),
        "detail": clean_html(selector.css(".product-description").get()),
        "promo": promo_text,
    }


class ProductSearchResponse(TypedDict):
    title: str
    price: str
    url: str


async def product_search(keyword: str) -> list[ProductSearchResponse]:
    query = urllib.parse.urlencode(
        {
            "text": keyword,
        }
    )
    url = f"{HOMEBASE_API}/search/?{query}"

    async with http_client.create_client() as client:
        response = await client.get(url)

    selector = Selector(text=response.text)
    results = []

    for item in selector.css(".product-item"):
        title = (
            item.css("::attr(data-product-name)").get()
            or item.css("a.product-link.name::text").get()
            or ""
        )
        url_path = (
            item.css("::attr(data-url)").get()
            or item.css("a.product-link.name::attr(href)").get()
            or ""
        )
        price = (
            item.css("::attr(data-price-formatted-value)").get()
            or item.css(".price::text").get()
            or ""
        )

        results.append(
            {
                "title": title.strip(),
                "price": price.strip(),
                "url": f"https://www.homebase.co.uk{url_path}" if url_path else "",
            }
        )

    return results
