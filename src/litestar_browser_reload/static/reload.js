// Create a new WebSocket connection to the specified endpoint
const socket = new WebSocket('ws://localhost:8000/browser-reload');

// Event listener for when the WebSocket connection is opened
socket.onopen = function (event) {
    console.log('WebSocket connection established', event);
};

// Event listener for when a message is received from the server
socket.onmessage = function (event) {
    console.log('Message received from server', event.data);
    // Check if the received message is 'reload'
    if (event.data === 'reload') {
        console.log('Reloading page as instructed by server');
        // Reload the current page
        window.location.reload();
    }
};

// Event listener for when the WebSocket connection is closed
socket.onclose = function (event) {
    console.log('WebSocket connection closed', event);
};

// Event listener for any errors that occur with the WebSocket connection
socket.onerror = function (error) {
    console.log('WebSocket error', error);
};