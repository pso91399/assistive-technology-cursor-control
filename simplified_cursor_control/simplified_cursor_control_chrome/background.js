//background.js

var nearestElement;
var hyperlinkEnlargerActive = false;
var buttonEnlargerActive = false;
var nearestElementActive = false;
var remindPopupActive = false;

chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.local.set({ hyperlinkEnlargerActive: hyperlinkEnlargerActive });
    chrome.storage.local.set({ buttonEnlargerActive });
    chrome.storage.local.set({ nearestElementActive });
    chrome.storage.local.set({ remindPopupActive });
});

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {

    // check whether hyperlink enlarger function is active
    chrome.storage.local.get("hyperlinkEnlargerActive", ({ hyperlinkEnlargerActive }) => {
        if (hyperlinkEnlargerActive && changeInfo.status == 'complete') {
            chrome.scripting.executeScript({
                target: { tabId: tab.id },
                function: setBackgroundColor,
            });
            chrome.scripting.executeScript({
                target: { tabId: tab.id },
                function: enlargeClickableArea,
            });
        }
    });

    // check whether button enlarger function is active
    chrome.storage.local.get("buttonEnlargerActive", ({ buttonEnlargerActive }) => {
        if (buttonEnlargerActive && changeInfo.status == 'complete') {
            chrome.scripting.executeScript({
                target: { tabId: tab.id },
                function: enlargeButton,
            });
        }
    });
    
    // check whether nearest element function is active
    chrome.storage.local.get("nearestElementActive", ({ nearestElementActive }) => {
        if (nearestElementActive && changeInfo.status == 'complete') {
            chrome.scripting.executeScript({
                target: { tabId: tab.id },
                function: highlightNearestElement,
            });
            chrome.scripting.executeScript({
                target: { tabId: tab.id },
                function: activateNearestElement,
            });
        }
    });

    chrome.storage.local.get("remindPopupActive", ({ remindPopupActive }) => {
        if (remindPopupActive && changeInfo.status == 'complete') {
            chrome.scripting.executeScript({
                target: { tabId: tab.id },
                function: remindPopup,
            });
        }
    });
});


// Set background color of an element in order to indicate its clickable area has been enlarged
function setBackgroundColor() {
    // g: Usual search result
    // qGXjvb: Ads on top of search results
    // usJj9c: Sublinks
    var testElements = document.querySelectorAll('.g, .qGXjvb, .usJj9c')
    var testDivs = Array.prototype.filter.call(testElements, function (testElement) {
        return testElement.nodeName === 'DIV';
    });
    for (let i = 0; i < testDivs.length; i++) {
        testDivs[i].addEventListener(
            "mouseover",
            function () {
                // Set cursor style.
                if (testDivs[i].className === 'usJj9c') {
                    testDivs[i].style.cursor = "pointer";
                }
                // Set background color.
                if (testDivs[i].className === 'usJj9c') {
                    testDivs[i].style.backgroundColor = "#87CEEB";
                } else {
                    testDivs[i].style.backgroundColor = "#d5def5";
                }
            },
            {
                passive: true
            }
        );
        // Unset background color.
        testDivs[i].addEventListener(
            "mouseleave",
            function () {
                testDivs[i].style.backgroundColor = "transparent";
            },
            {
                passive: true,
            }
        );
    }

    var mouseHover = document.querySelectorAll('.yuRUbf, .VwiC3b.yXK7lf.MUxGbd.yDYNvb.lyLwlc.lEBKkf, .aCOpRe.ljeAnf')
    for (let i = 0; i < mouseHover.length; i++) {
        mouseHover[i].addEventListener(
            "mouseover",
            function () {
                mouseHover[i].style.cursor = "pointer";
            },
            {
                passive: true,
            }
        );
    }
}

// Make an area clickable which contains hyperlink as its sub-element
function enlargeClickableArea() {
    // Find hyperlink contained inside an element.
    $(".yuRUbf, .qGXjvb, .usJj9c").click(function () {
        window.location = $(this).find("a").attr("href");
        return false;
    });
    // Find hyperlink of text field by finding its parent since text element does not contain a hyperlink.
    $(".VwiC3b.yXK7lf.MUxGbd.yDYNvb.lyLwlc.lEBKkf, .aCOpRe.ljeAnf").click(function () {
        window.location = $($(this)[0].parentElement.parentElement.getElementsByTagName('a'))[0].getAttribute("href");
        return false;
    })
}

