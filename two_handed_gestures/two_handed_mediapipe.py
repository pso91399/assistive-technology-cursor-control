import collections
import cv2
import time
import mediapipe as mp
import numpy as np
import pyautogui
import math
from pynput import keyboard
from pynput.keyboard import Controller, Key
import time

def get_structured_landmarks(landmarks):
        # global structuredLandmarks
        structured_landmarks = []
        for j in range(42):
            if (j % 2 == 1):
                structured_landmarks.append ( {'x': landmarks[j - 1] , 'y': landmarks[j]} )
        return structured_landmarks


def recognize_hand_gesture(landmarks, label):
        # global select_ges
        thumbState = 'UNKNOW'
        indexFingerState = 'UNKNOW'
        middleFingerState = 'UNKNOW'
        ringFingerState = 'UNKNOW'
        littleFingerState = 'UNKNOW'
        thumbRight = False
        thumbLeft = False
        recognizedHandGesture = None

        if (landmarks[4]['y'] < landmarks[3]['y'] < landmarks[5]['y'] < landmarks[9]['y'] < landmarks[13]['y'] <
                landmarks[17]['y'] and landmarks[6]['x'] < landmarks[7]['x']):
            print('Thumbs Up')

        elif (landmarks[4]['y'] > landmarks[3]['y'] > landmarks[5]['y'] > landmarks[9]['y'] > landmarks[13]['y'] >
              landmarks[17]['y'] and landmarks[6]['x'] < landmarks[7]['x']):
            print('Thumbs down')

        if label.strip() == 'Left':
            pseudoFixKeyPoint = landmarks[2]['x']

            if pseudoFixKeyPoint < landmarks[3]['x'] < landmarks[4]['x']:
                thumbState = 'OPEN'
            elif pseudoFixKeyPoint > landmarks[3]['x'] > landmarks[4]['x']:
                thumbState = 'CLOSE'
        else:
            pseudoFixKeyPoint = landmarks[2]['x']

            if pseudoFixKeyPoint < landmarks[3]['x'] < landmarks[4]['x']:
                thumbState = 'CLOSE'
            elif pseudoFixKeyPoint > landmarks[3]['x'] > landmarks[4]['x']:
                thumbState = 'OPEN'

        if (pseudoFixKeyPoint < landmarks[3]['x'] < landmarks[4]['x'] and landmarks[4]['x'] >
                landmarks[17]['x']):
            thumbRight = True
        elif (pseudoFixKeyPoint > landmarks[3]['x'] > landmarks[4]['x'] and landmarks[4]['x'] <
              landmarks[17]['x']):
            thumbLeft = True

        pseudoFixKeyPoint = landmarks[6]['y']
        if pseudoFixKeyPoint > landmarks[7]['y'] > landmarks[8]['y']:
            indexFingerState = 'OPEN'
        elif pseudoFixKeyPoint < landmarks[7]['y'] < landmarks[8]['y']:
            indexFingerState = 'CLOSE'

        pseudoFixKeyPoint = landmarks[10]['y']
        if pseudoFixKeyPoint > landmarks[11]['y'] > landmarks[12]['y']:
            middleFingerState = 'OPEN'
        elif pseudoFixKeyPoint < landmarks[11]['y'] < landmarks[12]['y']:
            middleFingerState = 'CLOSE'

        pseudoFixKeyPoint = landmarks[14]['y']
        if pseudoFixKeyPoint > landmarks[15]['y'] > landmarks[16]['y']:
            ringFingerState = 'OPEN'
        elif pseudoFixKeyPoint < landmarks[15]['y'] < landmarks[16]['y']:
            ringFingerState = 'CLOSE'

        pseudoFixKeyPoint = landmarks[18]['y']
        if pseudoFixKeyPoint > landmarks[19]['y'] > landmarks[20]['y']:
            littleFingerState = 'OPEN'
        elif pseudoFixKeyPoint < landmarks[19]['y'] < landmarks[20]['y']:
            littleFingerState = 'CLOSE'

        if thumbState == 'OPEN' and indexFingerState == 'OPEN' and middleFingerState == 'OPEN' and ringFingerState == 'OPEN' and littleFingerState == 'OPEN':
            # and '5' in select_ges:
            recognizedHandGesture = 5  # "FIVE"
            # pressKey ( ges_key['5'] )

        elif thumbState == 'CLOSE' and indexFingerState == 'OPEN' \
                and middleFingerState == 'OPEN' and ringFingerState == 'OPEN' \
                and littleFingerState == 'OPEN':
            #     and '4' in select_ges:
            # pressKey ( ges_key['4'] )

            # scrolling(landmarks[0]['x']*img_width,landmarks[0]['y']*img_height)
            #     slide(landmarks[0]['x']*img_width,landmarks[0]['y']*img_height,landmarks[9]['x']*img_width,landmarks[9]['y']*img_height)
            #     keyboard.press_and_release('Page Down')

            recognizedHandGesture = 4  # "FOUR"
        elif thumbState == 'CLOSE' and indexFingerState == 'OPEN' \
                and middleFingerState == 'OPEN' and ringFingerState == 'OPEN' \
                and littleFingerState == 'CLOSE':
            #     and '3' in select_ges:
            # pressKey ( ges_key['3'] )

            recognizedHandGesture = 3  # "THREE"

        elif thumbState == 'OPEN' and indexFingerState == 'OPEN' \
                and middleFingerState == 'CLOSE' and ringFingerState == 'CLOSE' \
                and littleFingerState == 'CLOSE':
            #     and '2' in select_ges:

            # pressKey ( ges_key['2'] )
            recognizedHandGesture = 'Arrow'  # "TWO"

        elif thumbState == 'CLOSE' and indexFingerState == 'CLOSE' \
                and middleFingerState == 'CLOSE' and ringFingerState == 'CLOSE' \
                and littleFingerState == 'CLOSE':
            #     and 'Fist' in select_ges:
            # pressKey ( ges_key['Fist'] )
            recognizedHandGesture = 'Fist'  # "FIST"

        elif thumbState == 'CLOSE' and indexFingerState == 'OPEN' \
                and middleFingerState == 'OPEN' and ringFingerState == 'CLOSE' \
                and littleFingerState == 'CLOSE':
            #     and 'Victory' in select_ges:
            # pressKey ( ges_key['Victory'] )
            recognizedHandGesture = 2  # "Victory"

        elif (
                thumbState == 'OPEN' and thumbLeft and indexFingerState == 'CLOSE' and middleFingerState == 'CLOSE' and ringFingerState == 'CLOSE' and littleFingerState == 'CLOSE'):
            recognizedHandGesture = 'Thumb Left'
        elif (
                thumbState == 'OPEN' and thumbRight and indexFingerState == 'CLOSE' and middleFingerState == 'CLOSE' and ringFingerState == 'CLOSE' and littleFingerState == 'CLOSE'):
            recognizedHandGesture = 'Thumb Right'


        elif thumbState == 'CLOSE' and indexFingerState == 'OPEN' \
                and middleFingerState == 'CLOSE' and ringFingerState == 'CLOSE' \
                and littleFingerState == 'CLOSE':
                # and '1' in select_ges:

            #     keyboard.press('Ctrl')
            # pressKey ( ges_key['1'] )  # ONE
            recognizedHandGesture = 1  # "1"
        else:
            #     print(landmarks[8]['x'], landmarks[8]['y'])
            #     pyautogui.moveTo(landmarks[8]['x']*1080*2, landmarks[8]['y']*1920*2, duration = 0.1)
            recognizedHandGesture = 0  # "UNKNOW"

        print(thumbState,
            indexFingerState,
            middleFingerState,
            ringFingerState,
            littleFingerState,)

        return recognizedHandGesture

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
    pyautogui.moveTo(center[0] * screen_width // width, center[1] * screen_height // height, _pause=False)

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
    
def volume_control(landmarks):
    Keyboard = Controller()
    last_length = None
    w, h = image.shape[1], image.shape[0]

    x1, y1 = int(landmarks[4]['x'] * w), int(landmarks[4]['y'] * h)
    print("X1 y1", x1, y1)
    x2, y2 = int(landmarks[8]['x'] * w), int(landmarks[8]['y'] * h)
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

    cv2.circle(image, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
    cv2.circle(image, (x2, y2), 15, (0, 0, 255), cv2.FILLED)
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 3)
    cv2.circle(image, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

    length = math.hypot(x2 - x1, y2 - y1)

    if last_length:
        if length>last_length:
            Keyboard.press(Key.media_volume_up)
            Keyboard.release(Key.media_volume_up)
            print("VOL UP")
        elif length<last_length:
            Keyboard.press(Key.media_volume_down)
            Keyboard.release(Key.media_volume_down)
            print("VOL DOWN")
    
    last_length = length

    if length < 50:
        cv2.circle(image, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
        Keyboard.press(Key.media_volume_mute)
        Keyboard.release(Key.media_volume_mute)

    cv2.putText(image, f'{int(length)} distance', (40, 90), cv2.FONT_HERSHEY_COMPLEX,
                2, (0, 9, 255), 3) 


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)
mode_mapping = {1: 'cursor', 2: 'scroll', 3: 'volume', 4: 'window', 5: 'safari', 'Arrow': 'keyboard'}
time_start = None
keyboard_mode = False
prev_key = None
center_queue = collections.deque(5 * [(0, 0)], 5)

success, image = cap.read()
screen_width, screen_height = pyautogui.size()
height, width = image.shape[:2]
joystick_center = np.array([int(0.75 * width), int(0.5 * height)])
joystick_radius = 40

pyautogui.FAILSAFE = False
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
        right_hand, right_landmarks = None, None
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
                landmark_data.append(point.x)
                landmark_data.append(point.y)
            hand_gesture = recognize_hand_gesture(get_structured_landmarks(landmark_data), handedness)
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
            if mode == 'scroll' and not keyboard_mode:
                if right_hand == 1:
                    # pyautogui.press('up')
                    pyautogui.scroll(5)
                elif right_hand == 'Arrow':
                    pyautogui.press('down')
                    # pyautogui.press('down')
                    pyautogui.scroll(-5)
                elif right_hand == 2:
                    pyautogui.hscroll(10)
                elif right_hand == 3:
                    pyautogui.hscroll(-10) 
            elif mode == 'cursor' and not keyboard_mode and right_landmarks:
                keypoints = hand_keypoints(right_landmarks)
                center, radius = palm_center(keypoints)
                center_queue.appendleft(center)
                center = np.mean(center_queue, axis=0)
                absolute(center)
                # joystick(center, image)

                cv2.circle(image, tuple(np.int32(center)), 2, (0, 255, 0), 2)
                cv2.circle(image, tuple(np.int32(center)), radius, (0, 255, 0), 2)
                cv2.circle(image, tuple(joystick_center), joystick_radius, (255, 0, 0), 2)

                if right_hand == 1:
                    pyautogui.click()
                elif right_hand == 2:
                    pyautogui.doubleClick()
                elif right_hand == 'Arrow':
                    pyautogui.rightClick()
            elif mode == 'volume' and not keyboard_mode:
                keyboard = Controller()
                if right_hand == 1:
                    keyboard.tap(Key.media_volume_up)
                    time.sleep(0.3)
                elif right_hand == 'Arrow':
                    keyboard.tap(Key.media_volume_down)
                    time.sleep(0.3)
                elif right_hand == 2:
                    keyboard.tap(Key.media_volume_mute)
            elif mode == 'window' and not keyboard_mode:
                if right_hand == 1: #switch to previous app
                    pyautogui.hotkey('command', 'tab')
                elif right_hand == 2: #browse windows
                    pyautogui.hotkey('ctrl', 'up')
                elif right_hand == 3: #minimize active window
                    pyautogui.hotkey('command', 'm')
            elif mode == 'safari' and not keyboard_mode:
                if time_start is None:
                    time_start = time.time()
                time_stamp = time.time()
                if (time_stamp - time_start > 1):
                    time_start = time_stamp
                    Keyboard = Controller()
                    if right_hand == 1: # new tab
                        Keyboard.press(Key.cmd)
                        Keyboard.press('t')
                        Keyboard.release('t')
                        Keyboard.release(Key.cmd)
                        #time.sleep(0.5)
                    
                    if right_hand == 2: # address bar
                        Keyboard.press(Key.cmd)
                        Keyboard.press('l')
                        Keyboard.release('l')
                        Keyboard.release(Key.cmd)
                        #time.sleep(0.5)

                    if right_hand == 4: # decrease text size
                        Keyboard.press(Key.cmd)
                        Keyboard.press('-')
                        Keyboard.release('-')
                        Keyboard.release(Key.cmd)
                        #time.sleep(0.5)
                    
                    if right_hand == 5: # increase text size
                        Keyboard.press(Key.cmd)
                        Keyboard.press('+')
                        Keyboard.release('-')
                        Keyboard.release(Key.cmd)
                        #time.sleep(0.5)
                        
                        
                    if right_hand == 'Arrow': # switch tab
                        Keyboard.press(Key.ctrl)
                        Keyboard.press(Key.tab)
                        Keyboard.release(Key.tab)
                        Keyboard.release(Key.ctrl)
                        #time.sleep(0.5)
                    
                    if right_hand == 3: #close tab
                        Keyboard.press(Key.cmd)
                        Keyboard.press('w')
                        Keyboard.release('w')
                        Keyboard.release(Key.cmd)
                        #time.sleep(0.5)
            elif mode == 'keyboard':
                if time_start is None:
                    time_start = time.time()
                time_stamp = time.time()
                if (time_stamp - time_start > 1):
                    time_start = time_stamp
                    if keyboard_mode:
                        keyboard_mode = False
                    else:
                        keyboard_mode = True
            elif keyboard_mode:
                letter_mappings = {'cursor': 'a b c d e', 'scroll': 'f g h i j', 'volume': 'k l m n o', 'window': 'p q r s t', 'safari': 'u v w x y z'}
                cv2.putText(image, letter_mappings[mode],
                (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
                if time_start is None:
                    time_start = time.time()
                time_stamp = time.time()
                if (time_stamp - time_start > 1):
                    time_start = time_stamp
                    Keyboard = Controller()
                    if mode == 'cursor':
                        if right_hand == 1:
                            Keyboard.press('a')
                        elif right_hand == 2:
                            Keyboard.press('b')
                        elif right_hand == 3:
                            Keyboard.press('c')
                        elif right_hand == 4:
                            Keyboard.press('d')
                        elif right_hand == 5:
                            Keyboard.press('e')
                    elif mode == 'scroll':
                        if right_hand == 1:
                            Keyboard.press('f')
                        elif right_hand == 2:
                            Keyboard.press('g')
                        elif right_hand == 3:
                            Keyboard.press('h')
                        elif right_hand == 4:
                            Keyboard.press('i')
                        elif right_hand == 5:
                            Keyboard.press('j')
                    elif mode == 'volume':
                        if right_hand == 1:
                            Keyboard.press('k')
                        elif right_hand == 2:
                            Keyboard.press('l')
                        elif right_hand == 3:
                            Keyboard.press('m')
                        elif right_hand == 4:
                            Keyboard.press('n')
                        elif right_hand == 5:
                            Keyboard.press('o')
                    elif mode == 'window':
                        if right_hand == 1:
                            Keyboard.press('p')
                        elif right_hand == 2:
                            Keyboard.press('q')
                        elif right_hand == 3:
                            Keyboard.press('r')
                        elif right_hand == 4:
                            Keyboard.press('s')
                        elif right_hand == 5:
                            Keyboard.press('t')
                    elif mode == 'safari':
                        if right_hand == 1:
                            Keyboard.press('u')
                        elif right_hand == 2:
                            Keyboard.press('v')
                        elif right_hand == 3:
                            Keyboard.press('w')
                        elif right_hand == 4:
                            Keyboard.press('x')
                        elif right_hand == 5:
                            Keyboard.press('y')
                        elif right_hand == 'Arrow':
                            Keyboard.press('z')
                        elif right_hand == 'Thumb Left':
                            pyautogui.press('backspace')
                        elif right_hand == 'Fist':
                            pyautogui.press('enter')
            cv2.putText(image, 'keyboard mode: ' + ('on' if keyboard_mode else 'off'),
                (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
            

                

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()