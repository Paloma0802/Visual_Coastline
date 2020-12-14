import numpy as np
import cv2
import os



os.chdir(r"C:/Users/Thinkpad/Documents/Study/Python3/FDU/KeShiHua/PJ")
img_l = os.listdir('./step2')
raw_l = os.listdir('./Result')
for name1, name2 in zip(img_l, raw_l):
    filename = name1.split('.')[0]
    print(filename)
    # 绘出边界
    img = cv2.imread('./step2/' + name1)
    edge = cv2.Canny(img, 200, 300)
    row, col = edge.shape


    # 加粗边界线(Use滤波器)
    edge_mod = np.zeros((row, col))
    flag = edge / 255

    for i in range(4, row - 4):
        for j in range(4, col - 4):
            if np.sum(flag[i - 4:i + 5, j - 4:j + 5]) / 81 > 0.1:
                edge_mod[i, j] = 255
    cv2.imwrite('./Canny/' + name2, edge_mod)

    # 转换颜色(背景图和边线图均变为RGB)
    # edge_mod = cv2.imread('edge_mod.png')
    edge = 255 - edge_mod
    new_edge = np.zeros((row, col, 3))
    new_png = np.zeros((row, col, 3))
    
    for i in range(row):
        for j in range(col):
            if edge[i, j] != 255:
                new_edge[i, j] = np.array([255, 0, 255])
            else:
                new_edge[i, j] = np.array([255, 255, 255])
    cv2.imwrite('./step3/' + filename + '_canny.png', new_edge)
    
    raw_name = name2.split('.')[0]
    print(raw_name)
    raw_img = cv2.imread('./Result/' + name2)
    for i in range(row):
        for j in range(col):
            new_png[i, j] = np.ones(3) * raw_img[i, j]
    cv2.imwrite('./Raw_RGB/' + name2 + '.png', new_png)

