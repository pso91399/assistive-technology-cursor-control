'''from https://github.com/metalwhale/hand_tracking'''
import cv2
import time
from examples.mediapipe_tracking.src.hand_tracker_3d import HandTracker3D
import numpy as np
import os
import re
import json
import csv
import datetime

PALM_MODEL_PATH = "examples/mediapipe_tracking/models/palm_detection_without_custom_op.tflite"
LANDMARK_MODEL_PATH = "examples/mediapipe_tracking/models/hand_landmark_3d.tflite"
ANCHORS_PATH = "examples/mediapipe_tracking/models/anchors.csv"
OUTPUT_PATH = "gesture_learning/Fall 2020/ipn/keypoints_data"
VIDEO_PATH = "/Users/Radiance/capstone/ipn/videos"
LABEL_TRAINING_PATH = "/Users/Radiance/capstone/ipn/annotations/Annot_TrainList.txt"
LABEL_TESTING_PATH = "/Users/Radiance/capstone/ipn/annotations/Annot_TestList.txt"

INPUT_FPS = 30
OUTPUT_FPS = 30
FRAME_STEP = INPUT_FPS // OUTPUT_FPS

detector = HandTracker3D(
    PALM_MODEL_PATH,
    LANDMARK_MODEL_PATH,
    ANCHORS_PATH,
    box_shift=0.2,
    box_enlarge=1.3
)

def generate_datasets(video_path, label_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, 'description.txt'), 'w+') as f:
        f.writelines([f"time modified: {datetime.datetime.now()}\n"])
    labelList = list(csv.reader(label_path))
    for video,label,id,t_start,t_end,frames in labelList:
        os.makedirs(os.path.join(output_path, subjectName, sceneName), exist_ok=True)
        for groupEntry in os.scandir(os.path.join(LABEL_PATH, subjectName, sceneName)):
            dataset = []
            # print(groupEntry.name,re.fullmatch(r'Group\d+.csv', groupEntry.name))
            if not re.fullmatch(r'Group\d+.csv', groupEntry.name): continue
            groupNum = int(re.findall(r'Group(\d+).csv', groupEntry.name)[0])
            with open(groupEntry) as label_path:
                curFrameIdx = 0
                rgbPath = os.path.join(VIDEO_PATH, subjectName, sceneName, 'Color', f'rgb{groupNum}.avi')
                rgbCap = cv2.VideoCapture(rgbPath)
                labelList = list(csv.reader(label_path))
                print(f"Processing subject {subjectName}, scene {sceneName}, group {groupNum}")
                for i, (label, startFrame, endFrame) in enumerate(labelList):
                    try:
                        label = int(label)
                        if label not in labels_to_use: continue
                        videoKeypoints = []
                        for nextFrameIdx in range(int(startFrame), int(endFrame), FRAME_STEP):
                            while curFrameIdx < nextFrameIdx:
                                hasRGBFrame, rgbFrame = rgbCap.read()
                                curFrameIdx += 1
                            image = cv2.cvtColor(rgbFrame, cv2.COLOR_BGR2RGB)
                            points = detector.detect_rotated_joints(image)
                            # visualize_keypoints(rgbFrame, points, connections)
                            if points is None:
                                videoKeypoints.append([])
                            else:
                                videoKeypoints.append(points.tolist())
                        if len(videoKeypoints):
                            dataset.append({'label': label, 'keypoints': videoKeypoints})
                    except Exception as e:
                        print(e)
                rgbCap.release()
            if not dataset:
                continue
            with open(os.path.join(output_path, subjectName, sceneName, f'group{groupNum}.json'), 'w+') as dataFile:
                json.dump(dataset, dataFile)
                print(f"Data written to {os.path.abspath(dataFile.name)}")
generate_datasets([1,2])