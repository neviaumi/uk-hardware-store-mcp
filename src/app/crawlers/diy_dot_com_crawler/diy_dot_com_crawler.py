from typing import TypedDict
import urllib.parse
from bs4 import BeautifulSoup
import uuid

from crawlee import Request
from crawlee.crawlers import ParselCrawlingContext
from app.crawlers.base.crawlers import run_crawler_with_result
from app.crawlers.base.crawlers import router

DIY_DOT_COM_URL = "https://www.diy.com"


@router.handler(label="diy.com product search")
async def diy_dot_com_product_search_handler(context: ParselCrawlingContext) -> None:
    def _extract_product(product_selector):
        product_url = product_selector.css(
            "[data-testid='product-link']::attr(href)"
        ).get()
        return {
            "title": product_selector.css("[data-testid='product-name']::text").get(),
            "price": product_selector.css("[data-testid='product-price']::text").get(),
            "url": f"{DIY_DOT_COM_URL}{product_url}",
            "promo": product_selector.css("[data-testid='promotion-msg']::text").get(),
        }

    for product in context.selector.css("[data-testid='product']"):
        await context.push_data(
            _extract_product(product), dataset_name=context.request.unique_key
        )


@router.handler(label="diy.com product detail")
async def diy_dot_com_product_detail_handler(context: ParselCrawlingContext) -> None:
    def clean_html(html):
        soup = BeautifulSoup(html, "lxml")
        for tag in soup.find_all(True):
            tag.attrs.pop("style", None)
            tag.attrs.pop("class", None)
        return str(soup)

    await context.push_data(
        {
            "title": context.selector.css("[data-testid='product-name']::text").get(),
            "price": context.selector.css("[data-testid='product-price']::text").get(),
            "detail": clean_html(context.selector.css("#product-details").get()),
            "promo": context.selector.xpath(
                '//a[@data-testid="promotion-link"]/preceding-sibling::p/text()'
            ).get(),
        },
        dataset_name=context.request.unique_key,
    )


class ProductDetailResponse(TypedDict):
    title: str
    price: str
    detail: str
    promo: str | None


async def product_detail(url: str) -> ProductDetailResponse:
    request = Request.from_url(
        url, label="diy.com product detail", unique_key=str(uuid.uuid4())
    )
    return (await run_crawler_with_result(request, "html"))[0]


class ProductSearchResponse(TypedDict):
    title: str
    price: str
    url: str
    promo: str | None


async def product_search(keyword: str) -> list[ProductSearchResponse]:
    query = urllib.parse.urlencode({"term": keyword})
    request = Request.from_url(
        f"{DIY_DOT_COM_URL}/search?{query}",
        label="diy.com product search",
        unique_key=str(uuid.uuid4()),
    )
    return await run_crawler_with_result(request, "html")
