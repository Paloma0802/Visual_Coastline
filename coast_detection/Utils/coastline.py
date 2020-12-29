import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
import cv2
from skimage import img_as_ubyte
import math
#import imutils

from Utils.median_blur import median_blur

'''
检测海岸线所需使用的函数
其中coastline函数引用本文件中其它函数完成了完整的流程
'''

###  中值模糊

def kmeans_blur(img):
    
#    img = cv2.medianBlur(img, 15)
    img = median_blur(img)

    img_flat = img.flatten()
    img_flat = img_flat[:, np.newaxis] / 255

    # 聚类
    km = KMeans(n_clusters=2, random_state=0).fit(img_flat)
    reshape_label = np.reshape(km.labels_, img.shape)

    img_kmeans = reshape_label * 200
    img_kmeans = img_kmeans.astype(np.uint8)

    return img_kmeans


### 二值化、反转
def reverse(img_kmeans):

    # 输出其实只用到了其中一行，就删去了其余部分
    ret3, img_reverse = cv2.threshold(img_kmeans, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return img_reverse

### 填洞
def FillHole(img_reverse):

    contours, hierarchy = cv2.findContours(img_reverse, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    len_contour = len(contours)

    img_filled = np.zeros_like(img_reverse, np.uint8)
    for i in range(len_contour):
        drawing = np.zeros_like(img_reverse, np.uint8)  # create a black image
        img_contour = cv2.drawContours(drawing, contours, i, (255, 255, 255), -1)
        img_filled = img_filled + img_contour
        # 更改了img_contour的存储方式，不再使用list存储中间结果，否则内存容易爆掉

    return img_filled


### 绘制边界
def canny(img_filled, img_gray):

    # 绘出边界

    edge = cv2.Canny(img_filled, 200, 300)

    line = np.where(edge == 255)

    row, col = edge.shape
    # 加粗边界线(Use滤波器)
    edge_mod = np.zeros((row, col))
    flag = edge / 255

    for i in range(4, row - 4):
        for j in range(4, col - 4):
            if np.sum(flag[i - 4:i + 5, j - 4:j + 5]) / 81 > 0.1:
                edge_mod[i, j] = 255

    line_bold = np.where(edge_mod == 255)

#    # 转换颜色(背景图和边线图均变为RGB)
#    edge = 255 - edge_mod
#    new_edge = np.zeros((row, col, 3), dtype = np.uint8)
#    img_rgb = np.zeros((row, col, 3))
#
#    idx_r, idx_c = np.where(edge!=255)
#    new_edge[idx_r, idx_c, :] = np.array([255, 0, 255], dtype = np.uint8)
#    new_edge[-idx_r, -idx_c, :] = np.array([255, 255, 255], dtype = np.uint8)
#
##    for i in range(row):
##        for j in range(col):
##            if edge[i, j] != 255:
##                new_edge[i, j] = np.array([255, 0, 255], dtype = np.uint8)
##            else:
##                new_edge[i, j] = np.array([255, 255, 255], dtype = np.uint8)
#
#    # 更改原for循环为broadcast
#    img_rgb = np.broadcast_to(np.expand_dims(img_gray, axis=2), (row, col, 3))
#
#    img_coast = cv2.addWeighted(img_rgb, (math.sqrt(5)-1)/2, new_edge,(math.sqrt(5)-1)/2,0)

    return line, line_bold


### 完整的海岸线绘制流程
def coastline(img):

    img = img_as_ubyte(img)

    # 进行聚类和中值模糊处理
    img_kmeans = kmeans_blur(img)
#    cv2.imwrite('/root/Coastline/Result/img_kmeans.png', img_kmeans)

    # 二值化并反转
    img_reverse = reverse(img_kmeans)
#    cv2.imwrite('/root/Coastline/Result/img_reverse.png', img_reverse)

    # 填充孔洞
    img_filled = FillHole(img_reverse)
    cv2.imwrite('/root/Coastline/Result/img_filled.png', img_filled)

    # 用canny方法绘制海岸线
#    img_coast = canny(img_filled, img)
    line, line_bold = canny(img_filled, img)
    return line, line_bold