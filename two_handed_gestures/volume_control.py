from queue import LifoQueue
import cv2
import time
import numpy as np
import mediapipe as mp
import math
from pynput.keyboard import Key,Controller

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
 
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
 
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
 
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img
 
    def findPosition(self, img, handNo=0, draw=True):
 
        lmList = []
        z = []
        depth_mean = -1
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                z.append(cz)
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            depth_mean = abs(np.average(z))
        return lmList, depth_mean



################################
wCam, hCam = 1280, 720
################################
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

keyboard = Controller()
detector = handDetector(detectionCon=0.7)


last_angle=None
last_length=None



minAngle = 0
maxAngle = 180
angle    = 0
angleBar = 400
angleDeg = 0
minHand  = 50 #50
maxHand  = 300 #300

stack = []


while True:
    success, img = cap.read()
    if not success:
        break
    img = detector.findHands(img)
    lmList, depth = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
 
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
 
        cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        length_relative = 10 * math.hypot(x2 - x1, y2 - y1) / depth

        # smoothing
        # if len(stack) == 50:
        #     stack.pop()
        # stack.append(length_mean)
        # length_average = np.average(stack)


        # print(length)
 
        # Hand range 50 - 300
    
        # angle  = np.interp(length, [minHand, maxHand], [minAngle, maxAngle])
        # angleBar = np.interp(length, [minHand, maxHand], [400, 150])
        # angleDeg = np.interp(length, [minHand, maxHand], [0, 180])   # degree angle 0 - 180

        
       

        if last_length:
            if length_relative>last_length * 2:
                keyboard.press(Key.media_volume_up)
                keyboard.release(Key.media_volume_up)
                print("VOL UP")
            elif length_relative < last_length / 2:
                keyboard.press(Key.media_volume_down)
                keyboard.release(Key.media_volume_down)
                print("VOL DOWN")
        
        last_length=length_relative

        # print(int(length), angle)

        


 
        if length_relative < 20:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
            keyboard.press(Key.media_volume_mute)
            print("VOL MUTE")

        cv2.putText(img, f'{int(length_relative)} distance', (40, 90), cv2.FONT_HERSHEY_COMPLEX,
                2, (0, 9, 255), 3)      
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(angleBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    # cv2.putText(img, f'{int(angleDeg)} deg', (40, 90), cv2.FONT_HERSHEY_COMPLEX,
    #             2, (0, 9, 255), 3)
      
 
    cv2.imshow("Img", img)
    cv2.waitKey(1)