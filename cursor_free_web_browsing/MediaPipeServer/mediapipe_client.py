import time
import pyautogui
import numpy as np
import mediapipe as mp
import cv2
import collections
import socketio
import threading
from threading import Timer

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://127.0.0.1:1998',
            transports='websocket', namespaces='/mediapipe')


cursor_control = "absolute"
clicking_enabled = False
modeSwitchState = True
ctrlSwitchState = True
state = 0
mode = ["Standby Mode", "Interactive Mode", "Control Mode"]
# MediaPipe Hands Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

pyautogui.FAILSAFE = False

# Organizes landmarks into NumPy array


def timeout(): 
    global modeSwitchState
    global ctrlSwitchState
    modeSwitchState = True
    ctrlSwitchState = True

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

        if label.strip() == 'Left':
            pseudoFixKeyPoint = landmarks[2][0]

            if pseudoFixKeyPoint < landmarks[3][0] < landmarks[4][0]:
                thumbState = 'OPEN'
            elif pseudoFixKeyPoint > landmarks[3][0] > landmarks[4][0]:
                thumbState = 'CLOSE'
        else:
            pseudoFixKeyPoint = landmarks[2][0]

            if pseudoFixKeyPoint < landmarks[3][0] < landmarks[4][0]:
                thumbState = 'CLOSE'
            elif pseudoFixKeyPoint > landmarks[3][0] > landmarks[4][0]:
                thumbState = 'OPEN'

        if (pseudoFixKeyPoint < landmarks[3][0] < landmarks[4][0] and landmarks[4][0] >
                landmarks[17][0]):
            thumbRight = True
        elif (pseudoFixKeyPoint > landmarks[3][0] > landmarks[4][0] and landmarks[4][0] <
              landmarks[17][0]):
            thumbLeft = True

        pseudoFixKeyPoint = landmarks[6][1]
        if pseudoFixKeyPoint > landmarks[7][1] > landmarks[8][1]:
            indexFingerState = 'OPEN'
        elif pseudoFixKeyPoint < landmarks[7][1] < landmarks[8][1]:
            indexFingerState = 'CLOSE'

        pseudoFixKeyPoint = landmarks[10][1]
        if pseudoFixKeyPoint > landmarks[11][1] > landmarks[12][1]:
            middleFingerState = 'OPEN'
        elif pseudoFixKeyPoint < landmarks[11][1] < landmarks[12][1]:
            middleFingerState = 'CLOSE'

        pseudoFixKeyPoint = landmarks[14][1]
        if pseudoFixKeyPoint > landmarks[15][1] > landmarks[16][1]:
            ringFingerState = 'OPEN'
        elif pseudoFixKeyPoint < landmarks[15][1] < landmarks[16][1]:
            ringFingerState = 'CLOSE'

        pseudoFixKeyPoint = landmarks[18][1]
        if pseudoFixKeyPoint > landmarks[19][1] > landmarks[20][1]:
            littleFingerState = 'OPEN'
        elif pseudoFixKeyPoint < landmarks[19][1] < landmarks[20][1]:
            littleFingerState = 'CLOSE'

        if thumbState == 'OPEN' and indexFingerState == 'OPEN' and middleFingerState == 'OPEN' and ringFingerState == 'OPEN' and littleFingerState == 'OPEN':
            # and '5' in select_ges:
            recognizedHandGesture = 5  # "FIVE"
            # pressKey ( ges_key['5'] )

        elif thumbState == 'CLOSE' and indexFingerState == 'OPEN' \
                and middleFingerState == 'OPEN' and ringFingerState == 'OPEN' \
                and littleFingerState == 'OPEN':

            recognizedHandGesture = 4  # "FOUR"
        elif thumbState == 'CLOSE' and indexFingerState == 'OPEN' \
                and middleFingerState == 'OPEN' and ringFingerState == 'OPEN' \
                and littleFingerState == 'CLOSE':

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
            recognizedHandGesture = 0  # "UNKNOW"

        print(thumbState,
            indexFingerState,
            middleFingerState,
            ringFingerState,
            littleFingerState,)

        return recognizedHandGesture
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
    avg_points =np.array(keypoints[:, :2])
    avg_2d = np.std(avg_points, axis=0)
    area, x, y, combination = shoelace_area(points)
    center_x = np.sum(x * combination) / (6 * area)
    center_y = np.sum(y * combination) / (6 * area)
    center = np.array([center_x, center_y])
    radius = int(np.min(np.linalg.norm(points - center, axis=1))
                 * np.mean(frame.shape[:2]))
    center = tuple(np.int32(center * frame.shape[1::-1]))
    return center, radius, avg_2d

