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
    document.getElementById("send_test_message").addEventListener("click", sendMessageToContent({ "sender": "popup", "action": "sendMessage", "msgStr": "hello from chrome extension!" }), false);

    buttonActionDictionary = {
        "control_video_mute": "controlVideoMute",
        "control_video_play": "controlVideoPlay",
        "control_video_forward": "controlVideoForward",
        "control_video_backward": "controlVideoBackward"
    };

    for (buttonId in buttonActionDictionary) {
        document.getElementById(buttonId).addEventListener("click", sendMessageToContent({ "sender": "popup", "action": buttonActionDictionary[buttonId] }), false);
    }

}, false);