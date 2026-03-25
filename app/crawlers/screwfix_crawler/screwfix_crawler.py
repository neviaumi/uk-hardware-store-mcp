from typing import TypedDict
import urllib.parse
from bs4 import BeautifulSoup
import uuid

from crawlee import Request
from crawlee.crawlers import ParselCrawlingContext
from app.crawlers.base.crawlers import router, run_crawler_with_result

SCREWFIX_URL = "https://www.screwfix.com"


def clean_html(html):
    if html is None:
        return html
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(True):
        tag.attrs.pop("style", None)
        tag.attrs.pop("class", None)
    return str(soup)


@router.handler(label="screwfix product search")
async def screwfix_product_search_handler(context: ParselCrawlingContext) -> None:
    def _extract_product(product_selector):
        product_url = product_selector.css(
            "[data-qaid='product_description']::attr(href)"
        ).get()
        promo_message = context.selector.css("[data-qaid='promo-banner'] *::text").get()
        bulk_saves = context.selector.css("[data-qaid='bulksave-banner'] *::text").get()
        return {
            "title": product_selector.css(
                "[data-qaid='product_description'] span::text"
            ).get(),
            "price": product_selector.css("[data-qaid='price']::text").get(),
            "url": f"{SCREWFIX_URL}{product_url}",
            "promo": promo_message if promo_message is not None else bulk_saves,
            "description": clean_html(
                product_selector.css("[data-qaid='bullets']").get()
            ),
        }

    for product in context.selector.css("[data-qaid='product-card']"):
        await context.push_data(
            _extract_product(product), dataset_name=context.request.unique_key
        )


@router.handler(label="screwfix product detail")
async def screwfix_product_detail_handler(context: ParselCrawlingContext) -> None:
    promo_message = context.selector.css("[data-qaid='promo-message']::text").get()
    bulk_saves = clean_html(context.selector.css("[data-qaid='bulk-save-table']").get())

    await context.push_data(
        {
            "title": context.selector.css(
                "[data-qaid='pdp-product-name'] *::text"
            ).get(),
            "price": "".join(
                context.selector.css("[data-qaid='pdp-price'] *::text").getall()[:-1]
            ),
            "description": context.selector.css(
                "[data-qaid='pdp-product-overview']::text"
            ).get(),
            "detail": clean_html(
                context.selector.css("[data-qaid='pdp-tabpanel-2'] table").get()
            ),
            "promo": promo_message if promo_message is not None else bulk_saves,
        },
        dataset_name=context.request.unique_key,
    )


class ProductDetailResponse(TypedDict):
    title: str
    price: str
    detail: str
    description: str
    promo: str | None


async def product_detail(url: str) -> ProductDetailResponse:
    request = Request.from_url(
        url, label="screwfix product detail", unique_key=str(uuid.uuid4())
    )
    return (await run_crawler_with_result(request, "html"))[0]


class ProductSearchResponse(TypedDict):
    title: str
    price: str
    url: str
    promo: str | None


async def product_search(keyword: str) -> list[ProductSearchResponse]:
    query = urllib.parse.urlencode({"search": keyword})
    request = Request.from_url(
        f"{SCREWFIX_URL}/search?{query}",
        label="screwfix product search",
        unique_key=str(uuid.uuid4()),
    )
    return await run_crawler_with_result(request, "html")
