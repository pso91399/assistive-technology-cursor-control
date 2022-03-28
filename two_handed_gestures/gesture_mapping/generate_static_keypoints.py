"""this file is used to generate template / static input images landmarks and save them in the right path"""
from dataclasses import Field
import mediapipe as mp
import numpy as np
import os
import cv2
import csv
import re
from typing import List




# INPUT_IMAGE_FILES = os.listdir(os.path.join(os.getcwd(), 'input_image'))
# TEMPLATE_IMAGE_FILES = os.listdir(os.path.join(os.getcwd(), 'template_image'))
# print(TEMPLATE_IMAGE_FILES)

def list_file_paths(directory: str) -> List:
    """ Generate a list of relative file path for landmark data

    Args:
        directory: folder name of the landmark data files
    Returns:
        a list of paths
    """
    return [os.path.join(directory,file) for file in os.listdir(directory)]


def generate_landmarks(FILES):
  # mediapipe drawing package and hand solutions
  mp_hands = mp.solutions.hands

  # initialize
  with mp_hands.Hands(
      static_image_mode=True,
      max_num_hands=2,
      min_detection_confidence=0.5) as hands:
      # choose input or template images directory to generate keypoints
    for idx, file in enumerate(FILES):
      # Read an image, flip it around y-axis for correct handedness output 
      image = cv2.flip(cv2.imread(file), 1)
      # Convert the BGR image to RGB before processing.
      results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

      # Print handedness
      print(results.multi_handedness)
      print(type(results.multi_handedness))

      if not results.multi_hand_landmarks:
        print(results)
        continue

      for hand_landmarks in results.multi_hand_landmarks:    
      
        # save (x,y) keypoints to csv, and put it into corresponding folder
        temp = []
        for point in hand_landmarks.landmark:
            temp.append([point.x,point.y])

        
        name = re.findall(r'\/(\w+).', file)[0]
        path = re.findall(r'\_(\w+)', name)[0]

        with open(path + '_data/' + name + '.csv','w') as f:
            write = csv.writer(f)
            write.writerows(temp)


