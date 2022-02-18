// Page specific code here
const scriptName = "content.js: ";

// The following code adds a stub function before the document loading 
// to record addClickListener-like statements
let preInjectionCode = `
let elementsWithDynamicClick = new Set();

// Stub function to inject
function recordClickEvent(event, element) {
    if (event === "click") {
        elementsWithDynamicClick.add(element)
    }
}

Window.prototype._addEventListener = Window.prototype.addEventListener;
Window.prototype.addEventListener = function (a, b, c) {
    if (c == undefined) c = false;
    this._addEventListener(a, b, c);
    if (!this.eventListenerList) this.eventListenerList = {};
    if (!this.eventListenerList[a]) this.eventListenerList[a] = [];
    recordClickEvent(a, this);
    this.eventListenerList[a].push({ listener: b, options: c });
};

EventTarget.prototype._addEventListener = EventTarget.prototype.addEventListener;
EventTarget.prototype.addEventListener = function (a, b, c) {
    if (c == undefined) c = false;
    this._addEventListener(a, b, c);
    if (!this.eventListenerList) this.eventListenerList = {};
    if (!this.eventListenerList[a]) this.eventListenerList[a] = [];
    recordClickEvent(a, this);
    this.eventListenerList[a].push({ listener: b, options: c });
};

EventTarget.prototype._getEventListeners = function (a) {
    if (!this.eventListenerList) this.eventListenerList = {};
    if (a == undefined) { return this.eventListenerList; }
    return this.eventListenerList[a];
};
`;

let preInjectionScript = document.createElement('script');
preInjectionScript.textContent = preInjectionCode;
(document.head || document.documentElement).prepend(preInjectionScript);
preInjectionScript.parentNode.removeChild(preInjectionScript);

// The following code adds a stub function after the document loading 
// to get the ids of all clickable elements and send it to background.js
// then background.js will forward the message to content.js
let postInjectionCode = `
window.addEventListener("load", afterLoad, false);
function afterLoad(event) {
    let elements = document.body.getElementsByTagName("*");
    let index = 0;
    let prefix = "#global-clickable-id-";
    let clickableTags = new Set(["a", "input", "button"]);
    let clickableIds = [];
    
    for (let element of elements) {
        if (elementsWithDynamicClick.has(element) ||
            element.getAttribute('onclick') ||
            element.getAttribute('href') ||
            clickableTags.has(element.tagName)
        ) {
            if (!element.id ||
                element.id.includes("#temp-fake-id-")
            ) {
                element.id = (prefix + index);
                index++;
            }
            clickableIds.push(element.id);
        }
    }

    prefix = "#global-video-id-";
    index = 0;
    let videoIds = ["movie_player"];

    let extensionId = "gilogbcjbjgomknecgdapibjhjmnkmhd";
    chrome.runtime.sendMessage(extensionId, { "clickableIds": clickableIds, "videoIds": videoIds },
        function (response) {
            if (!response.success)
                console.err(response);
        }
    );
}

// window.addEventListener("message", receiveContentScriptMessage, false);

// function receiveContentScriptMessage(event) {
//     // We only accept messages from ourselves
//     if (event.source != window) {
//         return;
//     }

//     let message = event.data;
//     if (message.sender && (message.sender === "content")) {
//         document.getElementById(message.id).dispatchEvent(new Event('click'));
//     }
// }
`;

let postInjectionScript = document.createElement('script');
postInjectionScript.textContent = postInjectionCode;
(document.head || document.documentElement).appendChild(postInjectionScript);
postInjectionScript.parentNode.removeChild(postInjectionScript);

let clickableGrid = undefined;
let gridX = 0;
let gridY = 0;
let lastCSS = undefined;
let directions = { "up": [-1, 0], "down": [1, 0], "left": [0, -1], "right": [0, 1] };

function moveSelection(reqeust) {
    let direction = reqeust["direction"];
    let nextGridX = gridX + directions[direction][0];
    let nextGridY = gridY + directions[direction][1];
    if (nextGridX >= clickableGrid.length) {
        nextGridX = clickableGrid.length - 1;
    }
    if (nextGridX < 0) {
        nextGridX = 0;
    }
    if (nextGridY >= clickableGrid[nextGridX].length) {
        nextGridY = clickableGrid[nextGridX].length - 1;
    }
    if (nextGridY < 0) {
        nextGridY = 0;
    }
    if (nextGridX === gridX && nextGridY === gridY) {
        return;
    }

    // Restore the last selected element
    if (lastCSS !== -1) {
        let lastElement = document.getElementById(clickableGrid[gridX][gridY]["id"]);
        lastElement.style.backgroundColor = lastCSS;
    }
    // Select the new element
    gridX = nextGridX;
    gridY = nextGridY;
    let clickableElement = document.getElementById(clickableGrid[gridX][gridY]["id"]);
    // console.log(clickableElement);
    lastCSS = clickableElement.style.backgroundColor;
    clickableElement.style.backgroundColor = 'RED';
    //clickableElement.style.transform = "scale(1.25)";
}

