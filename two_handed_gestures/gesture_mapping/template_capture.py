import numpy as np
import cv2
import mediapipe as mp
import csv

def template_capture():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(
        min_detection_confidence=0.7)
    cap = cv2.VideoCapture(0)
    frame_cnt = 0
    fig_cnt = 0

    while cap.isOpened():
        
        success, image = cap.read()
        image = cv2.flip(image, 1)
        if not success:
            print("Ignoring empty camera frame.")
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
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness = results.multi_handedness[i].classification[0].label
                frame_cnt += 1
                print(frame_cnt)
                # print(handedness)
                if frame_cnt == 30:
                    print("save template")
                    landmark_data = []
                    for point in hand_landmarks.landmark:
                        landmark_data.append([point.x, point.y])
                    landmark_data = np.array(landmark_data)
                    with open('tmp_data/' + str(fig_cnt) + '.csv','w') as f:
                        write = csv.writer(f)
                        write.writerows(landmark_data)
                    cv2.imwrite('landmark_figs/' + str(fig_cnt) + '.png', image)
                    fig_cnt += 1
                    frame_cnt = 0
                
                else:          
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()


  

# if __name__ == '__main__':
#     template_capture()
    
template_capture()