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


def generate_landmarks():

  IMAGE_FILES = {
    "./images/template_image_new_wide/arrow.jpeg": "arrow_3d",
    "./images/template_image_new_wide/fist.jpeg": "fist_3d",
    "./images/template_image_new_wide/five.jpeg": "five_3d",
    "./images/template_image_new_wide/four.jpeg": "four_3d",
    "./images/template_image_new_wide/one.jpeg": "one_3d",
    "./images/template_image_new_wide/three.jpeg": "three_3d",
    "./images/template_image_new_wide/thumb.jpeg": "thumb_3d",
    "./images/template_image_new_wide/two.jpeg": "two_3d"
  }
  # mediapipe drawing package and hand solutions
  mp_hands = mp.solutions.hands

  # initialize
  with mp_hands.Hands(
      static_image_mode=True,
      max_num_hands=2,
      min_detection_confidence=0.5) as hands:
      # choose input or template images directory to generate keypoints
    for file in IMAGE_FILES:
      # Read an image, flip it around y-axis for correct handedness output 
      image = cv2.imread(file)
      # image = cv2.flip(cv2.imread(file), 1)
      # Convert the BGR image to RGB before processing.
      results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

      # Print handedness
      print(results.multi_handedness)
      # print(type(results.multi_handedness))

      if not results.multi_hand_landmarks:
        print(results)
        continue

      for hand_landmarks in results.multi_hand_landmarks:    
      
        # save (x,y) keypoints to csv, and put it into corresponding folder
        temp = []
        for point in hand_landmarks.landmark:
          # 2D result
            temp.append([point.x,point.y, point.z])

        path = "./data/template_image_new_wide_data_3d/"

        with open(path + IMAGE_FILES[file] + '.csv','w') as f:
            write = csv.writer(f)
            write.writerows(temp)


if __name__ == "__main__":
  generate_landmarks()

