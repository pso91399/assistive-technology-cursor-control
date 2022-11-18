import mediapipe as mp
import numpy as np
import cv2
import pyautogui
from pynput import keyboard
from pynput.keyboard import Controller, Key

import collections
import time
import os
import re

import alignment
import util


def load_temp():
    confident_col = np.ones((21,1))
    templates = []
    templates_category = []
    # files = ["temp_data/arrow_temp.csv", "temp_data/fist_temp.csv","temp_data/five_temp.csv","temp_data/four_temp.csv","temp_data/one_temp.csv",]
    file_path = "./data/template_image_new_wide_data/"
    files = os.listdir(file_path)
    print(files)
    for file in files:
        name = re.findall(r'(\w+).', file)[0]
        temp = np.hstack((np.loadtxt(file_path + file, dtype = float, delimiter=','), confident_col))
        templates.append(temp)
        templates_category.append(name)
    return templates, templates_category

def recognize_hand_gesture(landmarks):
    confident_col = np.ones((21,1))
    landmark_data = np.array(landmarks)
    landmark_data = np.hstack((landmark_data, confident_col))
    best_score = 0.
    for pose, pose_category in zip(templates, templates_category):
        matrix, score = alignment.pose_affinematrix(landmark_data, pose, dst_area=1.0, hard=True)
        if score > 0:
            # valid `matrix`. default (dstH, dstW) is (1.0, 1.0)
            # matrix = get_resize_matrix(1.0, 1.0, dstW, dstH).dot(matrix)
            # scale = math.sqrt(matrix[0,0] ** 2 + matrix[0,1] ** 2)
            print(score)
            
            if score > best_score:
                category = pose_category
                best_score = score

    return category if score > 0.5 else 0


def flip_hand(handedness):
    if handedness == 'Right':
        return 'Left'
    else:
        return 'Right'

# organize landmarks for cursor control hand tracking
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
    radius = int(np.min(np.linalg.norm(points - center, axis=1)) * np.mean(image.shape[:2]))
    center = tuple(np.int32(center * image.shape[1::-1]))
    return center, radius

def absolute(center):
    scale = 2
    print("center:", center)
    x = center[0] * screen_width // (scale * width)
    y = center[1] * screen_height // (scale * height)
    print(x, y)
    pyautogui.moveTo(x, y, _pause=False)

def absolute_scale(center):
    start_point = [0.50 * width, 0.25 * height]
    scale = screen_width // (0.25 * width)
    #scale_y = screen_height // (0.5 * height)
    out_x = scale * (center[0] - start_point[0])
    out_y = scale * (center[1] - start_point[1])
    pyautogui.moveTo(out_x, out_y, _pause=False)


def joystick(center, frame):
    mouse_vector = center - joystick_center
    length = np.linalg.norm(mouse_vector)
    if length > joystick_radius:
        mouse_vector = mouse_vector - np.array([joystick_radius, joystick_radius])
        # mouse_vector = mouse_vector / length * (length - joystick_radius)
        # mouse_move = np.multiply(np.power(abs(mouse_vector), 1.75) * 0.05, np.sign(mouse_vector))
        pyautogui.move(np.int32(mouse_vector)[0], np.int32(mouse_vector)[1], _pause=False)
        print('mouse vector', mouse_vector)
    cv2.line(frame, tuple(joystick_center), tuple(np.int32(center)), (255, 0, 0), 2)
    


# mediapipe setup
mp_drawing, mp_drawing_styles = util.mediapipe_draw_setup()
hands, mp_hands = util.mediapipe_hand_setup()

# gesture recognition setup
templates, templates_category = util.load_temp()

# video streaming setup
cap = cv2.VideoCapture(0)


# mode_mapping = {1: 'cursor', 2: 'scroll', 3: 'volume', 4: 'window', 5: 'safari'}
mode_mapping = {"one_left": 'cursor', "two_left": 'scroll', "three_left": 'volume', "four_left": 'window', "five_left": 'safari'}

time_start = None
leftclick_start = None
rightclick_start = None
center_queue = collections.deque(5 * [(0, 0)], 5)

success, image = cap.read()
screen_width, screen_height = pyautogui.size()
height, width = image.shape[:2]
joystick_center = np.array([int(0.75 * width), int(0.5 * height)])
joystick_radius = 40

templates, templates_category = load_temp()

pyautogui.FAILSAFE = False

