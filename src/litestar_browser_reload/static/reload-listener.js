// https://github.com/adamchainz/django-browser-reload/blob/main/src/django_browser_reload/static/django-browser-reload/reload-listener.js
// thanks Adam, and sorry for having no soul
'use strict'

{
  const dataset = document.currentScript.dataset
  const workerScriptPath = dataset.workerScriptPath
  const wsPath = dataset.wsPath

  if (!window.SharedWorker) {
    console.debug('😭 litestar-browser-reload cannot work in this browser.')
  } else {
    const worker = new SharedWorker(workerScriptPath, {
      name: 'litestar-browser-reload'
    })

    worker.port.addEventListener('message', (event) => {
      if (event.data === 'Reload') {
        location.reload()
      }
    })

    worker.port.postMessage({
      type: 'initialize',
      wsPath
    })

    worker.port.start()
  }
}