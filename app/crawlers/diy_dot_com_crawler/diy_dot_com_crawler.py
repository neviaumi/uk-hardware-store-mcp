from typing import TypedDict
import urllib.parse
from parsel import Selector

import app.crawlers.http_client as http_client
from app.crawlers.utils import clean_html

DIY_DOT_COM_URL = "https://www.diy.com"


class ProductDetailResponse(TypedDict):
    title: str
    price: str
    detail: str
    promo: str | None


async def product_detail(url: str) -> ProductDetailResponse:
    async with http_client.create_client() as client:
        response = await client.get(url)

    selector = Selector(text=response.text)

    return {
        "title": selector.css("[data-testid='product-name']::text").get() or "",
        "price": selector.css("[data-testid='product-price']::text").get() or "",
        "detail": clean_html(selector.css("#product-details").get()),
        "promo": selector.xpath(
            '//a[@data-testid="promotion-link"]/preceding-sibling::p/text()'
        ).get(),
    }


class ProductSearchResponse(TypedDict):
    title: str
    price: str
    url: str
    promo: str | None


async def product_search(keyword: str) -> list[ProductSearchResponse]:
    query = urllib.parse.urlencode({"term": keyword})
    url = f"{DIY_DOT_COM_URL}/search?{query}"

    async with http_client.create_client() as client:
        response = await client.get(url)

    selector = Selector(text=response.text)

    results = []
    for product in selector.css("[data-testid='product']"):
        product_url = product.css("[data-testid='product-link']::attr(href)").get()
        title = product.css("[data-testid='product-name']::text").get() or ""
        price = product.css("[data-testid='product-price']::text").get() or ""
        promo = product.css("[data-testid='promotion-msg']::text").get()

        results.append(
            {
                "title": title,
                "price": price,
                "url": f"{DIY_DOT_COM_URL}{product_url}" if product_url else "",
                "promo": promo,
            }
        )

    return results
