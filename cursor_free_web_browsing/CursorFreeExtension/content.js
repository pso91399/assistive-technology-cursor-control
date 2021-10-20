// Page specific code here
const scriptName = "content.js: ";

class VideoHandler {
    mute(player) {
        if (!player.muted) {
            player.muted = true;
            console.log(scriptName, "Muted!")
        } else {
            player.muted = false;
            console.log(scriptName, "Unmuted!")
        }
    }

    play(player) {
        if (player.paused) {
            player.play();
        } else {
            player.pause();
        }
    }

    forward(player) {
        player.currentTime += 5;
    }

    backward(player) {
        player.currentTime -= 5;
    }
}


chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    let handler = new VideoHandler();
    let player = document.getElementsByTagName("video")[0];
    actionDictionary = {
        "controlVideoMute": handler.mute,
        "controlVideoPlay": handler.play,
        "controlVideoForward": handler.forward,
        "controlVideoBackward": handler.backward
    };

    if (request["action" === "sendMessage"]) {
        console.log(scriptName, "Sending message to background.js")
        chrome.runtime.sendMessage(request["msgStr"], function (response) {
            console.log(scriptName, "Background send message response: ", response);
        });
    } else if (request["action"] === "receiveMessage") {
        console.log(scriptName, "Sender: ", request["sender"], "Content: ", request["msgStr"])
    } else {
        console.log(scriptName, "action: ", request["action"]);
        actionDictionary[request["action"]](player);
    }
});