import numpy as np
import cv2
import math
import matplotlib.pyplot as plt


# https://github.com/liruilong940607/Pose2Seg/blob/master/lib/transforms.py

def get_affine_matrix(center, angle, translate, scale, shear=0):
    # Helper method to compute affine transformation

    # As it is explained in PIL.Image.rotate
    # We need compute affine transformation matrix: M = T * C * RSS * C^-1
    # where T is translation matrix: [1, 0, tx | 0, 1, ty | 0, 0, 1]
    #       C is translation matrix to keep center: [1, 0, cx | 0, 1, cy | 0, 0, 1]
    #       RSS is rotation with scale and shear matrix
    #       RSS(a, scale, shear) = [ cos(a)*sx    -sin(a + shear)*sy     0]
    #                              [ sin(a)*sx    cos(a + shear)*sy     0]
    #                              [     0                  0          1]

    angle = math.radians(angle)
    shear = math.radians(shear)

    T = np.array([[1, 0, translate[0]], [0, 1, translate[1]], [0, 0, 1]]).astype(np.float32)
    C = np.array([[1, 0, center[0]], [0, 1, center[1]], [0, 0, 1]]).astype(np.float32)
    RSS = np.array([[ math.cos(angle)*scale[0], -math.sin(angle + shear)*scale[1], 0],
                    [ math.sin(angle)*scale[0],  math.cos(angle + shear)*scale[1], 0],
                    [ 0, 0, 1]]).astype(np.float32)
    C_inv = np.linalg.inv(np.mat(C))
    M = T.dot(C).dot(RSS).dot(C_inv)
    return M

def warpAffinePoints(pts, H):
    # pts: (N, (x,y))
    pts = np.array(pts, dtype=np.float32)
    assert H.shape in [(3,3), (2,3)], 'H.shape must be (2,3) or (3,3): {}'.format(H.shape)
    ext = np.ones((len(pts), 1), dtype=pts.dtype)
    return np.array(np.hstack((pts, ext)).dot(H[0:2, :].transpose(1, 0)), dtype=np.float32)

def get_resize_padding_matrix(srcW, srcH, dstW, dstH, iscenter=False):
    # this function keep ratio
    scalex = scaley = min(float(dstW)/srcW, float(dstH)/srcH)
    if iscenter:
        translate = ((dstW - srcW * scalex)/2.0, (dstH - srcH * scaley)/2.0)
    else:
        translate = (0, 0)
    return get_affine_matrix(center=(0, 0), angle=0, translate=translate, scale=(scalex, scaley))

def get_resize_matrix(srcW, srcH, dstW, dstH):
    # this function do not keep ratio
    scalex, scaley = (float(dstW)/srcW, float(dstH)/srcH)
    return get_affine_matrix(center=(0, 0), angle=0, translate=(0, 0), scale=(scalex, scaley))



# https://github.com/liruilong940607/Pose2Seg/blob/64fcc5e0ee7b85c32f4be2771ce810a41b9fcb38/modeling/core.py#L159
def pose_affinematrix(src_kpt, dst_kpt, dst_area, hard=False):
    ''' `dst_kpt` is the template. 
    Args:
        src_kpt, dst_kpt: (17, 3)
        dst_area: used to uniform returned score.
        hard: 
            - True: for `dst_kpt` is the template. we do not want src_kpt
                to match a template and out of range. So in this case, 
                src_kpt[vis] should convered by dst_kpt[vis]. if not, will 
                return score = 0
            - False: for matching two kpts.
    Returns:
        matrix: (2, 3)
        score: align confidence/similarity, a float between 0 and 1.
    '''
    # set confidence constriants
    src_vis = src_kpt[:, 2] > 0
    dst_vis = dst_kpt[:, 2] > 0
    visI = np.logical_and(src_vis, dst_vis)
    visU = np.logical_or(src_vis, dst_vis)
    # - 0 Intersection Points means we know nothing to calc matrix.
    # - 1 Intersection Points means there are infinite matrix.
    # - 2 Intersection Points means there are 2 possible matrix.
    #   But in most case, it will lead to a really bad solution
    if sum(visI) == 0 or sum(visI) == 1 or sum(visI) == 2:
        matrix = np.array([[1, 0, 0], 
                           [0, 1, 0]], dtype=np.float32)
        score = 0.
        return matrix, score
    
    if hard and (False in dst_vis[src_vis]):
        matrix = np.array([[1, 0, 0], 
                           [0, 1, 0]], dtype=np.float32)
        score = 0.
        return matrix, score
      
    src_valid = src_kpt[visI, 0:2]
    dst_valid = dst_kpt[visI, 0:2]
    matrix = solve_affinematrix(src_valid, dst_valid)
    matrix = np.vstack((matrix, np.array([0,0,1], dtype=np.float32)))
    
    # calc score
    #sigmas = np.array([.26, .25, .25, .35, .35, .79, .79, .72, .72, .62,.62, 1.07, 1.07, .87, .87, .89, .89])/10.0
    #vars_valid = ((sigmas * 2)**2)[visI]
    vars_valid = 1
    diff = warpAffinePoints(src_valid, matrix) - dst_valid
    # print(diff)
    # error = np.sum(diff**2, axis=1) / vars_valid / dst_area / 2
    # score = np.mean(np.exp(-error)) * np.sum(visI) / np.sum(visU)
    error = np.sum(diff**2, axis=1) * 50
    score = np.mean(np.exp(-error))
    
    return matrix, score

