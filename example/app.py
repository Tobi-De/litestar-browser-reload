import logging
import asyncio
from pathlib import Path

from litestar import Litestar, get, WebSocket
from litestar_vite import ViteConfig, VitePlugin
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar.response import Template
from litestar.handlers import WebsocketListener

from watchfiles import awatch, DefaultFilter

logger = logging.getLogger("foxglove.cli")


watch_path = Path("templates")


async def watch_reload(prompt_reload):
    async for _ in awatch(watch_path, watch_filter=DefaultFilter()):
        print("something changed")
        await prompt_reload()


class BrowserReloadHandler(WebsocketListener):
    path = "/browser-reload"

    async def prompt_reload(self):
        if self.ws:
            logger.debug("prompting reload")
            print("sending text")
            await self.ws.send_text("reload")

    async def on_accept(self, socket: WebSocket) -> None:  # type: ignore
        logger.debug("reload websocket connecting")
        self._watch_task = asyncio.create_task(watch_reload(self.prompt_reload))
        self.ws = socket

    async def on_disconnect(self, socket: WebSocket) -> None:  # type: ignore
        logger.debug("reload websocket disconnecting")
        self._watch_task.cancel()
        try:
            await self._watch_task
        except asyncio.CancelledError:
            logger.debug("file watcher cancelled")

    async def on_receive(self, data: str, socket: WebSocket) -> str:
        self.ws = socket
        return data


@get("/")
async def index() -> Template:
    return Template(template_name="index.html.j2", context={})


@get("/favicon.ico", media_type="image/svg+xml")
async def favicon() -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        '<text y=".9em" font-size="90">🚀</text>'
        "</svg>"
    )


vite = VitePlugin(config=ViteConfig(template_dir="templates/"))
app = Litestar(
    route_handlers=[index, favicon, BrowserReloadHandler],
    debug=True,
    plugins=[vite],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
)