def process_line(center, history):
    message = ''
    if not history: 
        return ""
    scale = 3
    verstaticThrehold = 50
    hrzstaticThrehold = 80
    lastx, lasty = history[0], history[1]
    x, y = center[0], center[1]
    diffx, diffy = abs(lastx - x), abs(lasty - y)
    if diffx > diffy and diffx > hrzstaticThrehold:
        if diffx > scale*diffy:
            if x > lastx:
                message = 'forward'
            else:
                message = 'backward'
    elif diffx < diffy and diffy > verstaticThrehold:
        if diffy > scale*diffx:
            if y > lasty:
                message = 'pgdn'
            else:
                message = 'pgup'
    return message

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

def interactive_mode_recognition(center, w, h, startWidth, startHeight, keypoints):
    x, y = center[0], center[1]
    if recognize_hand_gesture(keypoints, 'Right')== 1 or recognize_hand_gesture(keypoints, 'Right')== 2:
        message = "Click"
        print(message)
    else:
        if x < w + startWidth and x > w - startWidth and y > h-startHeight and y < h + startHeight:
            message = "Pause"
        elif y < h-startHeight:
            message = "Up"
        elif y > h + startHeight:        
            message = "Down"
        elif x < w + startWidth:
            message  = "Left"
        else:
            message = "Right"
    return message


def control_mode_recognition(center, keypoint, history):
    message = ""
    if (keypoint[4][1] < keypoint[3][1] < keypoint[5][1] < keypoint[9][1] < keypoint[13][1] <
            keypoint[17][1] and keypoint[6][0] < keypoint[7][0]):
        message = "play"

    elif (keypoint[4][1] > keypoint[3][1] > keypoint[5][1] > keypoint[9][1] > keypoint[13][1] >
            keypoint[17][1] and keypoint[6][0] < keypoint[7][0]):
        message = "close"
    else:
        message = process_line(center, history)
    if not message:
        if recognize_hand_gesture(keypoints, "Right") == "Arrow":
            message = "next"

    return message


def convertTuple(tup):
    ans = ""
    for item in tup:
        ans += str(item)
        ans += ' '
    return ans


def get_current_milli_time():
    return round(time.time() * 1000)


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
history = None
last_send_time = get_current_milli_time()
while True:
    _, frame = cap.read()
    # Flip frame for correct handedness
    frame = cv2.flip(frame, 1)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.rectangle(frame, (width//2 - startWidth - 1, height//2 - startHeight-1),
                  (width//2 + startWidth - 1, height//2 + startHeight - 1), (30, 144, 255), 3)
   
    results = hands.process(img)
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        keypoints = hand_keypoints(hand_landmarks)
        center, radius , avg_2d= palm_center(keypoints)
        # message, history = process_pipeline(
        #     center, width//2, height//2, history, startWidth, startHeight, closeWidth, closeHeight)
        current_time = get_current_milli_time()
        #if we grab the fist and it is legal to change gesture
        if recognize_hand_gesture(keypoints, "Right") == "Fist" and modeSwitchState:

        #if avg_2d[1] < 0.10 and modeSwitchState:
            state +=1
            modeSwitchState = False
            t = Timer(2.0, timeout)
            t.start()  
        cv2.putText(frame, mode[state%3], (10, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


        if current_time // 1000 != last_send_time // 1000 :
            if state%3 != 0:
                if state%3 == 1:
                    message = interactive_mode_recognition(center,width//2, height//2, startWidth, startHeight, keypoints)
                elif state%3 == 2:
                    message = control_mode_recognition(center, keypoints, history)
                    history = center
                    
                    #ctrlSwitchState = False
                    #t = Timer(1.0, timeout)
                    #t.start()  
                #if message and ctrlSwitchState:     
                if message :               
                    sio.send(message, namespace='/mediapipe')
                    last_send_time = current_time
                    cv2.putText(frame, message, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        #if current_time // 200 != last_send_time // 200 and state%3 == 2:
        #     history.append(center)

        relative_queue.appendleft(center)
        center_queue.appendleft(center)
        center = np.mean(center_queue, axis=0)

        # Cursor movement
        """if cursor_control == "joystick":
            joystick(center, frame)
        elif cursor_control == "relative":
            relative(center)
        elif cursor_control == "absolute":
            absolute(center)

        if clicking_enabled:
            mouse_command(keypoints, closed)"""

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
