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
        .getElementById("up")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "move", "direction": "up" }),
            false);
    document
        .getElementById("down")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "move", "direction": "down" }),
            false);
    document
        .getElementById("left")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "move", "direction": "left" }),
            false);
    document
        .getElementById("right")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "move", "direction": "right" }),
            false);
    document
        .getElementById("click_current_element")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "clickCurrentElement" }),
            false);
    document
        .getElementById("print_current_element")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "printCurrentElement" }),
            false);
    document
        .getElementById("play")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "playCurrentVideo" }),
            false);
    document
        .getElementById("mute")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "muteCurrentVideo" }),
            false);
    document
        .getElementById("next")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "playNextVideo" }),
            false);
    document
        .getElementById("test_server_loopback")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "testServerLoopback" }),
            false);
}, false);