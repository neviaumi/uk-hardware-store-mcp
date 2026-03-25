from fastapi import FastAPI

from app.mcp_server import mcp

app = FastAPI(lifespan=lambda app: mcp.session_manager.run())

app.mount("/mcp", app=mcp.streamable_http_app(), name="MCP")
