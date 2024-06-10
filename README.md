# litestar-browser-reload

[![PyPI - Version](https://img.shields.io/pypi/v/litestar-browser-reload.svg)](https://pypi.org/project/litestar-browser-reload)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/litestar-browser-reload.svg)](https://pypi.org/project/litestar-browser-reload)

-----

> [!IMPORTANT]
> This plugin currently contains minimal features and is a work-in-progress

Automatic browser reload plugin for Litestar, designed for development use.

## Table of Contents

- [litestar-browser-reload](#litestar-browser-reload)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)
  - [Credits](#credits)

## Installation

```console
pip install litestar-browser-reload
```

## Usage

Parameters of `BrowserReloadPlugin`:

- `watch_paths: Sequence[Union[str, Path]]`: Paths to watch for changes.
- `ignore_dirs: Sequence[str]| None`: Directory names to ignore. ([example](https://watchfiles.helpmanual.io/api/filters/#watchfiles.DefaultFilter.ignore_dirs))
- `ignore_entity_patterns: Sequence[str]| None`: File/Directory name patterns to ignore ([example](https://watchfiles.helpmanual.io/api/filters/#watchfiles.DefaultFilter.ignore_entity_patterns)).

```python
from pathlib import Path

from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar.response import Template
from litestar_browser_reload import BrowserReloadPlugin

templates_path = Path("templates")
browser_reload = BrowserReloadPlugin(watch_paths=(templates_path,))

app = Litestar(
    route_handlers=[],
    debug=True,
    plugins=[browser_reload],
    template_config=TemplateConfig(
        directory=templates_path,
        engine=JinjaTemplateEngine,
    ),
)

```

Add the following to your base template:

```html
<head>
    ...
    {% if request.app.debug %}
    <script
        src="/__reload__/static/reload-listener.js"
        data-worker-script-path="/__reload__/static/reload-worker.js"
        data-ws-path="/__reload__"
        defer
    ></script>
    {% endif %}
 </head>
```

## License

`litestar-browser-reload` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


## Credits

Much of this was copied from [django-browser-reload](https://github.com/adamchainz/django-browser-reload) and [foxglove](https://github.com/samuelcolvin/foxglove)