// Page specific code here
const scriptName = "content.js: ";

class VideoHandler {
    constructor(document) {
        this.document = document;
        this.player = this.document.getElementsByTagName("video")[0];
    }

    mute() {
        if (!this.player.muted) {
            this.player.muted = true;
            console.log(scriptName, "Muted!")
        } else {
            this.player.muted = false;
            console.log(scriptName, "Unmuted!")
        }
    }

    play() {
        if (this.player.paused) {
            this.player.play();
        } else {
            this.player.pause();
        }
    }
}

let handler = new VideoHandler(document);

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request["sender"] === "popup") {
        if (request["action" === "sendMessage"]) {
            console.log(scriptName, "Sending message to background.js")
            chrome.runtime.sendMessage(request["msgStr"], function (response) {
                console.log(scriptName, "Background send message response: ", response);
            });
        } else if (request["action"] === "controlVideoMute") {
            console.log(scriptName, "Muting youtube video")
            handler.mute();
        } else if (request["action"] === "controlVideoPlay") {
            console.log(scriptName, "PLaying youtube video")
            handler.play();
        }
    } else if (request["sender"] === "background") {
        console.log(scriptName, "Background server response: ", request["msgStr"])
    }
});