const scriptName = "background.js: ";

const socket = io.connect("http://127.0.0.1:1998/extension");

socket.on("connect", function () {
    console.log("Client connected!")
});

socket.on('message', function (msg) {
    console.log(scriptName, "Received message from server:", msg);
    chrome.tabs.query({ active: true, currentWindow: true },
        function (tabs) {
            if (msg === "click") {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "server", "action": "click" });
            } else if (msg == "pgup") {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "server", "action": "pgup" });
            } else if (msg == "pgdn") {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "server", "action": "pgdn" });
            } else if (msg == "forward") {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "server", "action": "forward" });
            } else if (msg == "backward") {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "server", "action": "backward" });
            } else if (msg == "play") {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "server", "action": "play" });
            } else if (msg == "next") {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "server", "action": "next" });
            } else if (msg == "mute") {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "server", "action": "mute" });
            } else if (msg == "close") {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "server", "action": "close" });
            } else {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "server", "action": "move", "direction": msg });
            }
        });
});

chrome.runtime.onInstalled.addListener(() => {
    // Server-client communication code here
    chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
        if (request["sender"] === "content" && request["action"] === "testServerLoopback") {
            socket.send("testServerLoopback");
        }

        if (request["sender"] === "content" && request["action"] === "closeCurrentTab") {
            chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
                chrome.tabs.remove(tabs[0].id);
            });
        }
    });
});

chrome.runtime.onMessageExternal.addListener(
    function (request, sender, sendResponse) {
        chrome.tabs.query({ active: true, currentWindow: true },
            function (tabs) {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "background", "action": "pageMessage", "clickableIds": request.clickableIds, "videoIds": request.videoIds });
            });
        console.log(request.clickableIds);
        console.log(request.videoIds);
    });