// Highlight element with tag 'a' that is nearest to cursor position in Euclidian space
function highlightNearestElement() {
    // Find all links with tag 'a'.
    let links = Array.from(document.querySelectorAll('a'));

    // Get coordination of the center of link rectangle.
    let linkCoords = links.map(link => {
        let rect = link.getBoundingClientRect();
        return [rect.x + rect.width / 2, rect.y + rect.height / 2];
    });

    let prevIdx = -1;  // Initialize to -1 means no previous link is highlighted
    var prevOutline;

    // Highlight nearest element when pointer moves.
    document.addEventListener(
        "pointermove",
        ev => {
            let distances = [];

            // Calculate distance between center of each link rectangle and cursor.
            linkCoords.forEach(linkCoord => {
                let distance = Math.hypot(linkCoord[0] - parseInt(ev.pageX), linkCoord[1] - parseInt(ev.pageY));
                distances.push(parseInt(distance));
            });

            // Get the index of nearest element.
            let closestLinkIndex = distances.indexOf(Math.min(...distances));

            if (prevIdx != closestLinkIndex) {
                // If there is a previous link rectangle that is highlighted by outline,
                // resume its outline to previous one.
                if (prevIdx >= 0) {
                    links[prevIdx].style.outline = prevOutline;
                }

                // Record current highlighted link rectangle as next iteration's prev
                prevOutline = links[closestLinkIndex].style.outline;
                prevIdx = closestLinkIndex;

                // Highlight current nearest link rectangle by changing its outline
                links[closestLinkIndex].style.outline = '#C85C5C solid 3px';
                nearestElement = links[closestLinkIndex]
            }
        },
        {
            passive: true,
        }
    );
}

// Redirect mouse click event to the nearest element
function activateNearestElement() {
    document.addEventListener(
        "click",
        ev => {
            nearestElement.click()
        },
        {
            passive: true,
        }
    )
}

// Enlarge the button where the mouse is hover on
function enlargeButton() {
    let enlarge_button_string = `
        a, button, input[type="button"], input[type="submit"] { transition: all .2s ease-in-out; }
        a:hover, button:hover, input[type="button"]:hover, input[type="submit"]:hover { transform: scale(1.2); }
    `;
    const style = document.createElement('style');
    style.textContent = enlarge_button_string;
    document.head.append(style);
}

// Remind how to close a popup by blinking the background color between hightligh color (currently blue) and transparent
function remindPopup() {
    let lastDate = new Date();  // Timestamp of last backgroud color change
    let is_set = false;  // Whether backgroud color is set or not
    let threshold =300;  // Time interval of background blinking 
    document.addEventListener(
        "pointermove",
        ev => {
            let curDate = new Date();
            // Check whether a popup appears and the time interval is greater than or equal to threshold
            if (document.getElementsByClassName("login-modal-div") !== null && curDate - lastDate >= threshold) {
                if (!is_set) {  // Set background color to highlight color if current status is not set
                    document.getElementsByClassName("login-modal-div")[0].style.backgroundColor = "rgba(135, 206, 235, 0.5)";
                    is_set = ~is_set;
                } else {  // Set background color to transparent if current status is set
                    document.getElementsByClassName("login-modal-div")[0].style.backgroundColor = "rgba(0,0,0,0.0)";
                    is_set = ~is_set;
                }
                lastDate = new Date();
            }
            
        },
        {
            passive: true,
        }
    );

    // function pausecomp(millis) {
    //     var date = new Date();
    //     var curDate = null;
    //     do { curDate = new Date(); }
    //     while(curDate-date < millis);
    // }

    // function waitForElm(selector) {
    //     return new Promise(resolve => {
    //         if (document.querySelector(selector)) {
    //             return resolve(document.querySelector(selector));
    //         }
    
    //         const observer = new MutationObserver(mutations => {
    //             if (document.querySelector(selector)) {
    //                 resolve(document.querySelector(selector));
    //                 observer.disconnect();
    //             }
    //         });
    
    //         observer.observe(document.body, {
    //             childList: true,
    //             subtree: true
    //         });
    //     });
    // }

    // if (document.URL.includes("www.geeksforgeeks.org") ) {
    //     // console.log("in URL");
    //     // // const delay = ms => new Promise(res => setTimeout(res, ms));
    //     // // await delay(5000);
    //     // pausecomp(20000);
    //     document.getElementsByClassName("login-modal-div")[0].style.backgroundColor = "rgba(200,0,0,0.4)";
    //     // // waitForElm('.login-modal-div').then((elm) => {
    //     // //     console.log('Element is ready');
    //     // //     elm.style.backgroundColor = 'rgba(200,0,0,0.4)';
    //     // // });
    //     // console.log("after URL");

    //     // // $("body").children().each(function () {
    //     // //     $(this).html( $(this).html().replace(/display: block;/g,"display: none;") );
    //     // // });

    //     // $("body").children().each(function () {
    //     //     $(this).html( $(this).html().replace(/<div class=\\"login-modal-div\\" style=\\"display: block\\";><\/div>/g,
    //     //     '<div class="login-modal-div" style="display: block"; background-color: rgba(200, 0, 0, 0.4);></div>')
    //     //     );
    //     // });
        
    // }
}