function clickCurrentElement(reqeust) {
    if (gridX >= clickableGrid.length || gridX < 0 ||
        gridY >= clickableGrid[gridX].length || gridY < 0) {
        return;
    }
    let id = clickableGrid[gridX][gridY]["id"];
    document.getElementById(id).click();
}

function printCurrentElement(reqeust) {
    if (gridX >= clickableGrid.length || gridX < 0 ||
        gridY >= clickableGrid[gridX].length || gridY < 0) {
        return;
    }
    let id = clickableGrid[gridX][gridY]["id"];
    console.log("content.js", document.getElementById(id));
}

function playCurrentVideo(reqeust) {
    if (gridX >= clickableGrid.length || gridX < 0 ||
        gridY >= clickableGrid[gridX].length || gridY < 0) {
        return;
    }
    let id = clickableGrid[gridX][gridY]["id"];
    let element = document.getElementById(id);
    if (element.id === "movie_player") {
        console.log(element);
        for (let prop in element) {
            console.log(prop);
        }
        if (element.getPlayerState() === 2) { // Is paused
            element.playVideo();
        } else {
            element.pauseVideo();
        }
    }
}

function muteCurrentVideo(reqeust) {
    if (gridX >= clickableGrid.length || gridX < 0 ||
        gridY >= clickableGrid[gridX].length || gridY < 0) {
        return;
    }
    let id = clickableGrid[gridX][gridY]["id"];

    let element = document.getElementById(id);
    if (element.id === "movie_player") {
        if (element.isMuted()) {
            element.unMute();
        } else {
            element.mute();
        }
    }
}

function playNextVideo(reqeust) {
    if (gridX >= clickableGrid.length || gridX < 0 ||
        gridY >= clickableGrid[gridX].length || gridY < 0) {
        return;
    }
    let id = clickableGrid[gridX][gridY]["id"];

    let element = document.getElementById(id);
    if (element.id === "movie_player") {

    }
}

function testServerLoopback(reqeust) {
    console.log(scriptName, "testServerLoopback");
    chrome.runtime.sendMessage({ "sender": "content", "action": "testServerLoopback" });
}

function prepareClickablePosition(clickableIds, videoIds) {
    let absoluteClickablePositions = []
    // Compute x y position
    for (let i = 0; i < clickableIds.length; i++) {
        let id = clickableIds[i];
        let element = document.getElementById(id);
        let elementRectArray = element.getClientRects();
        if (elementRectArray.length === 0) {
            continue;
        }
        let elementRect = elementRectArray[0];
        let x = elementRect.top;
        let y = elementRect.left;
        absoluteClickablePositions.push({ "id": id, "x": x, "y": y });
    }

    // Compute x y position
    for (let i = 0; i < videoIds.length; i++) {
        let id = videoIds[i];
        let element = document.getElementById(id);
        let elementRectArray = element.getClientRects();
        if (elementRectArray.length === 0) {
            continue;
        }
        let elementRect = elementRectArray[0];
        let x = elementRect.top;
        let y = elementRect.left;
        absoluteClickablePositions.push({ "id": id, "x": x, "y": y });
    }

    // Sort by x y postion
    absoluteClickablePositions.sort(function (a, b) {
        let xA = a["x"];
        let yA = a["y"];
        let xB = b["x"];
        let yB = b["y"];
        if (xA == xB) {
            return yA > yB ? 1 : -1;
        }

        return xA > xB ? 1 : -1;
    });


    clickableGrid = new Array()
    let lastX = -1;
    for (let position of absoluteClickablePositions) {
        if (position["x"] !== lastX) {
            lastX = position["x"];
            clickableGrid.push(new Array());
        }
        clickableGrid.at(-1).push({ "id": position["id"] });
    }
    lastCSS = document.getElementById(clickableGrid[gridX][gridY]["id"]).style;
    console.log(clickableGrid);
    return clickableGrid;
}

function handlePageMessage(request) {
    console.log(scriptName, "Sender: ", request["sender"]);
    clickableGrid = prepareClickablePosition(request["clickableIds"], request["videoIds"]);
}

function handleServerMessage(request) {
    console.log(scriptName, "serverMessage: ", request["msgStr"]);
}

const popupHandler = {
    "move": moveSelection,
    "clickCurrentElement": clickCurrentElement,
    "printCurrentElement": printCurrentElement,
    "playCurrentVideo": playCurrentVideo,
    "muteCurrentVideo": muteCurrentVideo,
    "playNextVideo": playNextVideo,
    "testServerLoopback": testServerLoopback
};

const backgroundHandler = {
    "pageMessage": handlePageMessage,
};

const serverHandler = {
    "move": moveSelection,
    "click": clickCurrentElement
}

// Main entry of content.js code
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request["sender"] === "popup") {
        popupHandler[request["action"]](request);
    } else if (request["sender"] === "background") {
        backgroundHandler[request["action"]](request);
    } else if (request["sender"] === "server") {
        serverHandler[request["action"]](request);
    } else {
        console.log(scriptName, "Unknown message", request);
    }
});

