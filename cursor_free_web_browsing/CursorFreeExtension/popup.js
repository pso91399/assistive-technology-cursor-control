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
            sendMessageToContent({ "sender": "popup", "action": "play" }),
            false);
    document
        .getElementById("mute")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "mute" }),
            false);
    document
        .getElementById("next")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "next" }),
            false);
    document
        .getElementById("pgup")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "pgup" }),
            false);
    document
        .getElementById("pgdn")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "pgdn" }),
            false);
    document
        .getElementById("back")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "back" }),
            false);
    document
        .getElementById("forward")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "forward" }),
            false);
    document
        .getElementById("close")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "close" }),
            false);
    document
        .getElementById("test_server_loopback")
        .addEventListener("click",
            sendMessageToContent({ "sender": "popup", "action": "testServerLoopback" }),
            false);
}, false);