win_name = "hands"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)
while cap.isOpened():
    success, image = cap.read()
    image = cv2.flip(image, 1)
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        right_hand = None
        left_hand = None
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[i].classification[0].label
            print(handedness)
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            landmark_data = []
            for point in hand_landmarks.landmark:
                landmark_data.append([point.x, point.y])
            # hand_gesture = recognize_hand_gesture(get_structured_landmarks(landmark_data), handedness)
            hand_gesture = recognize_hand_gesture(landmark_data)
            if handedness == 'Right':
                right_hand = hand_gesture
                right_landmarks = hand_landmarks
                cv2.putText(image, 'right hand gesture: ' + str(right_hand),
                (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
            else:
                left_hand = hand_gesture
                left_landmarks = hand_landmarks
                cv2.putText(image, 'left hand gesture: ' + str(left_hand),
                (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
            print(handedness + ' recognized hand gesture: ', hand_gesture)
        if left_hand in mode_mapping:
            mode = mode_mapping[left_hand]
            cv2.putText(image, 'mode: ' + mode, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
            if mode == 'scroll':
                if right_hand == "one":
                    # pyautogui.press('up')
                    pyautogui.scroll(5)
                elif right_hand == 'arrow':
                    pyautogui.press('down')
                    # pyautogui.press('down')
                    pyautogui.scroll(-5)
                elif right_hand == "two":
                    pyautogui.hscroll(10)
                elif right_hand == "three":
                    pyautogui.hscroll(-10) 
            elif mode == 'cursor':
                keypoints = hand_keypoints(right_landmarks)
                center, radius = palm_center(keypoints)
                center_queue.appendleft(center)
                center = np.mean(center_queue, axis=0)
                #absolute(center)
                absolute_scale(center)
                scale = screen_width // (0.5 * width)
                #joystick(center, image)

                # center and palm tracking
                cv2.circle(image, tuple(np.int32(center)), 2, (0, 255, 0), 2)
                cv2.circle(image, tuple(np.int32(center)), radius, (0, 255, 0), 2)
                # cv2.circle(image, tuple(joystick_center), joystick_radius, (255, 0, 0), 2)

                # hand movement area
                # cv2.line(image, (0.5 * width, 0.25 * height), (0.5 * width, 0.75 * height), (0, 255, 0), 3)
                # cv2.line(image, (1 * width, 0.25 * height), (1 * width, 0.75 * height), (0, 255, 0), 3)
                # cv2.line(image, (0.5 * width, 0.25 * height), (1 * width, 0.25 * height), (0, 255, 0), 3)
                # cv2.line(image, (0.5 * width, 0.75 * height), (1 * width, 0.75 * height), (0, 255, 0), 3)
                cv2. rectangle(image, (int(0.50 * width), int(0.75 * height)), (int(0.80 * width), int(0.25 * height)), (0, 255, 0), 3)

                if right_hand == 'arrow':
                    if not leftclick_start:
                        leftclick_start = time.time()
                    elif time.time() - leftclick_start <= 1:
                        continue
                        # cv2.putText(image, "leftclick: %d" %( - (time.time() - leftclick_start)), (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
                    else:
                        leftclick_start = None
                        pyautogui.click()
                elif right_hand == "two":
                    pyautogui.doubleClick()
                elif right_hand == "one":
                    pyautogui.rightClick()
            elif mode == 'volume':
                keyboard = Controller()
                if time_start is None:
                    time_start = time.time()
                time_stamp = time.time()
                if (time_stamp - time_start > 1):
                    time_start = time_stamp
                    if right_hand == "one":
                        keyboard.tap(Key.media_volume_up)
                    elif right_hand == 'arrow':
                        keyboard.tap(Key.media_volume_down)
                    elif right_hand == "two":
                        keyboard.tap(Key.media_volume_mute)
            elif mode == 'window':
                if time_start is None:
                    time_start = time.time()
                time_stamp = time.time()
                if (time_stamp - time_start > 1):
                    time_start = time_stamp
                    if right_hand == "one": #switch to previous app
                        pyautogui.hotkey('command', 'tab')
                    elif right_hand == "two": #browse windows
                        pyautogui.hotkey('ctrl', 'up')
                    elif right_hand == "three": #minimize active window
                        pyautogui.hotkey('command', 'm')
            elif mode == 'safari':
                if time_start is None:
                    time_start = time.time()
                time_stamp = time.time()
                if (time_stamp - time_start > 1):
                    time_start = time_stamp
                    Keyboard = Controller()
                    if right_hand == "one": # new tab
                        Keyboard.press(Key.cmd)
                        Keyboard.press('t')
                        Keyboard.release('t')
                        Keyboard.release(Key.cmd)
                        #time.sleep(0.5)
                    
                    if right_hand == "two": # address bar
                        Keyboard.press(Key.cmd)
                        Keyboard.press('l')
                        Keyboard.release('l')
                        Keyboard.release(Key.cmd)
                        #time.sleep(0.5)

                    if right_hand == "four": # decrease text size
                        Keyboard.press(Key.cmd)
                        Keyboard.press('-')
                        Keyboard.release('-')
                        Keyboard.release(Key.cmd)
                        #time.sleep(0.5)
                    
                    if right_hand == "five": # increase text size
                        Keyboard.press(Key.cmd)
                        Keyboard.press('+')
                        Keyboard.release('-')
                        Keyboard.release(Key.cmd)
                        #time.sleep(0.5)
                        
                        
                    if right_hand == 'arrow': # switch tab
                        Keyboard.press(Key.ctrl)
                        Keyboard.press(Key.tab)
                        Keyboard.release(Key.tab)
                        Keyboard.release(Key.ctrl)
                        #time.sleep(0.5)
                    
                    if right_hand == "three": #close tab
                        Keyboard.press(Key.cmd)
                        Keyboard.press('w')
                        Keyboard.release('w')
                        Keyboard.release(Key.cmd)
                        #time.sleep(0.5)

                

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow(win_name, image)
    cv2.resizeWindow(win_name, 320, 180)
    
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()