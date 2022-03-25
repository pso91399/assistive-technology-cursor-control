import numpy as np
import cv2
import mediapipe as mp
import os
import csv
import alignment as alignment


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For static images:
log = open('pose_log.txt', mode='w')
log.write('keep the landmark information from pose_alignment.py\n')
log.close()

five_input = os.path.join(os.getcwd(), 'templates', 'five_input.jpeg')
five_temp = os.path.join(os.getcwd(), 'templates','five_temp.jpeg')
arrow_temp = os.path.join(os.getcwd(), 'templates','arrow_temp.jpeg')
arrow_input = os.path.join(os.getcwd(), 'templates','arrow_input.jpeg')
IMAGE_FILES = [arrow_input]
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness and draw hand landmarks on the image.
    log = open('pose_log.txt', 'a')
    log.write(file + '\n')
    log.write(str(results.multi_handedness))
    print(type(results.multi_handedness))

    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    print(image_height)
    print(image_width)
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      log.write(str(hand_landmarks))
      log.writelines(
          ['Index finger tip coordinates: (',
          str(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width), 
          str(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height),')']
      )
      log.close()
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    cv2.imwrite(
        '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    # Draw hand world landmarks.
    # if not results.multi_hand_world_landmarks:
    #   continue
    # for hand_landmarks in results.multi_hand_landmarks:
    #   mp_drawing.plot_landmarks(
    #     hand_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
    
    # my_landmark = np.array(hand_landmarks.landmark)
    # print(my_landmark[0].items())
    
    # put hand landmarks into numpy arrays for calculation
    temp = []
    for point in hand_landmarks.landmark:
        temp.append([point.x,point.y])
    print(len(temp))
    
    with open('arrow_input.csv','w') as f:
        write = csv.writer(f)
        write.writerows(temp)


# video recognition

# temp = np.loadtxt('temp.csv', dtype = float, delimiter=',')
# confident_col = np.ones((temp.shape[0],1))
# temp = np.hstack((temp, confident_col))
# hands = mp_hands.Hands(
#     min_detection_confidence=0.7)
# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     success, image = cap.read()
#     image = cv2.flip(image, 1)
#     if not success:
#       print("Ignoring empty camera frame.")
#       # If loading a video, use 'break' instead of 'continue'.
#       continue

#     # To improve performance, optionally mark the image as not writeable to
#     # pass by reference.
#     image.flags.writeable = False
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = hands.process(image)

#     # Draw the hand annotations on the image.
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)



#     if results.multi_hand_landmarks:
#         right_hand = None
#         left_hand = None
#         for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
#             handedness = results.multi_handedness[i].classification[0].label
#             print(handedness)
#             mp_drawing.draw_landmarks(
#                 image,
#                 hand_landmarks,
#                 mp_hands.HAND_CONNECTIONS,
#                 mp_drawing_styles.get_default_hand_landmarks_style(),
#                 mp_drawing_styles.get_default_hand_connections_style())

#             landmark_data = []
#             for point in hand_landmarks.landmark:
#                 landmark_data.append([point.x, point.y])
#             landmark_data = np.array(landmark_data)
#             landmark_data = np.hstack((landmark_data, confident_col))
#             if handedness == 'Left':
#                 _, score = alignment.pose_affinematrix(landmark_data, temp, dst_area=1.0, hard=True)
#                 print(score)
  

