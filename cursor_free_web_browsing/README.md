# Cursor Free Web Browsing

## Installation

### Apple Sillicon

`pip3 install socketio flask_socketio websocket-client simple-websocket`

`pip3 install --upgrade setuptools`

`pip3 install pyautogui opencv-python mediapipe-silicon`

### Others

I don't have a x86 device on hand. I suppose you can install with the same commands above. The only thing needs to change is `mediapipe-sillicon` to `mediapipe`.

## Running

### Run server and MediaPipe client

`python3 ./MediaPipeServer/app.py`

`python3 ./MediaPipeServer/mediapipe_client.py`

 You should see your camera on and find a rectangle in the center of your screen.

### Load the extension

1. Launch Chrome, visit `chrome://extensions/`.
2. Follow the "Load Unpacked" part in this [link](https://webkul.com/blog/how-to-install-the-unpacked-extension-in-chrome/) to load this directory as an unpacked chrome extension.
3. Turn on the extension.
Click **Load Unpacked**.

Select `CursorFreeExtension` directory in your file system.

##Todo:

1. More accurate and portbale gesture recognition.
    - Why? 
    Accuracy is good but MediaPipe incorrectly classifies some gestures.
    MediaPipe is our prerequisite, heavy-weight library.
    - How? 
    Find a pretrained gesture classifier.
    Replace mediapipe with a real-time, easy to install gesture recognition framework.

2. User-friendly web browsing mode.
    - Why?
    Navigating the page by movement is a bit slow.
    - How?
    Inspired by Vimium, Vim-based keyboard browsing utilities.
    https://vimium.github.io/


3. More essential shortcuts
    - What do we have now?
    Video Control: play, next, mute
    Page Control: up, down
    Browser Control: forward, backward, close tab
    …

    - What else?
    Voice input (speech into text)
    Move half page down/up 
    Floating instruction reminder 
    Expand submenu