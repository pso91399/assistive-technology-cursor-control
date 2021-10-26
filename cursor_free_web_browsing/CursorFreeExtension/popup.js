function sendMessageToContent(message) {
    delay = function () {
        chrome.tabs.query({ currentWindow: true, active: true },
            function (tabs) {
                chrome.tabs.sendMessage(tabs[0].id, message);
            });
    };
    return delay;
}

document.addEventListener("DOMContentLoaded", function () {
    document
        .getElementById("next_clickable_element")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "nextClickableElement" }),
            false);
    document
        .getElementById("prev_clickable_element")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "prevClickableElement" }),
            false);
    document
        .getElementById("click_current_element")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "clickCurrentElement" }),
            false);
}, false);