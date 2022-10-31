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

### Load the extension

Launch Chrome, visit `chrome://extensions/`.

Click **Load Unpacked**.

Select `CursorFreeExtension` directory in your file system.