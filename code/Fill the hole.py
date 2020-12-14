import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def FillHole(mask):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    len_contour = len(contours)
    contour_list = []
    for i in range(len_contour):
        drawing = np.zeros_like(mask, np.uint8)  # create a black image
        img_contour = cv2.drawContours(drawing, contours, i, (255, 255, 255), -1)
        contour_list.append(img_contour)

    out = sum(contour_list)
    return out

os.chdir(r"C:/Users/Thinkpad/Documents/Study/Python3/FDU/KeShiHua/PJ")
img_l = os.listdir('./step1')
for name in img_l:
    filename = name.split('.')[0]
    #二值化
    img = cv2.imread('./step1/'+name, 0)
    # global thresholding
    ret1, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    # Otsu's thresholding
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # Otsu's thresholding
    # 阈值一定要设为 0 !
    ret3, th3 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # plot all the images and their histograms
    images = [img, 0, th1, img, 0, th2, img, 0, th3]

    # 反相
    # opencv读取图像

    img_shape = th3.shape  # 图像大小(565, 650, 3)

    h = img_shape[0]
    w = img_shape[1]
    # 彩色图像转换为灰度图像（3通道变为1通道）
    gray = th3

    # 最大图像灰度值减去原图像，即可得到反转的图像
    dst = gray

    # 填充
    # mask_in = cv2.imread('kmeans_reverse.png', 0)
    mask_out = FillHole(dst)
    cv2.imwrite('./step2/%s.png'%(filename+'_fill'), mask_out)