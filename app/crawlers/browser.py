import urllib.parse
from contextlib import asynccontextmanager

from patchright.async_api import async_playwright

from app.config import BROWSERLESS_API_KEY, BROWSERLESS_ENDPOINT


@asynccontextmanager
async def create_browser():
    if BROWSERLESS_API_KEY is None:
        raise ValueError("BROWSERLESS_API_KEY is not set")
    params = {"token": BROWSERLESS_API_KEY}
    endpoint = f"{BROWSERLESS_ENDPOINT}?{urllib.parse.urlencode(params)}"

    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(
            endpoint_url=endpoint, timeout=120000
        )
        context = await browser.new_context()
        try:
            yield context
        finally:
            await context.close()
            await browser.close()
