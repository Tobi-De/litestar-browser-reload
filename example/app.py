from pathlib import Path

from litestar import Litestar, get
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar.response import Template
from litestar_browser_reload import BrowserReloadPlugin


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


browser_reload = BrowserReloadPlugin(watch_paths=(Path("templates"),))

app = Litestar(
    route_handlers=[index, favicon],
    debug=True,
    plugins=[browser_reload],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
)
