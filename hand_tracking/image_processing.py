import numpy as np
import cv2
import collections
from scipy import stats
import time
from filterpy.kalman import KalmanFilter
import pyautogui

# Haar-like features
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# General kernel shape
kernel = np.ones((5,5),np.uint8)

# Skin color segmentation
min_hsv = np.array([0, 58, 0], dtype=np.uint8)
max_hsv = np.array([33, 255, 255], dtype=np.uint8)

# Converts color frame to binary
def binarize_frame(frame):
    # Detect face in frame
    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    # Apply background subtraction and thresholding
    subtracted = background.apply(frame, learningRate=0)
    ret, binary = cv2.threshold(subtracted, 254, 255, cv2.THRESH_BINARY)
    # Erode and dilate
    morph = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    # Mask frame
    combined = cv2.bitwise_and(frame, frame, mask=morph)
    # Black out face ellipse
    if len(faces) > 0:
        largest = np.argmax([face[2] * face[3] for face in faces])
        x, y, w, h = faces[largest]
        cv2.ellipse(combined, ((x + w // 2, y + h // 2),(w, int(h * 1.8)), 0),0,-1)
    # Identify skin color segments
    skin = cv2.inRange(cv2.cvtColor(combined, cv2.COLOR_BGR2HSV), min_hsv, max_hsv)
    # Dilate and blur for robustness
    dilate = cv2.dilate(skin, kernel)
    gaussian = cv2.GaussianBlur(dilate, (5, 5), 0)
    return gaussian

# Returns most likely contour for hand
def estimate_hand(contours, width):
    # Only consider large contours
    large = [contour for contour in contours if cv2.contourArea(contour) > 1000]
    if len(large) < 1:
        return None
    # Compute probability as weighted average of contour center and area
    areas = np.array([cv2.contourArea(contour) for contour in large])
    positions = np.array([width - np.mean(contour, axis=0)[0][0] for contour in large])
    totals = 0 * areas + 0.9 * positions
    return large[np.argmax(totals)].squeeze()

cap = cv2.VideoCapture(0)

# Initialize background subtractor
background = cv2.createBackgroundSubtractorMOG2()

# FPS variables
start_time = time.time()
frames = 0

kalman_filter = KalmanFilter (dim_x=4, dim_z=2)
# Current state
kalman_filter.x = np.array([0, 0, 0, 0])
# State transition function
kalman_filter.F = np.array([[1, 1, 0, 0],
                [0 ,1, 0, 0],
                [0, 0, 1, 1],
                [0, 0, 0 ,1]])
# Measurement function
kalman_filter.H = np.array([[1, 0, 0, 0],
                            [0, 0, 1, 0]])
# Covariance
kalman_filter.P *= 1000
# Measurement function
kalman_filter.R = np.eye(2) * 800
# Process uncertainty
kalman_filter.Q = np.eye(4) * 2

state = collections.deque(5 * [0], 5)
n = 3
queue = collections.deque([0] * n, n)
text = "none"
previous = 0

frame_center = np.array([140, 240])
for i in range(n):
    queue.appendleft(frame_center)
pyautogui.FAILSAFE = False

control_method = "joystick"

while True:
    position = 0
    # Read frame
    ret, frame = cap.read()
    binary = binarize_frame(frame)
    # Identify contours of binary frame
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Guess hand contour
    hand = estimate_hand(contours, frame.shape[0])
    # Blank image to draw onto
    blank = np.zeros(frame.shape[:2], np.uint8)
    if hand is not None:
        cv2.drawContours(blank, [hand], -1, 255, -1)
        dist = cv2.distanceTransform(blank, cv2.DIST_L2, 3)
        center = np.unravel_index(dist.argmax(), dist.shape)
        radius = dist[center]
        center = (center[1], center[0])
        if radius > 20:
            # Predict and update Kalman filter
            kalman_filter.predict()
            kalman_filter.update(center)
            cv2.circle(frame, (int(kalman_filter.x[0]), int(kalman_filter.x[2])), 2, (255, 0, 0), 3)
            cv2.circle(frame, (int(kalman_filter.x[0]), int(kalman_filter.x[2])), int(radius), (255, 0, 0), 3)

            position = 2
            hull = cv2.convexHull(hand, returnPoints=False)
            defects = cv2.convexityDefects(hand, hull)
            if defects is not None:
                for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    if d > radius * 160:
                        start = hand[s]
                        end = hand[e]
                        far = hand[f]
                        if start[1] < far[1] and end[1] < far[1]:
                            position = 1
                            break

            # Joystick
            if control_method == "joystick":
                mouse_vector = center - frame_center
                cv2.line(frame, tuple(frame_center), center, (255, 0, 0), 2)
                haha = np.multiply(np.power(abs(mouse_vector), 1.75) * 0.01, np.sign(mouse_vector))
                # pyautogui.move(tuple(np.int32(haha)), _pause=False)
            
            # Relative
            if control_method == "relative":
                past = np.mean(np.array(queue), axis=0)
                acceleration = abs(center - past) * 0.005
                queue.appendleft(center)
                # pyautogui.move(tuple(np.int32((center - past) * acceleration)), _pause=False)

            # Absolute
            if control_method == "absolute":
                screen_size = pyautogui.size()
                camera_resolution = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                coord = (center[0] * screen_size[0] / camera_resolution[0], center[1] * screen_size[1] / camera_resolution[1])
                # pyautogui.moveTo(coord)
                
    state.appendleft(position)
    m = stats.mode(state)[0][0]
    if m == 0:
        text = "none"
        previous = 0
    elif m == 1:
        text = "open"
        previous = 1
    elif m == 2:
        text = "close"
        if previous != 2:
            previous = 2
            # pyautogui.click()
    
    cv2.circle(frame, tuple(frame_center), 50, (0, 255, 0), 3)
    cv2.putText(frame, "FPS: {:.2f}".format(frames / (time.time() - start_time)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_4)     
    cv2.putText(frame, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_4)
    cv2.imshow('frame', frame)
    frames += 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
