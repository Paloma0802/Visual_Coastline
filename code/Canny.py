import numpy as np
import cv2

img = cv2.imread(r'fill.png', 0)
raw_img = cv2.imread(r'rotated_final.png', 0)

# 绘出边界

edge = cv2.Canny(img, 200, 300)
row, col = edge.shape
cv2.imwrite('canny.png', edge)
"""
# 加粗边界线(Use滤波器)
edge_mod = np.zeros((row, col))
flag = edge / 255

for i in range(4, row - 4):
    for j in range(4, col - 4):
        if np.sum(flag[i - 4:i + 5, j - 4:j + 5]) / 81 > 0.1:
            edge_mod[i, j] = 255
cv2.imwrite('edge_mod.png', edge_mod)

# 转换颜色(背景图和边线图均变为RGB)
edge_mod = cv2.imread('edge_mod.png')
edge = 255 - edge_mod
new_edge = np.zeros((row, col, 3))
new_tif = np.zeros((row, col, 3))

for i in range(row):
    for j in range(col):
        if any(edge[i, j] != 255):
            new_edge[i, j] = np.array([255, 0, 255])
        else:
            new_edge[i, j] = np.array([255, 255, 255])
cv2.imwrite('rbg_canny.png', new_edge)


for i in range(row):
    for j in range(col):
        new_tif[i, j] = np.ones(3) * raw_img[i, j]
cv2.imwrite('rbg_new.png', new_tif)

# cv2.imshow("canny", cv2.imread(r'canny.png'))
cv2.waitKey()
"""