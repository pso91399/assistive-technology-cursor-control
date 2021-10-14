// Page specific code here
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request["sender"] === "popup") {
        chrome.runtime.sendMessage(request["msgStr"], function(response) {
            console.log("Background send message response: ", response);
        });
    } else if (request["sender"] === "background") {
        console.log("Background server response: ", request["msgStr"])
    }
});