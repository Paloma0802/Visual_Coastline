import cv2
import numpy as np
import os
from PIL import Image
from skimage import img_as_ubyte
import math

'''
将多条海岸线绘制在同一张底图上，不同年份的海岸线采用不同颜色
'''

def draw_lines(line_idxs, img_default):

    # 可选颜色范围
    color_list = [[0, 255, 255],
        [255, 228, 225],
        [0, 255, 0],
        [255, 193, 37],
        [255, 106, 106],
        [255, 0, 255],
        [155, 48, 255],
        [238, 0, 0],
        [205, 133, 63],
        [209, 95, 238],
        [0, 0, 139] ]

    row, col = img_default.shape
    
    img_lined = np.broadcast_to(np.expand_dims(img_default, axis=2), (row, col, 3))

    img_lined = img_as_ubyte(img_lined)
    
    # 更改array属性，使得其中的值可以改变
    img_lined.flags.writeable = True
    
    # 为每条线设置一个颜色，并将它画在图上
    for i, k in enumerate(line_idxs.keys()):

        color = color_list[i%11]
        idx_r, idx_c = line_idxs[k]
        img_lined[idx_r, idx_c, :] = np.array(color, dtype = np.uint8)
    
    return img_lined