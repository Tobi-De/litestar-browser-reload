//https://github.com/adamchainz/litestar-browser-reload/blob/main/src/django_browser_reload/static/litestar-browser-reload/reload-worker.js
// Thanks again Adam, you are the best
/* eslint-env worker */
'use strict'

let wsPath = null
let port = null
let currentVersionId = null
let websocket = null

addEventListener('connect', (event) => {
  if (port) {
    port.close()
  }
  port = event.ports[0]
  port.addEventListener('message', receiveMessage)
  port.start()
})

const receiveMessage = (event) => {
  if (event.data.type === 'initialize') {
    const givenwsPath = event.data.wsPath

    if (givenwsPath !== wsPath) {
      if (websocket) {
        websocket.close()
      }

      resetConnectTimeout()

      setTimeout(connectToWebSocket, 0)
    }

    wsPath = event.data.wsPath
  }
}

let connectAttempts
let connectTimeoutMs

const resetConnectTimeout = () => {
  connectAttempts = 0
  connectTimeoutMs = 100
}
resetConnectTimeout()

const bumpConnectTimeout = () => {
  connectAttempts++

  if (connectTimeoutMs === 100 && connectAttempts === 20) {
    connectAttempts = 0
    connectTimeoutMs = 300
  } else if (connectTimeoutMs === 300 && connectAttempts === 20) {
    connectAttempts = 0
    connectTimeoutMs = 1000
  } else if (connectTimeoutMs === 1000 && connectAttempts === 20) {
    connectAttempts = 0
    connectTimeoutMs = 3000
  } else if (connectAttempts === 100) {
    console.debug('😢 litestar-browser-reload failed to connect after 5 minutes, shutting down.')
    close()
    return
  }
  if (connectAttempts === 0) {
    console.debug('😅 litestar-browser-reload WebSocket error, retrying every ' + connectTimeoutMs + 'ms')
  }
}

const connectToWebSocket = () => {
  if (!wsPath) {
    setTimeout(connectToWebSocket, connectTimeoutMs)
    return
  }

  websocket = new WebSocket(wsPath)

  websocket.addEventListener('open', () => {
    console.debug('😎 litestar-browser-reload connected')
    resetConnectTimeout()
  })

  websocket.addEventListener('message', (event) => {
    const message = JSON.parse(event.data)

    if (message.type === 'ping') {
      if (currentVersionId !== null && currentVersionId !== message.versionId) {
        console.debug('🔁 litestar-browser-reload triggering reload.')
        port.postMessage('Reload')
      }

      currentVersionId = message.versionId
    } else if (message.type === 'reload') {
      port.postMessage('Reload')
    }
  })

  websocket.addEventListener('error', () => {
    websocket.close()
    websocket = null
    bumpConnectTimeout()
    setTimeout(connectToWebSocket, connectTimeoutMs)
  })

  websocket.addEventListener('close', () => {
    websocket = null
    bumpConnectTimeout()
    setTimeout(connectToWebSocket, connectTimeoutMs)
  })
}