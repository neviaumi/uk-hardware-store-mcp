from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.logger import get_logging_for_fastapi
from app.mcp_server import mcp

logger = get_logging_for_fastapi()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield


app = FastAPI(lifespan=lifespan, redirect_slashes=True)

mcp_app = mcp.streamable_http_app()
app.mount("/mcp", app=mcp_app, name="MCP")
