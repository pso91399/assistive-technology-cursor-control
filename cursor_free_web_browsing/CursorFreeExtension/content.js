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
Window.prototype.addEventListener = function(a, b, c) {
   if (c==undefined) c=false;
   this._addEventListener(a,b,c);
   if (! this.eventListenerList) this.eventListenerList = {};
   if (! this.eventListenerList[a]) this.eventListenerList[a] = [];
   recordClickEvent(a, this);
   this.eventListenerList[a].push({listener:b,options:c});
};

EventTarget.prototype._addEventListener = EventTarget.prototype.addEventListener;
EventTarget.prototype.addEventListener = function(a, b, c) {
   if (c==undefined) c=false;
   this._addEventListener(a,b,c);
   if (! this.eventListenerList) this.eventListenerList = {};
   if (! this.eventListenerList[a]) this.eventListenerList[a] = [];
   recordClickEvent(a, this);
   this.eventListenerList[a].push({listener:b,options:c});
};

EventTarget.prototype._getEventListeners = function(a) {
    if (! this.eventListenerList) this.eventListenerList = {};
    if (a==undefined)  { return this.eventListenerList; }
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
    let prefix = "#universal-fake-id-";
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
                index ++;
            }
            clickableIds.push(element.id);
        }
    }

    let extensionId = "iobeldeiocmfodmelocllpcagpjhilic";
        chrome.runtime.sendMessage(extensionId, { "clickableIds": clickableIds },
            function(response) {
                if (!response.success)
                    console.err(response);
            }
        );   
}
`;
let postInjectionScript = document.createElement('script');
postInjectionScript.textContent = postInjectionCode;
(document.head || document.documentElement).appendChild(postInjectionScript);
postInjectionScript.parentNode.removeChild(postInjectionScript);

let clickableIds = undefined;
let index = 0;
let lastCSS = -1;
let lastIndex = -1;

function nextClickable() {
    if (index === clickableIds.length - 1) {
        return;
    }

    if (lastCSS !== -1) {
        document.getElementById(clickableIds[lastIndex]).style.backgroundColor = lastCSS;
    }
    clickableElement = document.getElementById(clickableIds[index]);
    console.log(clickableElement);
    lastCSS = clickableElement.style.backgroundColor;
    clickableElement.style.backgroundColor = 'RED';
    lastIndex = index;
    index ++;
}


function prevClickable() {
    if (index === 0) {
        return;
    }

    if (lastCSS !== -1) {
        document.getElementById(clickableIds[lastIndex]).style.backgroundColor = lastCSS;
    }
    clickableElement = document.getElementById(clickableIds[index]);
    console.log(clickableElement);
    lastCSS = clickableElement.style.backgroundColor;
    clickableElement.style.backgroundColor = 'RED';
    lastIndex = index;
    index --;
}

// Main entry of content.js code
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request["action"] === "nextClickableElement") {
        nextClickable();
    } else if (request["action"] === "prevClickableElement") {
        prevClickable();
    } else if (request["action"] === "receiveMessage") {
        console.log(scriptName, "Sender: ", request["sender"])
        clickableIds = request["clickableIds"];
    } else {
        console.log(scriptName, "action: ", request["action"]);
    }
});
