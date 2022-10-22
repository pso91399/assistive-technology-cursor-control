import cv2
import os
import mediapipe as mp
import matplotlib.pyplot as plt

IMAGE_FILES = [
    # five input
    '/Users/xinying/Project/assistive-mouse-control/assistive-technology-cursor-control/two_handed_gestures/gesture_mapping/input_image/five_input.jpeg',
    # five temp
    '/Users/xinying/Project/assistive-mouse-control/assistive-technology-cursor-control/two_handed_gestures/gesture_mapping/input_image/five_temp.jpeg',
    # arrow temp
    '/Users/xinying/Project/assistive-mouse-control/assistive-technology-cursor-control/two_handed_gestures/gesture_mapping/input_image/arrow_temp.jpeg'
]


# generate keypoint vectors
mp_hands = mp.solutions.hands
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.7) as hands:
  for idx, file in enumerate(IMAGE_FILES):
      image = cv2.flip(cv2.imread(file), 1)
      print(type(image))
      results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
      for hand_landmarks in results.multi_hand_landmarks:
          if idx == 0: # five input
            five_input = []
            for point in hand_landmarks.landmark:
                five_input.append([point.x,point.y])
          if idx == 1: # five temp
            five_temp = []
            for point in hand_landmarks.landmark:
                five_temp.append([point.x,point.y])
          if idx == 2: # arrow temp
            arrow_temp = []
            for point in hand_landmarks.landmark:
                arrow_temp.append([point.x,point.y])


# plot: before alignment
# input and five temp
plt.scatter(five_input[:,0], five_input[:,1])
plt.scatter(five_temp[:,0], five_temp[:,1])
plt.legend()
plt.clf()

plt.scatter(five_input[:,0], five_input[:,1])
plt.scatter(arrow_temp[:,0], arrow_temp[:,1])
plt.legend()
plt.clf()