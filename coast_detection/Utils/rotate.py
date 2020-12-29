import numpy as np
import cv2
import imutils
from PIL import Image

'''
识别出倾斜图像的四个顶点并进行旋转，随后去除黑边
'''


def get_minAreaRect(image):
    '''
    获取图片旋转角度
    '''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh < 255))
    return cv2.minAreaRect(coords)

def rotation(img):
    '''
    旋转图片
    '''
    angle = get_minAreaRect(img)[-1]
    # 开始旋转
    rotated = imutils.rotate_bound(img, angle)

    row, col = rotated.shape
    kernal = np.ones((3, 3))
    x = []
    y = []
    for i in range(1, row - 1):
        for j in range(1, col - 1):
            if rotated[i, j] == 1:
                x.append(j)
                y.append(i)
    left = min(x)
    right = max(x)
    top = min(y)
    bottom = max(y)

    target_mod = rotated[top:bottom, left:right + 1]

    return target_mod