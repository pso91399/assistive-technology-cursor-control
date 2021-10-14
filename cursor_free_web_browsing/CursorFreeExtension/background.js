let testSocket = new WebSocket("ws://127.0.0.1:9003");
testSocket.onerror = function (event) {
    console.error("WebSocket error observed:", event);
};

testSocket.onmessage = function (event) {
    chrome.tabs.query({ active: true, currentWindow: true },
        function (tabs) {
            chrome.tabs.sendMessage(tabs[0].id, { "msgStr": event.data, "sender": "background" }, function (response) { });
        });
};

chrome.runtime.onInstalled.addListener(() => {
    // Server-client communication code here

    chrome.runtime.onMessage.addListener(function (msgStr, sender, sendResponse) {
        testSocket.send(msgStr);
        sendResponse("Gotcha!");
    });
});

