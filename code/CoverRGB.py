import cv2
import numpy as np
import os
from PIL import Image
import math

os.chdir(r'C:/Users/Thinkpad/Documents/Study/Python3/FDU/KeShiHua/PJ')

img1 = cv2.imread('./Canny/subimg_20180205.png')
img2 = cv2.imread('./Canny/subimg_20190201.png')
img3 = cv2.imread('./Canny/subimg_20200225.png')

row = img1.shape[0]
col = img1.shape[1]

# 将三年的海岸线放在同一张图中，加上三原色
cover_img = np.ones((row, col, 3)) * 255
for i in range(row):
    for j in range(col):
        if np.sum(img1[i, j]) != 0:
            cover_img[i, j] = [255, 0, 0]
print('img1——蓝色——2018')
for i in range(row):
    for j in range(col):
        if np.sum(img2[i, j]) != 0:
            cover_img[i, j] = [0, 255, 0]
print('img2——绿色——2019')
for i in range(row):
    for j in range(col):
        if np.sum(img3[i, j]) != 0:
            cover_img[i, j] = [0, 0, 255]
print('img3——红色——2020')

cv2.imwrite('./Canny/cover_img.png', cover_img)

# 上海地图的背景变成双色

bi_img = cv2.imread(r"C:\Users\Thinkpad\Documents\Study\Python3\FDU\KeShiHua\PJ\step2\subimg_20180205_fill.png")
row, col = bi_img.shape[0], bi_img.shape[1]
for i in range(row):
    for j in range(col):
        if np.sum(bi_img[i, j]) > 0:
            bi_img[i, j] = np.array([0, 255, 255])
        else:
            bi_img[i, j] = np.array([255, 255, 255])

cv2.imwrite(r'C:\Users\Thinkpad\Documents\Study\Python3\FDU\KeShiHua\PJ\Canny\Yellow.png', bi_img)
final = Image.open(r"C:\Users\Thinkpad\Documents\Study\Python3\FDU\KeShiHua\PJ\Canny\cover_img.png")
raw = Image.open(r"C:\Users\Thinkpad\Documents\Study\Python3\FDU\KeShiHua\PJ\Canny\Yellow.png")
final_img = Image.blend(final, raw, (math.sqrt(5) - 1) / 2)
final_img.save(r'C:\Users\Thinkpad\Documents\Study\Python3\FDU\KeShiHua\PJ\Canny\final.png')
