"""this file contains functions for drawing hand landmarks, both by matplatlib and mediapipe drawing tools"""
from cProfile import label
import matplotlib.pyplot as plt
import os
import re
import mediapipe as mp
import numpy as np
import cv2
from typing import List


def list_file_paths(directory: str) -> List:
    """ Generate a list of relative file path for landmark data

    Args:
        directory: folder name of the landmark data files
    Returns:
        a list of paths
    """
    return [os.path.join(directory,file) for file in os.listdir(directory)]


# by matlabplot
# for idx, file in enumerate(list_file_paths('temp_data')):
#     name = re.findall(r'\/(\w+).', file)[0]
#     data = np.loadtxt(file, dtype = float, delimiter=',')
#     plt.scatter(data[:,0], data[:,1])
#     plt.title('{} tamplate'.format(name))
#     plt.show()
#     plt.clf()


# handles, labels = plt.gca().get_legend_handles_labels()
# by_label = dict(zip(labels, handles))
# plt.scatter(pose[:,0], pose[:,1], c='b', label=pose_category+'_template')
# plt.scatter(landmark_data[:,0],landmark_data[:,1],c='r', label='raw landmark')
# plt.title("template and {} raw landmark with score at {:.2f} recognized as {}".format(handedness, score, pose_category))
# plt.legend(by_label.values(), by_label.keys())
# plt.savefig('landmark_figs/' + pose_category + 'raw '+ handedness + str(score)[:5] + '.png')
# plt.clf()

def draw_by_plt(FILES, path):
    """Generate scatter plots with matplotlib.pyplot.

    Axies for landmarks will be the same as opencv. 
    Name of the saved figure will be the same as input files's name.
    
    Args:
        FILES: a list of paths of files to be plotted on the same figure  TODO: determine if to strict it to absolute paths.
        path: path for the figure to save.
    Returns:
        saved figure: a scatter plot with scatter points.
    """
    for _, file in enumerate(FILES):
        name = re.findall(r'\/(\w+).', file)[0]
        data = np.loadtxt(file, dtype = float, delimiter=',', label=name)
        plt.scatter(data[:,0], data[:,1])
    plt.legend()
    plt.gca().invert_yaxis()
    plt.title("hand landmarks")
    plt.savefig("{}/" + name + ".png".format(path))
    plt.clf()
        


# by mediapipe drawing tools
def draw_by_mp(FILES):
    # For static images:
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:
        for idx, file in enumerate(FILES):
            # Read an image, flip it around y-axis for correct handedness output (see
            # above).
            name = re.findall(r'\/(\w+).', file)[0]
            image = cv2.flip(cv2.imread(file), 1)
            # Convert the BGR image to RGB before processing.
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Print handedness and draw hand landmarks on the image.
            # print('Handedness:', results.multi_handedness)
            if not results.multi_hand_landmarks:
                continue
            annotated_image = image.copy()
            for hand_landmarks in results.multi_hand_landmarks:
                print('hand_landmarks:', hand_landmarks)
                mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                cv2.putText(results.multi_handedness,(10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
                cv2.imwrite(
                    'mp_annotated_image/' + name + '.png', cv2.flip(annotated_image, 1))
