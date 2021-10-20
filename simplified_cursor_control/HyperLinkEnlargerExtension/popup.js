let changeColor = document.getElementById("changeColor");
var isActive = false;

// When the button is clicked, inject setPageBackgroundColor into current page
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
    var testElements = document.getElementsByClassName("g");
    var testDivs = Array.prototype.filter.call(testElements, function(testElement){
        return testElement.nodeName === 'DIV';
    });
    for(let i = 0; i < testDivs.length; i++) {
        testDivs[i].addEventListener("mouseover", function() {
            testDivs[i].style.backgroundColor = "#d5def5";
            //console.log("set");
        });
        testDivs[i].addEventListener("mouseleave", function() {
            testDivs[i].style.backgroundColor = "transparent";
            //console.log("unset");
        })
    }
}

function enlargeClickableArea() {
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
    
    $(".g").click(function(){
        window.location=$(this).find("a").attr("href");
        return false;
   });
}