def solve_affinematrix(src, dst):
    '''
    Document: https://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html?highlight=solve#cv2.solve
    C++ Version: aff_trans.cpp in opencv
    src: numpy array (N, 2)
    dst: numpy array (N, 2)
    fullAffine = False means affine align without shear.
    '''
    src = src.reshape(-1, 1, 2)
    dst = dst.reshape(-1, 1, 2)
    
    out = np.zeros((2,3), np.float32)
    siz = 2*src.shape[0]

    matM = np.zeros((siz,4), np.float32)
    matP = np.zeros((siz,1), np.float32)
    contPt=0
    for ii in range(0, siz):
        therow = np.zeros((1,4), np.float32)
        if ii%2==0:
            therow[0,0] = src[contPt, 0, 0] # x
            therow[0,1] = src[contPt, 0, 1] # y
            therow[0,2] = 1
            matM[ii,:] = therow[0,:].copy()
            matP[ii,0] = dst[contPt, 0, 0] # x
        else:
            therow[0,0] = src[contPt, 0, 1] # y ## Notice, c++ version is - here
            therow[0,1] = -src[contPt, 0, 0] # x
            therow[0,3] = 1
            matM[ii,:] = therow[0,:].copy()
            matP[ii,0] = dst[contPt, 0, 1] # y
            contPt += 1
    sol = cv2.solve(matM, matP, flags = cv2.DECOMP_SVD)
    sol = sol[1]
    out[0,0]=sol[0,0]
    out[0,1]=sol[1,0]
    out[0,2]=sol[2,0]
    out[1,0]=-sol[1,0]
    out[1,1]=sol[0,0]
    out[1,2]=sol[3,0]

    # result
    return out


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

# try to static image recognition
five_temp = np.loadtxt('temp.csv', dtype = float, delimiter=',')
arrow_temp = np.loadtxt('arrow_temp.csv', dtype=float,delimiter=',')
five_input = np.loadtxt('input.csv', dtype = float, delimiter=',')
arrow_input = np.loadtxt('arrow_input.csv', dtype=float,delimiter=',')
# denormalize the data
# five_temp[:,0] *= 4032 # width
# print(five_temp[1,0])
# five_temp[:,1] *= 3024 # height
# arrow_temp[:,0] *= 4032 # width
# arrow_temp[:,1] *= 3024 # height
# input[:,0] *= 4032 # width
# input[:,1] *= 3024 # height


# print(temp.shape)
# print(input.shape)
confident_col = np.ones((five_temp.shape[0],1))
five_temp = np.hstack((five_temp, confident_col))
arrow_temp = np.hstack((arrow_temp, confident_col))
arrow_input = np.hstack((arrow_input, confident_col))
five_input = np.hstack((five_input, confident_col))
print(five_temp.shape)

five_matrix, five_score = pose_affinematrix(five_input, five_temp, dst_area=1.0, hard=True)
arrow_matrix1, arrow_score1 = pose_affinematrix(five_input, arrow_temp, dst_area=1.0, hard=True)
arrow_matrix2, arrow_score2 = pose_affinematrix(arrow_input, arrow_temp, dst_area=1.0, hard=True)
#print(matrix.shape)
#print(input.shape)
# affined_input = warpAffinePoints(arrow_input[:,0:2], five_matrix)
# print(affined_input.shape)
# print(score)
# plt.scatter(arrow_temp[:,0], five_temp[:,1], c='b', label='five_template')
# plt.scatter(affined_input[:,0],affined_input[:,1],c='r', label='five_input')
# plt.legend()
# plt.show()
# print(five_score, arrow_score)

# score: fiveT_fiveI, arrowT_fiveI, arrowT_arrowI
print(five_score, arrow_score1, arrow_score2)