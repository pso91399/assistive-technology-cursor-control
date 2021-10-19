//background.js

let color = '#F0F0F0'

chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({ color });
    console.log('Default background color set to %cgray', `color: ${color}`);
})

var toggle = false;

chrome.action.onClicked.addListener((tab) => {
  toggle = !toggle;
  if (toggle) {
    chrome.action.setIcon({path: "/images/on.png", tabId: tab.id});
  } else {
    chrome.action.setIcon({path: "/images/off.png", tabId: tab.id});
  }
});
