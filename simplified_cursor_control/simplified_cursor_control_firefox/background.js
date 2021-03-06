//background.js

var nearestElement;
var hyperlink_enlarger_active = false;
var button_enlarger_active = false;
var nearest_element_active = false;

chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.local.set({ hyperlink_enlarger_active });
    chrome.storage.local.set({ button_enlarger_active });
    chrome.storage.local.set({ nearest_element_active });
});

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {

    chrome.storage.local.get("hyperlink_enlarger_active", ({ hyperlink_enlarger_active }) => {
        if (hyperlink_enlarger_active && changeInfo.status == 'complete') {
            chrome.tabs.executeScript({
                code: `
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
                `,
            });
            chrome.tabs.executeScript({
                code: `
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
                `,
            });
        }
    });
    
    chrome.storage.local.get("button_enlarger_active", ({ button_enlarger_active }) => {
        if (button_enlarger_active && changeInfo.status == 'complete') {
            chrome.tabs.executeScript({
                code: `
                let enlarge_button_string = \`
                a, button, input[type="button"], input[type="submit"] { transition: all .2s ease-in-out; }
                a:hover, button:hover, input[type="button"]:hover, input[type="submit"]:hover { transform: scale(1.2); }
                \`;
                const style = document.createElement('style');
                style.textContent = enlarge_button_string;
                document.head.append(style);
                `,
            });
        }
    });
    
    chrome.storage.local.get("nearest_element_active", ({ nearest_element_active }) => {
        if (nearest_element_active && changeInfo.status == 'complete') {
            chrome.tabs.executeScript({
                code: `
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
                `,
            });
            chrome.tabs.executeScript({
                code: `
                document.addEventListener(
                    "click",
                    ev => {
                        nearestElement.click()
                    },
                    {
                        passive: true,
                    }
                )
                `,
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



function enlargeButton() {
    let enlarge_button_string = `
        a, button, input[type="button"], input[type="submit"] { transition: all .2s ease-in-out; }
        a:hover, button:hover, input[type="button"]:hover, input[type="submit"]:hover { transform: scale(1.2); }
    `;
    const style = document.createElement('style');
    style.textContent = enlarge_button_string;
    document.head.append(style);
}