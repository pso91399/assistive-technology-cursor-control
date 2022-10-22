import cv2
import os
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
drawing_spec_connection = mp_drawing.DrawingSpec(thickness=20, circle_radius=2)
drawing_spec_landmarks = mp_drawing.DrawingSpec((0, 0, 255), thickness=20, circle_radius=10)
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For static images:
IMAGE_FILES = os.listdir('template_image_new')
if '.DS_Store' in IMAGE_FILES:
  IMAGE_FILES.remove('.DS_Store')
print(IMAGE_FILES)
print(IMAGE_FILES)
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.7) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    file_abolute_path = os.path.join(os.getcwd(), 'template_image_new', file)
    print(file_abolute_path)
    image = cv2.flip(cv2.imread(file_abolute_path), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness and draw hand landmarks on the image.
    print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      print('hand_landmarks:', hand_landmarks)
      print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      )
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          # mp_drawing_styles.get_default_hand_landmarks_style(),
          drawing_spec_landmarks,
          # mp_drawing_styles.get_default_hand_connections_style())
          drawing_spec_connection)
      
    store_absolute_path = os.path.join(os.getcwd(), 'template_image_annotated_new')
    cv2.imwrite(
        store_absolute_path + '/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    # Draw hand world landmarks.
    # if not results.multi_hand_world_landmarks:
    #   continue
    # for hand_world_landmarks in results.multi_hand_world_landmarks:
    #   mp_drawing.plot_landmarks(
    #     hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
