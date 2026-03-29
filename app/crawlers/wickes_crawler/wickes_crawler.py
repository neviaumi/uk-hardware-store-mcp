import urllib.parse
from typing import TypedDict

from parsel import Selector

import app.config as config
import app.crawlers.http_client as http_client
from app.crawlers.utils import clean_html, remove_spaces


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

    raw_title = selector.css("title::text").get()
    title = remove_spaces(raw_title.split("|")[0].strip())

    price = selector.css(".main-price__value::text").get()
    description = selector.css(".product-main-info__description::text").get()

    return {
        "title": title.strip() if title else "",
        "price": price.strip() if price else "",
        "description": description.strip() if description else "",
        "detail": clean_html(selector.css(".additional-info").get()) or "",
        "promo": "".join(selector.css(".pdp-price__description *::text").getall()),
    }


class ProductSearchResponse(TypedDict):
    title: str
    price: str
    url: str
    promo: str | None


async def product_search(keyword: str) -> list[ProductSearchResponse]:
    query = urllib.parse.urlencode({"q": keyword})
    url = f"{config.WICKES_URL}/search?{query}"

    async with http_client.create_client() as client:
        response = await client.get(url)

    selector = Selector(text=response.text)

    results = []
    for product in selector.css("[data-product-code]"):
        product_url = product.css("a::attr(href)").get()
        promo = product.css(".products-list-v2__badge::text").get()
        title = product.css("a::attr(title)").get()
        price = product.css(".product-card__price-value::text").get()

        results.append({
            "title": title.strip() if title else "",
            "price": price.strip() if price else "",
            "url": f"{config.WICKES_URL}{product_url}" if product_url else "",
            "promo": promo.strip() if promo and "for" in promo else None,
        })

    return results
