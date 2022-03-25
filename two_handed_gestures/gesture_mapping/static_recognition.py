import numpy as np
import alignment
import matplotlib.pyplot as plt

"""
image-based gesture recognition 
by calculating error between template keypoints and affine-transformed input keypoints 
(both pre-extracted from images using mediapipe),
and classifying into the gesture of smalledst error / highest score
"""

# for pose, pose_category in zip(self.templates, self.templates_category):
#             matrix, score = pose_affinematrix(kpt, pose, dst_area=1.0, hard=True)
#             if score > 0:
#                 # valid `matrix`. default (dstH, dstW) is (1.0, 1.0)
#                 matrix = get_resize_matrix(1.0, 1.0, dstW, dstH).dot(matrix)
#                 scale = math.sqrt(matrix[0,0] ** 2 + matrix[0,1] ** 2)
#                 category = pose_category
#             else:
#                 matrix = basic_matrix
#                 category = -1

# load input and template 
# all keypoints are normalized to [0.0, 1.0] by image width and height (4032, 3024 in our case)
# (x, y) landmark, input array shape: [21,2]
# add confidence column to the right of input array -> [21,3]
confident_col = np.ones((21,1))
five_temp = np.hstack((np.loadtxt('template_data/five_temp.csv', dtype = float, delimiter=','), confident_col))
arrow_temp = np.hstack((np.loadtxt('template_data/arrow_temp.csv', dtype=float,delimiter=','), confident_col))
five_input = np.hstack((np.loadtxt('input_data/five_input.csv', dtype = float, delimiter=','), confident_col))
arrow_input = np.hstack((np.loadtxt('input_data/arrow_input.csv', dtype=float,delimiter=','), confident_col))
print(five_temp.shape)

# matrix: [3,3]  score: percentage
five_matrix, five_score = alignment.pose_affinematrix(five_input, five_temp, dst_area=1.0, hard=True)
arrow_matrix1, arrow_score1 = alignment.pose_affinematrix(five_input, arrow_temp, dst_area=1.0, hard=True)
arrow_matrix2, arrow_score2 = alignment.pose_affinematrix(arrow_input, arrow_temp, dst_area=1.0, hard=True)
print(five_matrix.shape)

# plot template and affined-transformed keypoints
# affined_input = alignment.warpAffinePoints(arrow_input[:,0:2], five_matrix)
# print(affined_input.shape)
# print(score)
# plt.scatter(arrow_temp[:,0], five_temp[:,1], c='b', label='five_template')
# plt.scatter(affined_input[:,0],affined_input[:,1],c='r', label='five_input')
# plt.legend()
# plt.show()

# score: fiveT_fiveI, arrowT_fiveI, arrowT_arrowI
print(five_score, arrow_score1, arrow_score2)