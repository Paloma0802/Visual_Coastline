import numpy as np
import cv2
import imutils
from PIL import Image


# 获取图片旋转角度
def get_minAreaRect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh < 255))
    return cv2.minAreaRect(coords)


img = cv2.imread('target.TIF')
angle = get_minAreaRect(img)[-1]

# 开始旋转
rotated = imutils.rotate_bound(img, angle)
cv2.imread('rotated.png')

# 去除黑边

img_r = Image.open('rotated.png').convert('L')
rotated_a = np.array(img_r)

rotated_a = cv2.medianBlur(rotated_a, 5)
rot_01 = np.where(rotated_a > 0, 1, 0)  # 中值滤波，去除黑色噪声

row, col = rot_01.shape
kernal = np.ones((3, 3))
x = []
y = []
for i in range(1, row - 1):
    for j in range(1, col - 1):
        if rot_01[i, j] == 1:
            x.append(j)
            y.append(i)
left = min(x)
right = max(x)
top = min(y)
bottom = max(y)

target_mod = rotated[top:bottom, left:right + 1]
cv2.imwrite('rotated_final.png', target_mod)
