import urllib.parse
from typing import Literal

from parsel import Selector
from pydantic import BaseModel, Field

import app.config as config
import app.crawlers.http_client as http_client
from app.crawlers.utils import clean_html, clean_text

_source = "The Range"


class ProductDetailResponse(BaseModel):
    source: Literal[_source] = Field(
        description="The source of the product.", default=_source
    )
    title: str = Field(description="The full commercial name of the product.")
    price: str = Field(
        description="The current retail price, including the currency symbol."
    )
    detail: str = Field(
        description="Comprehensive technical specifications or item details in HTML format."
    )
    promo: str | None = Field(
        description="Any active promotional offers or discounts associated with the product."
    )


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

    return ProductDetailResponse(
        title=title.strip(),
        price=price,
        detail=clean_html(detail_html),
        promo=promo_text,
    )


class ProductSearchResponse(BaseModel):
    source: Literal[_source] = Field(
        description="The source of the search result.", default=_source
    )
    title: str = Field(
        description="The commercial name of the product as shown in search results."
    )
    price: str = Field(
        description="The current retail price, including the currency symbol."
    )
    url: str = Field(
        description="The absolute URL leading to the product's detail page."
    )


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
            ProductSearchResponse(
                title=title.strip(),
                price=price,
                url=urllib.parse.urljoin(config.THE_RANGE_URL, url_path)
                if url_path
                else "",
            )
        )

    return results
