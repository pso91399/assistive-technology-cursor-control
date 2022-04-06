var hyperlink_enlarger_switch = document.getElementById("hyperlink_enlarger_switch");
var button_enlarger_switch = document.getElementById("button_enlarger_switch");
var nearest_element_switch = document.getElementById("nearest_element_switch");

chrome.storage.local.get(["hyperlink_enlarger_active", "button_enlarger_active", "nearest_element_active"], ({ hyperlink_enlarger_active, button_enlarger_active, nearest_element_active }) => {
    hyperlink_enlarger_switch.checked = hyperlink_enlarger_active;
    button_enlarger_switch.checked = button_enlarger_active;
    nearest_element_switch.checked = nearest_element_active;
});

hyperlink_enlarger_switch.addEventListener('change', function() {
    chrome.storage.local.set({ hyperlink_enlarger_active: this.checked });
});

button_enlarger_switch.addEventListener('change', function() {
    chrome.storage.local.set({ button_enlarger_active: this.checked });
});

nearest_element_switch.addEventListener('change', function() {
    chrome.storage.local.set({ nearest_element_active: this.checked });
});
