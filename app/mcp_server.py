from enum import Enum
from typing import Union

import mcp.server.fastmcp.prompts as prompts
from mcp.server.fastmcp import FastMCP
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


@mcp.prompt("Hardware store staff", "helpful assistant for a hardware store")
def hardware_store_staff() -> list[prompts.base.Message]:
    return [
        prompts.base.UserMessage(
            content="""You are a knowledgeable hardware store assistant with expertise in DIY tools and equipment. Your role is to:

1. UNDERSTAND REQUIREMENTS:
- Listen carefully to customer needs and use cases
- Ask clarifying questions when necessary to better understand their project
- Consider user's skill level when making recommendations

2. PRODUCT RECOMMENDATIONS:
- Search across diy.com, screwfix.com, toolstation.com, and wickes.co.uk
- Provide 2-3 best options that match the customer's needs
- Include price comparisons across different stores
- Always include direct product URLs

3. PRODUCT INFORMATION:
- Present key features and specifications
- Explain why each recommendation suits their needs
- Include any relevant safety information or usage tips
- Mention ongoing promotions or deals if available

4. INTERACTION STYLE:
- Be friendly and professional
- Use clear, jargon-free language
- Offer follow-up assistance for additional questions
- Provide practical advice for tool usage and maintenance

When suggesting products, format your response as:
• Product Name
• Price
• Store Link
• Key Features
• Why it's recommended

Remember to get specific details about the customer's project before making recommendations to ensure the most suitable tools are suggested."""
        ),
        prompts.base.AssistantMessage(
            content="""Welcome to the Hardware Store! I'm here to help you find the right tools and equipment for your project. Could you tell me about what you're working on?"""
        ),
    ]


class ProductDetailRequest(BaseModel):
    provider: Provider = Field(description="The provider to search for products on.")
    product_url: str = Field(
        description="The absolute product URL (e.g., `https://www.diy.com/products/hammer`)."
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
    "Retrieve detailed product information from a provider for a specific product URL.",
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
            result = {}

    return result


class ProductsSearchRequest(BaseModel):
    keyword: str = Field(description="The search term to query the product catalog.")
    provider: Provider = Field(description="The provider to search for products on.")


ProductSearchResponse = list[
    Union[
        diy_dot_com_crawler.ProductSearchResponse,
        homebase_crawler.ProductSearchResponse,
        screwfix_crawler.ProductSearchResponse,
        toolstation_crawler.ProductSearchResponse,
        wickes_crawler.ProductSearchResponse,
    ]
]


@mcp.tool("search_products", "Search for products on multiple providers.")
async def search_products(request: ProductsSearchRequest) -> ProductSearchResponse:
    """Search for products on multiple providers.

    Args:
        request (ProductsSearchRequest): The search request.

    Returns:
        str: A JSON-encoded list of product search results from multiple providers.

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
            result = []

    return result
