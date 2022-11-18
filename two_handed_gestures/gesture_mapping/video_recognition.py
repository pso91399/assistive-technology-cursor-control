"""this file is used to classify different hand gestures on video streaming mode and is based on template keypoints"""
import numpy as np
import cv2
import mediapipe as mp
import os
import re
import alignment as alignment
from typing import List
import util

def video_recognition():
    # mediapipe setup
    mp_drawing, mp_drawing_styles = util.mediapipe_draw_setup()
    hands, mp_hands = util.mediapipe_hand_setup()
    # gesture recognition setup
    templates, templates_category = util.load_temp()
    # video streaming setup
    cap = cv2.VideoCapture(0)
    
    # loop start
    while cap.isOpened():
        # image shape: height * width = 720 * 1280, 9:16
        success, image = cap.read()
        image = cv2.flip(image, 1)
        if not success:
            print("Ignoring empty camera frame.")
            # streaming: continue; vedio: break
            continue
        # get hand keypoints
        mp_success, num_hands, results = util.mediapipe_process(image, hands)
        if mp_success:
            for i in range(num_hands):
                score, handedness, hand_landmarks = util.get_mediapipe_result(results, i)
                category = util.recognize_gesture(templates, templates_category, hand_landmarks)
                util.mediapipe_draw(image, hand_landmarks, mp_hands, mp_drawing, mp_drawing_styles)
                cv2.putText(image, 'pose: ' + category, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()

if __name__ == '__main__':
    video_recognition()