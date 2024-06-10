# SPDX-FileCopyrightText: 2024-present Tobi DEGNON <tobidegnon@proton.me>
#
# SPDX-License-Identifier: MIT
from pathlib import Path
from dataclasses import dataclass
from typing import Union, List
from collections.abc import AsyncGenerator

from litestar import get
from litestar.config.app import AppConfig
from litestar.plugins import InitPluginProtocol
from litestar.response import ServerSentEvent, ServerSentEventMessage
from litestar.types import SSEData

from watchfiles import awatch


def reload_endpoint(watch_paths: List[Union[Path, str]]):

    async def watch_reload() -> AsyncGenerator[SSEData, None]:
        async for _ in awatch(*watch_paths):
            yield ServerSentEventMessage(event="reload")

    @get(path="/browser-reload")
    async def browser_reload_handler() -> ServerSentEvent:
        return ServerSentEvent(watch_reload())

    return browser_reload_handler


class BrowserReloadPlugin(InitPluginProtocol):

    def __init__(self, watch_paths: List[Union[Path, str]]) -> None:
        self.watch_paths = watch_paths

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        if app_config.debug:
            app_config.route_handlers.append(reload_endpoint(self.watch_paths))
        return app_config
