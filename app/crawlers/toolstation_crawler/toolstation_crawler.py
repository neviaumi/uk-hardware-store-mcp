import urllib.parse
from typing import TypedDict

from parsel import Selector

import app.config as config
import app.crawlers.http_client as http_client
from app.crawlers.utils import clean_html, clean_text, remove_spaces

TOOLSTATION_API = f"{config.TOOLSTATION_URL}/api"


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

    # Simplified title extraction using <title> tag as requested
    raw_title = selector.css("title::text").get() or ""
    title = remove_spaces(raw_title.split("|")[0].strip())

    # Price extraction from the prominent blue bold span
    price = selector.css(r".text-blue .font-bold.text-\[28px\]::text").get() or ""

    # Description from 'Product details' accordion
    description = clean_text(
        selector.xpath(
            "//h3[contains(text(), 'Product details')]/following-sibling::div//div[contains(@class, 'text-blue')]//text()"
        ).getall()
    )

    # Technical specifications table
    detail = (
        clean_html(
            selector.xpath(
                "//h3[contains(text(), 'Technical specification')]/following-sibling::div//table"
            ).get()
        )
        or ""
    )

    # Promo badge extraction
    promo = clean_text(
        selector.css("[data-testid='savings-badge-wrapper'] *::text").getall()
    )

    return {
        "title": title,
        "price": price.strip(),
        "detail": detail,
        "description": description,
        "promo": promo if promo else None,
    }


class ProductSearchResponse(TypedDict):
    title: str
    price: str
    url: str
    promo: str | None


async def product_search(keyword: str) -> list[ProductSearchResponse]:
    query = urllib.parse.urlencode({
        "request_type": "search",
        "q": keyword,
        "start": "0",
        "search_type": "keyword",
        "skipCache": "true",
    })
    url = f"{TOOLSTATION_API}/search/crs?{query}"

    async with http_client.create_client() as client:
        response = await client.get(url)

    body = response.json()
    results = []

    # Safe extraction depending on API response format
    docs = body.get("response", {}).get("docs", [])

    for product in docs:
        title = product.get("title", "")
        price = product.get("price", "")
        product_url = product.get("url", "")
        promo = product.get("weboverlaytext", "")

        results.append({
            "title": title.strip() if title else "",
            "price": f"£{price}" if price else "",
            "url": f"{config.TOOLSTATION_URL}{urllib.parse.urlparse(product_url.strip()).path}"
            if product_url
            else "",
            "promo": promo if promo and "for" in promo else None,
        })

    return results
