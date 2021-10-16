// Page specific code here
const scriptName = "content.js: ";
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request["sender"] === "popup") {
        console.log(scriptName, "Sending message to background.js")
        chrome.runtime.sendMessage(request["msgStr"], function(response) {
            console.log(scriptName, "Background send message response: ", response);
        });
    } else if (request["sender"] === "background") {
        console.log(scriptName, "Background server response: ", request["msgStr"])
    }
});