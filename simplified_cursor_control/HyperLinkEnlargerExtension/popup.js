let changeColor = document.getElementById("changeColor");
var isActive = false;

// When the button is clicked, inject functions into current page.
changeColor.addEventListener("click", async () => {
    isActive = !isActive;
    if (isActive) {
        changeColor.style.backgroundColor = "#8fbc8f";
    } else {
        chrome.storage.sync.get("color", ({ color }) => {
            changeColor.style.backgroundColor = color;
        });
    }

    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: setBackgroundColor,
    });
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: enlargeClickableArea,
    });
});

// The body of this function will be executed as a content script inside the current page.
function setBackgroundColor() {
    // g: Usual search result
    // qGXjvb: Ads on top of search results
    // usJj9c: Sublinks
    var testElements = document.querySelectorAll('.g, .qGXjvb, .usJj9c')
    var testDivs = Array.prototype.filter.call(testElements, function (testElement) {
        return testElement.nodeName === 'DIV';
    });
    for (let i = 0; i < testDivs.length; i++) {
        // Set background color.
        testDivs[i].addEventListener("mouseover", function () {
            if (testDivs[i].className === 'usJj9c') {
                testDivs[i].style.backgroundColor = "#87CEEB";
            } else {
                testDivs[i].style.backgroundColor = "#d5def5";
            }
        });
        // Unset background color.
        testDivs[i].addEventListener("mouseleave", function () {
            testDivs[i].style.backgroundColor = "transparent";
        })
    }
}

function enlargeClickableArea() {
    // Find hyperlink contained inside an element.
    $(".yuRUbf, .qGXjvb, .usJj9c").click(function () {
        window.location = $(this).find("a").attr("href");
        return false;
    });
    // Find hyperlink of text field by finding its parent since text element does not contain a hyperlink.
    $(".VwiC3b.yXK7lf.MUxGbd.yDYNvb.lyLwlc.lEBKkf").click(function () {
        window.location = $($(this)[0].parentElement.parentElement.getElementsByTagName('a'))[0].getAttribute("href");
        return false;
    })

    // $('.g').after(jQuery.parseHTML('<a href="https://www.apple.com/macbook-air/" data-ved="2ahUKEwj75-uIktfzAhXTLH0KHVbfAtwQtwJ6BAg-EAM" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.apple.com/macbook-air/&amp;ved=2ahUKEwj75-uIktfzAhXTLH0KHVbfAtwQtwJ6BAg-EAM">'));
    // $('.g').before(jQuery.parseHTML('</a>'));
    // $('.g').replaceWith('<a href="https://www.apple.com/macbook-air/" data-ved="2ahUKEwj75-uIktfzAhXTLH0KHVbfAtwQtwJ6BAg-EAM" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.apple.com/macbook-air/&amp;ved=2ahUKEwj75-uIktfzAhXTLH0KHVbfAtwQtwJ6BAg-EAM">' + $('.g').text() + '</a>');

    //     var testElements = document.getElementsByClassName("g");
    //     var testDivs = Array.prototype.filter.call(testElements, function(testElement){
    //         return testElement.nodeName === 'DIV';
    //     });
    // for(let i = 0; i < testDivs.length; i++) {
    //     testDivs[i].after(jQuery.parseHTML('<a href="https://www.apple.com/macbook-air/" data-ved="2ahUKEwj75-uIktfzAhXTLH0KHVbfAtwQtwJ6BAg-EAM" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.apple.com/macbook-air/&amp;ved=2ahUKEwj75-uIktfzAhXTLH0KHVbfAtwQtwJ6BAg-EAM">' + testDivs[i].outerHTML + '</a>'));
    // }
}

// UNUSED: Bring sub divs that lie inside class "g" and have hyperlink forward.
// function bringSubDivForward() {
    // var testElements = document.getElementsByClassName("P1usbc");  // HiHjCd, yuRUbf, tF2Cxc, VNLkW
    // var testDivs = Array.prototype.filter.call(testElements, function(testElement){
    //     return testElement.nodeName === 'DIV';
    // });
    // for(let i = 0; i < testDivs.length; i++) {
    //     testDivs[i].style.position = 'relative';
    //     // testDivs[i].style.zIndex = testDivs[i].parentNode.style.zIndex + 1;
    //     testDivs[i].style.zIndex = 1000;
    // }
// }
