from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.types import ASGIApp, Receive, Scope, Send

from app.logger import get_logging_for_fastapi
from app.mcp_server import mcp

logger = get_logging_for_fastapi()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield


app = FastAPI(lifespan=lifespan, redirect_slashes=True)


class RequestLoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        receive_messages = []
        body = b""
        more_body = True
        while more_body:
            message = await receive()
            receive_messages.append(message)
            if message["type"] == "http.disconnect":
                break
            body += message.get("body", b"")
            more_body = message.get("more_body", False)

        body_str = body.decode("utf-8", errors="replace")
        logger.info(f"Request body: {body_str}")

        async def replaying_receive() -> dict:
            if receive_messages:
                return receive_messages.pop(0)
            return await receive()

        await self.app(scope, replaying_receive, send)


app.add_middleware(RequestLoggingMiddleware)

mcp_app = mcp.streamable_http_app()
app.mount("/mcp", app=mcp_app, name="MCP")
