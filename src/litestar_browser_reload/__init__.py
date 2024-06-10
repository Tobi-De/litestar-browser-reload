# SPDX-FileCopyrightText: 2024-present Tobi DEGNON <tobidegnon@proton.me>
#
# SPDX-License-Identifier: MIT
import asyncio
import logging
import uuid
from pathlib import Path
from typing import List
from typing import Sequence
from typing import Union

from litestar import WebSocket
from litestar.config.app import AppConfig
from litestar.handlers import WebsocketListener
from litestar.plugins import InitPluginProtocol
from litestar.static_files import create_static_files_router
from watchfiles import awatch
from watchfiles import DefaultFilter


logger = logging.getLogger("browser-reload")

version_id = str(uuid.uuid4())


def reload_endpoint(
    watch_paths: Sequence[Union[Path, str]],
    ignore_dirs: Sequence[str] | None = None,
    ignore_entity_patterns: Sequence[str] | None = None,
):
    # shamelessy copied from https://github.com/samuelcolvin/foxglove/blob/main/foxglove/devtools.py

    async def watch_reload(prompt_reload):
        async for _ in awatch(
            *watch_paths,
            watch_filter=DefaultFilter(
                ignore_dirs=ignore_dirs,
                ignore_entity_patterns=ignore_entity_patterns
            ),
        ):
            await prompt_reload()

    class BrowserReloadHandler(WebsocketListener):
        path = "/__reload__"

        async def prompt_reload(self):
            if self.ws:
                logger.debug("prompting reload")
                await self.ws.send_json({"type": "reload"})

        async def on_accept(self, socket: WebSocket) -> None:  # type: ignore
            logger.debug("reload websocket connecting")
            self._watch_task = asyncio.create_task(watch_reload(self.prompt_reload))
            self.ws = socket
            await self.ws.send_json({"type": "ping", "versionId": version_id})

        async def on_disconnect(self) -> None:  # type: ignore
            logger.debug("reload websocket disconnecting")
            self._watch_task.cancel()
            try:
                await self._watch_task
            except asyncio.CancelledError:
                logger.debug("file watcher cancelled")

        async def on_receive(self, data: str) -> str:
            return data

    return BrowserReloadHandler


class BrowserReloadPlugin(InitPluginProtocol):

    def __init__(self, watch_paths: List[Union[Path, str]]) -> None:
        self.watch_paths = watch_paths

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        if app_config.debug:
            app_config.route_handlers.append(reload_endpoint(self.watch_paths))
            app_config.route_handlers.append(
                create_static_files_router(
                    directories=[Path(__file__).parent / "static"],
                    path="/__reload__/static",
                    name="browser_reload_static",
                    opt={"exclude_from_auth": True},
                    include_in_schema=False,
                ),
            )
        return app_config
