from enum import Enum
from typing import Union

import mcp.server.fastmcp.prompts as prompts
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from pydantic import BaseModel, Field

import app.crawlers.diy_dot_com_crawler as diy_dot_com_crawler
import app.crawlers.homebase_crawler.homebase_crawler as homebase_crawler
import app.crawlers.screwfix_crawler as screwfix_crawler
import app.crawlers.toolstation_crawler as toolstation_crawler
import app.crawlers.wickes_crawler as wickes_crawler


class Provider(str, Enum):
    DIY_DOT_COM = "B&Q"
    HOMEBASE = "Homebase"
    SCREWFIX = "Screwfix"
    TOOLSTATION = "Toolstation"
    WICKES = "Wickes"


mcp = FastMCP("Hardware Store", streamable_http_path="/", host="0.0.0.0")


@mcp.prompt("Hardware store staff", "Helpful assistant for a UK hardware store project")
def hardware_store_staff() -> list[prompts.base.Message]:
    return [
        prompts.base.UserMessage(
            content="""You are a knowledgeable hardware store assistant with expertise in DIY tools and equipment. Your role is to:

1. UNDERSTAND REQUIREMENTS:
- Listen carefully to customer needs and use cases.
- Ask clarifying questions about their project (e.g., "What material are you drilling into?", "Is this for indoor or outdoor use?") to suggest the most appropriate tools.
- Consider the user's skill level and safety requirements.

2. PRODUCT RECOMMENDATIONS:
- Search across B&Q (diy.com), Homebase, Screwfix, Toolstation, and Wickes.
- Provide 2-3 best options that match the customer's needs.
- Include price comparisons across different stores when available.
- Always include direct product URLs.

3. PRODUCT INFORMATION:
- Present key features and specifications clearly.
- Explain WHY each recommendation suits their specific project.
- Include relevant safety information or mandatory accessories (e.g., "You'll need a SDS bit for this drill").
- Mention ongoing promotions if available.

4. INTERACTION STYLE:
- Be friendly, professional, and practical.
- Use clear, jargon-free language.
- Offer follow-up assistance for maintenance or usage tips.

Format your product recommendations as follows:
• Product Name
• Price
• Store Link
• Key Features
• Why it's recommended

Wait for the user to describe their project before offering specific product links."""
        ),
        prompts.base.AssistantMessage(
            content="""Welcome to the Hardware Store! I'm here to help you find the perfect tools and supplies for your DIY projects. To give you the best advice, could you please tell me a bit more about what you're planning to work on today?"""
        ),
    ]


class ProductDetailRequest(BaseModel):
    provider: Provider = Field(
        description="The UK hardware retailer to fetch details from (B&Q, Homebase, Screwfix, Toolstation, or Wickes)."
    )
    product_url: str = Field(
        description="The absolute product URL (e.g., `https://www.diy.com/products/hammer-12345`)."
    )


ProductDetailResponse = Union[
    diy_dot_com_crawler.ProductDetailResponse,
    homebase_crawler.ProductDetailResponse,
    screwfix_crawler.ProductDetailResponse,
    toolstation_crawler.ProductDetailResponse,
    wickes_crawler.ProductDetailResponse,
]


@mcp.tool(
    "get_product_detail",
    "Fetch comprehensive product details (specifications, description, price) using a store URL from a specific provider.",
)
async def get_product_detail(request: ProductDetailRequest) -> ProductDetailResponse:
    match request.provider:
        case Provider.DIY_DOT_COM:
            result = await diy_dot_com_crawler.product_detail(request.product_url)
        case Provider.HOMEBASE:
            result = await homebase_crawler.product_detail(request.product_url)
        case Provider.SCREWFIX:
            result = await screwfix_crawler.product_detail(request.product_url)
        case Provider.TOOLSTATION:
            result = await toolstation_crawler.product_detail(request.product_url)
        case Provider.WICKES:
            result = await wickes_crawler.product_detail(request.product_url)
        case _:
            raise ToolError(f"Provider {request.provider} is not supported.")

    return result


class ProductsSearchRequest(BaseModel):
    keyword: str = Field(
        description="The search term (e.g., 'M6 Hex Bolt', 'Combi Drill') to query the catalog."
    )
    provider: Provider = Field(
        description="The UK hardware retailer to search on (B&Q, Homebase, Screwfix, Toolstation, or Wickes)."
    )


ProductSearchResponse = list[
    Union[
        diy_dot_com_crawler.ProductSearchResponse,
        homebase_crawler.ProductSearchResponse,
        screwfix_crawler.ProductSearchResponse,
        toolstation_crawler.ProductSearchResponse,
        wickes_crawler.ProductSearchResponse,
    ]
]


@mcp.tool(
    "search_products",
    "Search for products on a specific UK hardware retailer's catalog.",
)
async def search_products(request: ProductsSearchRequest) -> ProductSearchResponse:
    """Search for products on the specified retailer's website.

    Args:
        request (ProductsSearchRequest): The search request containing the keyword and provider.

    Returns:
        ProductSearchResponse: A list of objects containing product name, price, URL, and thumbnail.

    """
    match request.provider:
        case Provider.DIY_DOT_COM:
            result = await diy_dot_com_crawler.product_search(request.keyword)
        case Provider.HOMEBASE:
            result = await homebase_crawler.product_search(request.keyword)
        case Provider.SCREWFIX:
            result = await screwfix_crawler.product_search(request.keyword)
        case Provider.TOOLSTATION:
            result = await toolstation_crawler.product_search(request.keyword)
        case Provider.WICKES:
            result = await wickes_crawler.product_search(request.keyword)
        case _:
            raise ToolError(f"Provider {request.provider} is not supported.")

    return result
