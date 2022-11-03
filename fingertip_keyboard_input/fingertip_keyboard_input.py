# Main File
# Modified from https://google.github.io/mediapipe/solutions/hands.html

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For static images:
# IMAGE_FILES = []
# with mp_hands.Hands(
#         static_image_mode=True,
#         max_num_hands=2,
#         min_detection_confidence=0.5) as hands:
#     for idx, file in enumerate(IMAGE_FILES):
#         # Read an image, flip it around y-axis for correct handedness output (see
#         # above).
#         image = cv2.flip(cv2.imread(file), 1)
#         # Convert the BGR image to RGB before processing.
#         results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#         # Print handedness and draw hand landmarks on the image.
#         print('Handedness:', results.multi_handedness)
#         if not results.multi_hand_landmarks:
#             continue
#         image_height, image_width, _ = image.shape
#         annotated_image = image.copy()
#         for hand_landmarks in results.multi_hand_landmarks:
#             print('hand_landmarks:', hand_landmarks)
#             print(
#                     f'Index finger tip coordinates: (',
#                     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
#                     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
#             )
#             mp_drawing.draw_landmarks(
#                     annotated_image,
#                     hand_landmarks,
#                     mp_hands.HAND_CONNECTIONS,
#                     mp_drawing_styles.get_default_hand_landmarks_style(),
#                     mp_drawing_styles.get_default_hand_connections_style())
#         cv2.imwrite(
#                 '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
#         # Draw hand world landmarks.
#         if not results.multi_hand_world_landmarks:
#             continue
#         for hand_world_landmarks in results.multi_hand_world_landmarks:
#             mp_drawing.plot_landmarks(
#                 hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)

def draw_path(image, points):
    thickness = 5
    color = (0, 255, 0)
    for i in range(0, len(points) - 1):
        image = cv2.line(image, points[i], points[i+1], color, thickness)

    return image

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

    # array to hold drawn points
    fingertip_path_right = []

    while cap.isOpened():
        success, image = cap.read()
        image_height, image_width, channels = image.shape
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # print('Handedness:', results.multi_handedness)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):

                # if the right hand, store the points
                handedness = results.multi_handedness[i].classification[0].label

                #TODO: investigate why is this flipped, should be right hand
                if handedness == 'Left': 
                    print('Found Right Hand')
                    x_pixel = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x\
                                  * image_width)
                    y_pixel = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y\
                                  * image_height)
                    fingertip_path_right.append((x_pixel, y_pixel))
                    # print('Appending: {} and {}'.format(x_pixel, y_pixel))

                mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            # draw the path of the fingertip
            image = draw_path(image, fingertip_path_right)

        # if no hands, remove drawn points
        else:
            fingertip_path_right = []

        

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
