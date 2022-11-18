var hyperlinkEnlargerSwitch = document.getElementById("hyperlink_enlarger_switch");
var buttonEnlargerSwitch = document.getElementById("button_enlarger_switch");
var nearestElementSwitch = document.getElementById("nearest_element_switch");
var remindPopupSwitch = document.getElementById("remind_popup_switch");

chrome.storage.local.get(["hyperlinkEnlargerActive", "buttonEnlargerActive", "nearestElementActive", "remindPopupActive"], ({ hyperlinkEnlargerActive, buttonEnlargerActive, nearestElementActive, remindPopupActive }) => {
    hyperlinkEnlargerSwitch.checked = hyperlinkEnlargerActive;
    buttonEnlargerSwitch.checked = buttonEnlargerActive;
    nearestElementSwitch.checked = nearestElementActive;
    remindPopupSwitch.checked = remindPopupActive;
});

hyperlinkEnlargerSwitch.addEventListener('change', function() {
    chrome.storage.local.set({ hyperlinkEnlargerActive: this.checked });
});

buttonEnlargerSwitch.addEventListener('change', function() {
    chrome.storage.local.set({ buttonEnlargerActive: this.checked });
});

nearestElementSwitch.addEventListener('change', function() {
    chrome.storage.local.set({ nearestElementActive: this.checked });
});

remindPopupSwitch.addEventListener('change', function() {
    chrome.storage.local.set({ remindPopupActive: this.checked });
})
