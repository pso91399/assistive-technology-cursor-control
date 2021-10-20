document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("send_test_message").addEventListener("click", sendTestMessageOnClick, false);
    function sendTestMessageOnClick() {
        chrome.tabs.query({ currentWindow: true, active: true },
            function (tabs) {
                chrome.tabs.sendMessage(tabs[0].id, { "msgStr": "hello from chrome extension!", "sender": "popup", "action": "sendMessage" });
            });
    }

    document.getElementById("control_video_mute").addEventListener("click", controlVideoMuteOnClick, false);
    function controlVideoMuteOnClick() {
        chrome.tabs.query({ currentWindow: true, active: true },
            function (tabs) {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "popup", "action": "controlVideoMute" });
            });
    }

    document.getElementById("control_video_play").addEventListener("click", controlVideoPlayOnClick, false);
    function controlVideoPlayOnClick() {
        chrome.tabs.query({ currentWindow: true, active: true },
            function (tabs) {
                chrome.tabs.sendMessage(tabs[0].id, { "sender": "popup", "action": "controlVideoPlay" });
            });
    }

}, false);