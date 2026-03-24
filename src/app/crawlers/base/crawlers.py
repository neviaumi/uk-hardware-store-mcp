from crawlee.crawlers import ParselCrawlingContext
from crawlee.router import Router
from crawlee.crawlers import ParselCrawler
from crawlee.http_clients import HttpxHttpClient
from crawlee.crawlers import HttpCrawler
from crawlee import Request
from crawlee.storages import Dataset
from crawlee.storage_clients import MemoryStorageClient

router = Router()
_api_crawler = HttpCrawler(
    configure_logging=False, request_handler=router, http_client=HttpxHttpClient(), storage_client=MemoryStorageClient()
)
_html_crawler = ParselCrawler(
    configure_logging=False,
    request_handler=router,
    http_client=HttpxHttpClient(),
    storage_client=MemoryStorageClient()
)

from typing import Literal

async def run_crawler_with_result(request: Request, content_type: Literal["html", "api"]):
    dataset = await Dataset.open(name=request.unique_key)
    if content_type == "html":
        await _html_crawler.run([request])
    elif content_type == "api":
        await _api_crawler.run([request])
    result = [item for item in (await dataset.get_data()).items]
    await dataset.drop()
    return result

    