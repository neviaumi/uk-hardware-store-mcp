from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.mcp_server import mcp


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield


app = FastAPI(lifespan=lifespan, redirect_slashes=False)
mcp_app = mcp.streamable_http_app()
app.mount("/mcp", app=mcp_app, name="MCP")
app.mount("/mcp/", app=mcp_app, name="MCP Alias")
