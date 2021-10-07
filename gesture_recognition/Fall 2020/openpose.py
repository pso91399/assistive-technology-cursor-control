import cv2
import numpy as np

# Specify the paths for the 2 files
protoFile = "openpose_models/hand/pose_deploy.prototxt"
weightsFile = "openpose_models/hand/pose_iter_102000.caffemodel"

# Read the network into Memory
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

cam = cv2.VideoCapture(0)

while True:
     # Read the input image
     ret, frame = cam.read()
     if not ret:
          break

     frameHeight, frameWidth = frame.shape[:2]

     # Specify the input image dimensions
     width = 368
     height = 368

     # Prepare the frame to be fed to the network
     inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (width, height), (0, 0, 0), swapRB=False, crop=False)

     # Set the prepared object as the input blob of the network
     net.setInput(inpBlob)

     output = net.forward()
     h_out, w_out = output.shape[2:4]
     # Empty list to store the detected keypoints
     points = []
     for i in range(22):
          # confidence map of corresponding body's part
          probMap = output[0, i, :, :]

          # Find global maxima of the probMap
          minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

          # Scale the point to fit on the original image
          x = (frameWidth * point[0]) / w_out
          y = (frameHeight * point[1]) / h_out

          if prob > 0:
               cv2.circle(frame, (int(x), int(y)), 15, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
               cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3, lineType=cv2.LINE_AA)
               points.append((int(x), int(y)))
          else:
               points.append(None)

     cv2.imshow("Output-Keypoints", frame)
     
     k = cv2.waitKey(1)
     if k == 27 or k == 113: #27, 113 are ascii for escape and q respectively
          #exit
          break

cam.release()
# cv2.destroyAllWindows()