# litestar-browser-reload

[![PyPI - Version](https://img.shields.io/pypi/v/litestar-browser-reload.svg)](https://pypi.org/project/litestar-browser-reload)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/litestar-browser-reload.svg)](https://pypi.org/project/litestar-browser-reload)

-----

> [!IMPORTANT]
> This plugin currently contains minimal features and is a work-in-progress

Auto browser reload plugin for litestar, intended for use in development.

## Table of Contents

- [litestar-browser-reload](#litestar-browser-reload)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## Installation

```console
pip install litestar-browser-reload
```

## Usage

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

```javascript
 <script>
    // Create a new WebSocket connection to the specified endpoint
    const socket = new WebSocket('ws://localhost:8000/browser-reload');

    // Event listener for when the WebSocket connection is opened
    socket.onopen = function(event) {
    console.log('WebSocket connection established', event);
    };

    // Event listener for when a message is received from the server
    socket.onmessage = function(event) {
    console.log('Message received from server', event.data);
    // Check if the received message is 'reload'
    if (event.data === 'reload') {
        console.log('Reloading page as instructed by server');
        // Reload the current page
        window.location.reload();
    }
    };

    // Event listener for when the WebSocket connection is closed
    socket.onclose = function(event) {
    console.log('WebSocket connection closed', event);
    };

    // Event listener for any errors that occur with the WebSocket connection
    socket.onerror = function(error) {
    console.log('WebSocket error', error);
    };
</script>
```

## License

`litestar-browser-reload` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
