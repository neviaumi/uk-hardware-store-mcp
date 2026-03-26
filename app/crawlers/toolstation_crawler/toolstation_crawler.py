from typing import TypedDict
import urllib.parse

import app.crawlers.http_client as http_client

TOOLSTATION_API = "https://www.toolstation.com/api"


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

        results.append(
            {
                "title": title.strip() if title else "",
                "price": f"£{price}" if price else "",
                "url": product_url.strip() if product_url else "",
                "promo": promo if promo and "for" in promo else None,
            }
        )

    return results
