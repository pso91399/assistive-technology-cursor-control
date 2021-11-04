import collections
import cv2
import mediapipe as mp
import numpy as np
import pyautogui

cursor_control = "absolute"
clicking_enabled = False

# MediaPipe Hands Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

pyautogui.FAILSAFE = False

# Organizes landmarks into NumPy array


def hand_keypoints(hand_landmarks):
    points = []
    for landmark in hand_landmarks.landmark:
        points.append([landmark.x, landmark.y, landmark.z])
    return np.array(points)


def shoelace_area(points):
    x0, y0 = np.hsplit(points, 2)
    points1 = np.roll(points, -1, axis=0)
    x1, y1 = np.hsplit(points1, 2)
    combination = x0 * y1 - x1 * y0
    area = np.sum(combination) / 2
    return area, x0 + x1, y0 + y1, combination


def palm_center(keypoints):
    indices = [0, 1, 5, 9, 13, 17]
    points = keypoints[indices, :2]
    area, x, y, combination = shoelace_area(points)
    center_x = np.sum(x * combination) / (6 * area)
    center_y = np.sum(y * combination) / (6 * area)
    center = np.array([center_x, center_y])
    radius = int(np.min(np.linalg.norm(points - center, axis=1))
                 * np.mean(frame.shape[:2]))
    center = tuple(np.int32(center * frame.shape[1::-1]))
    return center, radius


def joystick(center, frame):
    mouse_vector = center - joystick_center
    length = np.linalg.norm(mouse_vector)
    if length > joystick_radius:
        mouse_vector = mouse_vector / length * (length - joystick_radius)
        mouse_move = np.multiply(
            np.power(abs(mouse_vector), 1.75) * 0.05, np.sign(mouse_vector))
        pyautogui.move(tuple(np.int32(mouse_move)), _pause=False)
    cv2.line(frame, tuple(joystick_center), tuple(
        np.int32(center)), (255, 0, 0), 2)


relative_queue = collections.deque(10 * [(0, 0)], 10)


def relative(center):
    past = np.mean(np.array(relative_queue), axis=0)
    acceleration = abs(center - past)
    pyautogui.move(
        tuple(np.int32((center - past) * acceleration)), _pause=False)
    center_queue.appendleft(center)


def absolute(center):
    pyautogui.moveTo(center[0] * screen_width // width,
                     center[1] * screen_height // height, _pause=False)


def mouse_command(keypoints, closed):
    index_closed = keypoints[8, 1] > keypoints[7,
                                               1] or keypoints[8, 1] > keypoints[6, 1]
    middle_closed = keypoints[12, 1] > keypoints[11,
                                                 1] or keypoints[10, 1] > keypoints[9, 1]
    ring_closed = keypoints[16, 1] > keypoints[15,
                                               1] or keypoints[14, 1] > keypoints[13, 1]
    pinky_closed = keypoints[20, 1] > keypoints[19,
                                                1] or keypoints[18, 1] > keypoints[17, 1]
    if index_closed or middle_closed or ring_closed or pinky_closed:
        closed.appendleft(1)
    else:
        closed.appendleft(0)
    if sum(closed) == 5:
        pyautogui.click()


def process_pipeline(center, w, h, history, startWidth, startHeight, closeWidth, closeHeight):
    x, y = center[0], center[1]
    message = "No detected Gesture"
    if x < w + startWidth and x > w - startWidth and y > h-startHeight and y < h + startHeight:
        message = "Ready"
        history = []
    elif x < w + closeWidth and x > w - closeWidth and y > h - closeHeight and y < h + closeHeight:
        history.append(center)
        message = "Detecting"
    else:
        if history:
            head, tail = history[0], history[-1]
            history.append(center)
            if tail[0] - head[0] > 80:
                message = "Right"
            elif tail[0] - head[0] < -80:
                message = "Left"
            elif tail[1] - head[1] > 50:
                message = "Down"
            else:
                message = "Up"

    return message, history


def convertTuple(tup):
    ans = ""
    for item in tup:
        ans += str(item)
        ans += ' '
    return ans


cap = cv2.VideoCapture(0)

_, frame = cap.read()
screen_width, screen_height = pyautogui.size()
height, width = frame.shape[:2]
startWidth, startHeight = width//6, height//5
closeWidth, closeHeight = width//4, height//3
joystick_center = np.array([int(0.75 * width), int(0.5 * height)])
joystick_radius = 40

center_queue = collections.deque(5 * [(0, 0)], 5)

closed = collections.deque(5 * [0], 5)
history = []
while True:
    _, frame = cap.read()
    # Flip frame for correct handedness
    frame = cv2.flip(frame, 1)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.rectangle(frame, (width//2 - startWidth - 1, height//2 - startHeight-1),
                  (width//2 + startWidth - 1, height//2 + startHeight - 1), (30, 144, 255), 3)
    cv2.rectangle(frame, (width//2 - closeWidth - 1, height//2 - closeHeight-1),
                  (width//2 + closeWidth - 1, height//2 + closeHeight - 1), (30, 144, 255), 3)
    results = hands.process(img)
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        keypoints = hand_keypoints(hand_landmarks)
        center, radius = palm_center(keypoints)
        message, history = process_pipeline(
            center, width//2, height//2, history, startWidth, startHeight, closeWidth, closeHeight)
        cv2.putText(frame, message, (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        relative_queue.appendleft(center)
        center_queue.appendleft(center)
        center = np.mean(center_queue, axis=0)

        # Cursor movement
        if cursor_control == "joystick":
            joystick(center, frame)
        elif cursor_control == "relative":
            relative(center)
        elif cursor_control == "absolute":
            absolute(center)

        if clicking_enabled:
            mouse_command(keypoints, closed)

        cv2.circle(frame, tuple(np.int32(center)), 2, (0, 255, 0), 2)
        cv2.circle(frame, tuple(np.int32(center)), radius, (0, 255, 0), 2)
        cv2.rectangle(frame, (0, 0), (width - 1, height - 1), (0, 255, 0), 3)

    else:
        cv2.rectangle(frame, (0, 0), (width - 1, height - 1), (0, 0, 255), 3)

    if cursor_control == "joystick":
        cv2.circle(frame, tuple(joystick_center),
                   joystick_radius, (255, 0, 0), 2)
    cv2.imshow("MediaPipe Hands", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
