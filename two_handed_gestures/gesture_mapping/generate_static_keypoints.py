import mediapipe as mp
import numpy as np
import os
import cv2
import csv
import re


# mediapipe drawing package
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
# mediapipe hand package
mp_hands = mp.solutions.hands

# keep a log file if needed
# log = open('pose_log.txt', mode='w')
# log.write('keep the landmark information from pose_alignment.py\n')
# log.close()

# INPUT_IMAGE_FILES = os.listdir(os.path.join(os.getcwd(), 'input_image'))
# TEMPLATE_IMAGE_FILES = os.listdir(os.path.join(os.getcwd(), 'template_image'))
# print(TEMPLATE_IMAGE_FILES)

def list_file_paths(directory):
    return [os.path.join(directory,file) for file in os.listdir(directory)]

# initialize
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
    # choose input or template images directory to generate keypoints
  for idx, file in enumerate(list_file_paths('input_image')):
    # Read an image, flip it around y-axis for correct handedness output 
    image = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness (and keep logging)
    print(results.multi_handedness)
    # log = open('pose_log.txt', 'a')
    # log.write(file + '\n')
    # log.write(str(results.multi_handedness))
    print(type(results.multi_handedness))

    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:

    # # keep logging
    #   log.write(str(hand_landmarks))
    #   log.writelines(
    #       ['Index finger tip coordinates: (',
    #       str(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width), 
    #       str(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height),')']
    #   )
    #   log.close()

    # draw hand landmarks on the image
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    # cv2.imwrite(
    #     '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    # Draw hand world landmarks.
    for hand_landmarks in results.multi_hand_landmarks:
      mp_drawing.plot_landmarks(
        hand_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
    
    my_landmark = np.array(hand_landmarks.landmark)
    
    # save (x,y) keypoints to csv, and put it into corresponding folder
    temp = []
    for point in hand_landmarks.landmark:
        temp.append([point.x,point.y])
    
    name = re.findall(r'\/(\w+).', file)[0]
    path = re.findall(r'\_(\w+)', name)[0]
    with open(path + '_data/' + name + '.csv','w') as f:
        write = csv.writer(f)
        write.writerows(temp)