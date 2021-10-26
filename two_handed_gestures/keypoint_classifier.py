import cv2
import numpy as np
import tensorflow as tf
import tensorflow.keras.layers as layers
import os
import sys
import time

sys.path.append(os.getcwd())

GESTURE_TYPES = 11

GESTURE_LABELS = [
    'Fist', 'Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
    'Eight', 'Nine'
]

CONNECTION_LABELS = [(0, 1), (1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (7, 8),
                     (9, 10), (10, 11), (11, 12), (13, 14), (14, 15), (15, 16),
                     (17, 18), (18, 19), (19, 20), (0, 5), (5, 9), (9, 13),
                     (13, 17), (0, 17)]

WINDOW = 'Keypoint Classifier'
POINT_COLOR = (0, 255, 0)
CONNECTION_COLOR = (255, 0, 0)
THICKNESS = 2
MAX_WIDTH = 480

from hand_tracker_3d import HandTracker3D


def generate_connection_angles(keypoints,
                               keypoints_num=21,
                               keypoints_dimensions=3):
    connections = []
    for connection in CONNECTION_LABELS:
        connections.append(keypoints[..., connection[1], :] -
                           keypoints[..., connection[0], :])
    connections = np.stack(connections, axis=-2)
    tensor1 = connections[..., np.newaxis].repeat(keypoints_num,
                                                  -1).transpose(0, 1, 2, 4, 3)
    tensor2 = connections[..., np.newaxis].repeat(keypoints_num,
                                                  -1).transpose(0, 1, 4, 2, 3)
    angles = (tensor1 * tensor2).sum(axis=-1) / np.linalg.norm(
        tensor1, axis=-1) / np.linalg.norm(tensor2, axis=-1)
    angles = angles.transpose(2, 3, 0,
                              1)[np.triu_indices(21, k=1)].transpose(1, 2, 0)
    return np.arccos(angles)


def generate_joint_distances(keypoints,
                             keypoints_num=21,
                             keypoints_dimensions=3):
    connections = []
    for connection in CONNECTION_LABELS:
        connections.append(keypoints[..., connection[1], :] -
                           keypoints[..., connection[0], :])
    connections = np.stack(connections, axis=-2)
    tensor1 = connections[..., np.newaxis].repeat(keypoints_num,
                                                  -1).transpose(0, 1, 2, 4, 3)
    tensor2 = connections[..., np.newaxis].repeat(keypoints_num,
                                                  -1).transpose(0, 1, 4, 2, 3)
    distances = np.linalg.norm(tensor1 - tensor2, axis=-1).transpose(
        2, 3, 0, 1)[np.triu_indices(21, k=1)].transpose(1, 2, 0)
    return distances


class KeypointClassifier(HandTracker3D):
    def __init__(self,
                 palm_model,
                 joint_model,
                 anchors_path,
                 gesture_weights,
                 box_enlarge=1.5,
                 box_shift=0.2):
        super().__init__(palm_model, joint_model, anchors_path, box_enlarge,
                         box_shift)
        self.gesture_classifier = tf.keras.Sequential([
            layers.Masking(),
            layers.GRU(GESTURE_TYPES, activation=None, stateful=True),
            layers.Activation('softmax')
        ])
        self.gesture_classifier.load_weights(
            os.path.join(gesture_weights, 'model'))
        self.features_mean = np.load(os.path.join(gesture_weights, 'mean.npy'))
        self.features_std = np.load(os.path.join(gesture_weights, 'std.npy'))

    def __call__(self, img):
        points, kp_orig = super().__call__(img)
        if points is None:
            points = np.ones((21, 3)) * np.nan
        joints = points[np.newaxis, np.newaxis, ...]
        angles = generate_connection_angles(joints)
        distances = generate_joint_distances(joints)
        feature = self.process_features(joints, angles, distances)
        probs = self.gesture_classifier(feature)
        return probs, points, kp_orig

    def reset_states(self):
        self.gesture_classifier.reset_states()

    def process_features(self, keypoints, angles, distances):
        features = np.concatenate(
            (keypoints.reshape(1, 1, -1), angles, distances), -1)
        features = (features - self.features_mean) / self.features_std
        features = np.nan_to_num(features)
        return features


if __name__ == '__main__':
    PALM_MODEL_PATH = os.path.join(
        sys.path[0],
        "models/palm_detection_without_custom_op.tflite"
    )
    LANDMARK_MODEL_PATH = os.path.join(
        sys.path[0],
        "models/hand_landmark_3d.tflite")
    ANCHORS_PATH = os.path.join(
        sys.path[0], "models/anchors.csv")
    gesture_weights = os.path.join(sys.path[0], 'models/gru_stateful')
    classifier = KeypointClassifier(PALM_MODEL_PATH,
                                    LANDMARK_MODEL_PATH,
                                    ANCHORS_PATH,
                                    gesture_weights,
                                    box_shift=0.2,
                                    box_enlarge=1.3)

    cv2.namedWindow(WINDOW)
    # Initialize video stream
    capture = cv2.VideoCapture(0)
    if capture.isOpened():
        hasFrame, frame = capture.read()
    else:
        hasFrame = False

    font = cv2.FONT_HERSHEY_SIMPLEX
    start = time.time()
    frames = 0
    while True:
        cv2.imshow(WINDOW, frame)
        hasFrame, frame = capture.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        probs, points, kp_orig = classifier(image)
        frames += 1
        label = tf.argmax(probs, axis=1).numpy()[0]
        if kp_orig is not None:
            for point in kp_orig:
                x, y, z = point
                cv2.circle(frame, (int(x), int(y)), THICKNESS * 2, POINT_COLOR,
                           THICKNESS)
            for connection in CONNECTION_LABELS:
                x0, y0, z0 = kp_orig[connection[0]]
                x1, y1, z1 = kp_orig[connection[1]]
                cv2.line(frame, (int(x0), int(y0)), (int(x1), int(y1)),
                         CONNECTION_COLOR, 1)
        # print('{0:.2f}: {1:d} {2:s}'.format((time.time() - start) / frames,label, GESTURE_LABELS[label]))
        cv2.putText(frame,
            "FPS: {}, label: {}".format(round(frames / (time.time() - start)),
                                        GESTURE_LABELS[label]), (50, 50), font,
            1, (0, 0, 255), 2, cv2.LINE_4)
        key = cv2.waitKey(1)
        if key == 27:
            break
    capture.release()
    cv2.destroyAllWindows()
