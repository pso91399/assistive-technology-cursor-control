import cv2
import mediapipe as mp
import numpy as np
import pyautogui

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


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)
mode_mapping = {1: 'cursor', 2: 'scroll', 3: 'volume', 4: 'window'}

while cap.isOpened():
    success, image = cap.read()
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
            print(flip_hand(handedness))
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
            if flip_hand(handedness) == 'Right':
                right_hand = hand_gesture
                cv2.putText(image, 'right hand gesture: ' + str(right_hand),
                (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
            else:
                left_hand = hand_gesture
                cv2.putText(image, 'left hand gesture: ' + str(left_hand),
                (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
            print(flip_hand(handedness) + ' recognized hand gesture: ', hand_gesture)
        if left_hand in mode_mapping:
            mode = mode_mapping[left_hand]
            cv2.putText(image, 'mode: ' + mode, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
            if mode == 'scroll':
                if right_hand == 1:
                    pyautogui.press('up')
                elif right_hand == 'Arrow':
                    pyautogui.press('down')

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()