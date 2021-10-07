# User Research

### Dependencies
The Python scripts require MediaPipe and OpenCV to function and are packaged with PyInstaller. All three packages can be installed by running the following command.

```pip install mediapipe opencv-python pyinstaller```

### Creating an Executable
To create an executable of a Python script, run package.sh and pass in the file name. For example, palm_tracking.py can be packaged with the following command.

```./package.sh palm_tracking.py```