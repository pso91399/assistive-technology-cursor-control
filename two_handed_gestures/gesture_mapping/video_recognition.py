from matplotlib.animation import ImageMagickBase
import numpy as np
import cv2
import mediapipe as mp
import os
import csv
import re
import alignment as alignment
import matplotlib.pyplot as plt


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# video recognition

# load five_template keypoints
def list_file_paths(directory):
    return [os.path.join(directory,file) for file in os.listdir(directory)]

confident_col = np.ones((21,1))
five_temp = np.hstack((np.loadtxt('input_data/five_input.csv', dtype = float, delimiter=','), confident_col))
arrow_temp = np.hstack((np.loadtxt('input_data/arrow_input.csv', dtype = float, delimiter=','), confident_col))
templates = [five_temp, arrow_temp]

templates = []
templates_category = []
for idx, file in enumerate(list_file_paths('temp_data')):
    name = name = re.findall(r'\/(\w+).', file)[0]
    temp = np.hstack((np.loadtxt(file, dtype = float, delimiter=','), confident_col))
    templates.append(temp)
    templates_category.append(name)




# initialize mp hand module
hands = mp_hands.Hands(
    min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

draw_cnt = 0
while cap.isOpened():
    success, image = cap.read()
    image = cv2.flip(image, 1)
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
            print(handedness)
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            landmark_data = []
            for point in hand_landmarks.landmark:
                landmark_data.append([point.x, point.y])
            landmark_data = np.array(landmark_data)
            landmark_data = np.hstack((landmark_data, confident_col))




            # if handedness == 'Left':
            #     _, score = alignment.pose_affinematrix(landmark_data, temp, dst_area=1.0, hard=True)
            #     print(score)
            # if handedness == 'Right':
            #     _, score = alignment.pose_affinematrix(landmark_data, temp, dst_area=1.0, hard=True)
            #     print(score)
            best_score = 0.
            draw_cnt += 1
            for pose, pose_category in zip(templates, templates_category):
                matrix, score = alignment.pose_affinematrix(landmark_data, pose, dst_area=1.0, hard=True)
                if score > 0:
                    # valid `matrix`. default (dstH, dstW) is (1.0, 1.0)
                    # matrix = get_resize_matrix(1.0, 1.0, dstW, dstH).dot(matrix)
                    # scale = math.sqrt(matrix[0,0] ** 2 + matrix[0,1] ** 2)
                    print(score)
                    
                    if score > best_score:
                        category = pose_category
                        best_score = score
                    
                    # if draw_cnt == 30:
                        # draw template(arrow and temp) and raw landmark: 
                        # affined_input = alignment.warpAffinePoints(arrow_input[:,0:2], five_matrix)

                        # image show
                        # cv2.imwrite('landmark_figs/' + str(score)[:5] + '.png', image)

                        # # five_temp and raw landmark
                        # handles, labels = plt.gca().get_legend_handles_labels()
                        # by_label = dict(zip(labels, handles))
                        # plt.scatter(pose[:,0], pose[:,1], c='b', label=pose_category+'_template')
                        # plt.scatter(landmark_data[:,0],landmark_data[:,1],c='r', label='raw landmark')
                        # plt.title("template and {} raw landmark with score at {:.2f} recognized as {}".format(handedness, score, pose_category))
                        # plt.legend(by_label.values(), by_label.keys())
                        # plt.savefig('landmark_figs/' + pose_category + 'raw '+ handedness + str(score)[:5] + '.png')
                        # plt.clf()
                        

                        # # five_temp and affined landmark
                        # affined_input = alignment.warpAffinePoints(landmark_data[:,0:2], matrix)
                        # handles, labels = plt.gca().get_legend_handles_labels()
                        # by_label = dict(zip(labels, handles))
                        # plt.scatter(pose[:,0], pose[:,1], c='b', label=pose_category+'_template')
                        # plt.scatter(affined_input[:,0],affined_input[:,1],c='r', label='affined landmark')
                        # plt.title("template and {} raw landmark with score at {:.2f} recognized as {}".format(handedness, score, pose_category))
                        # plt.legend(by_label.values(), by_label.keys())
                        # plt.savefig('landmark_figs/' + pose_category +'affined '+ handedness + str(score)[:5] + '.png')
                        # plt.clf()

                    # else:
                    #     # matrix = basic_matrix
                    #     category = -1
                    # if draw_cnt == 30:
                    #     draw_cnt = 0
            


            cv2.putText(image, 'pose: ' + category, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()