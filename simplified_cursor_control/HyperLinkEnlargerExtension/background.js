//background.js

var active = true;

chrome.action.onClicked.addListener(() => {
  active = !active;
  if (active) {
    chrome.action.setIcon({path: "/images/on.png"});
  } else {
    chrome.action.setIcon({path: "/images/off.png"});
  }
});

chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
  if (active && changeInfo.status == 'complete') {
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: setBackgroundColor,
    });
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: enlargeClickableArea,
    });
  }
})

function setBackgroundColor() {
  // g: Usual search result
  // qGXjvb: Ads on top of search results
  // usJj9c: Sublinks
  var testElements = document.querySelectorAll('.g, .qGXjvb, .usJj9c')
  var testDivs = Array.prototype.filter.call(testElements, function(testElement){
      return testElement.nodeName === 'DIV';
  });
  for(let i = 0; i < testDivs.length; i++) {
      // Set background color.
      testDivs[i].addEventListener("mouseover", function() {
          if (testDivs[i].className !== 'g') {
            testDivs[i].style.cursor = "pointer";
          }
          if (testDivs[i].className === 'usJj9c') {
              testDivs[i].style.backgroundColor = "#87CEEB";
          } else {
              testDivs[i].style.backgroundColor = "#d5def5";
          }
      });
      // Unset background color.
      testDivs[i].addEventListener("mouseleave", function() {
          testDivs[i].style.backgroundColor = "transparent";
      })
  }

  var mouseHover = document.querySelectorAll('.yuRUbf, .VwiC3b.yXK7lf.MUxGbd.yDYNvb.lyLwlc.lEBKkf')
  var mouseDivs = Array.prototype.filter.call(mouseHover, function(testElement){
      return testElement.nodeName === 'DIV';
  });
  for(let i = 0; i < mouseDivs.length; i++) {
    mouseDivs[i].addEventListener("mouseover", function() {
      mouseDivs[i].style.cursor = "pointer";
    });
  }
}

function enlargeClickableArea() {
  // Find hyperlink contained inside an element.
  $(".yuRUbf, .qGXjvb, .usJj9c").click(function(){
      console.log($(this))
      window.location=$(this).find("a").attr("href");
      return false;
 });
 // Find hyperlink of text field by finding its parent since text element does not contain a hyperlink.
 $(".VwiC3b.yXK7lf.MUxGbd.yDYNvb.lyLwlc.lEBKkf").click(function(){
      window.location=$($(this)[0].parentElement.parentElement.getElementsByTagName('a'))[0].getAttribute("href");
      return false;
 })
}