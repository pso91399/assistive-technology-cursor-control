import mediapipe as mp
import numpy as np
import cv2
import alignment
import os
import re


def mediapipe_hand_setup(min_detection_confidence=0.7):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=min_detection_confidence)
    return hands, mp_hands

def mediapipe_draw_setup():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    return mp_drawing, mp_drawing_styles

def mediapipe_process(image, hands):
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
        success = True
        num_hands = len(results.multi_hand_landmarks)
    else:
        success = False
        num_hands = 0
    return success, num_hands, results

def get_mediapipe_result(mp_result, id):
    score = mp_result.multi_handedness[id].classification[0].score
    handedness = mp_result.multi_handedness[id].classification[0].label
    hand_landmarks = mp_result.multi_hand_landmarks[id]
    return score, handedness, hand_landmarks

def mediapipe_draw(image, hand_landmarks, mp_hands, mp_drawing, mp_drawing_styles):
    mp_drawing.draw_landmarks(
        image,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style())

def load_temp(file_path=None):
    confident_col = np.ones((21,1))
    templates = []
    templates_category = []
    if not file_path:
        file_path = "./data/template_image_new_wide_data/"
    files = os.listdir(file_path)
    print(files)
    for file in files:
        name = re.findall(r'(\w+).', file)[0]
        temp = np.hstack((np.loadtxt(file_path + file, dtype = float, delimiter=','), confident_col))
        templates.append(temp)
        templates_category.append(name)
    return templates, templates_category

def recognize_gesture(templates, templates_category, hand_landmarks):
    landmark_data = []
    for point in hand_landmarks.landmark:
        landmark_data.append([point.x, point.y])
    confident_col = np.ones((21,1))
    landmark_data = np.array(landmark_data)
    landmark_data = np.hstack((landmark_data, confident_col))
    best_score = 0.
    for pose, pose_category in zip(templates, templates_category):
        matrix, recog_score = alignment.pose_affinematrix(landmark_data, pose, dst_area=1.0, hard=True)
        if recog_score > 0:
            # valid `matrix`. default (dstH, dstW) is (1.0, 1.0)
            # matrix = get_resize_matrix(1.0, 1.0, dstW, dstH).dot(matrix)
            # scale = math.sqrt(matrix[0,0] ** 2 + matrix[0,1] ** 2)
            print(recog_score)
            
            if recog_score > best_score:
                category = pose_category
                best_score = recog_score
    
    return category if best_score > 0.5 else None



    