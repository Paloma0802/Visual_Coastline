import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import cv2


img = Image.open(r'rotated_final.png')
img_g = img.convert('L')
img_array = np.array(img_g)
img_array = cv2.medianBlur(img_array, 15)
row, col = img_array.shape

img_flat = img_array.flatten()
img_flat = img_flat[:, np.newaxis] / 255

km = KMeans(n_clusters=2, random_state=0).fit(img_flat)
reshape_label = np.reshape(km.labels_, img_array.shape)

"""
# 这部分好像没啥用==
kernal_r = 15
kernal = np.ones((kernal_r, kernal_r))
for i in range(kernal_r):
    for j in range(kernal_r):
        kernal[i, j] = np.exp(-(i - kernal_r / 2) ** 2 - (j - kernal_r / 2) ** 2)
kernal[kernal_r // 2 - 1, kernal_r // 2 - 1] = 0
kernal /= np.sum(kernal)
new = reshape_label
for run in range(5):
    change = np.ones((row,col))
    new_max = np.max(new)
    for i in range(kernal_r // 2, row - kernal_r // 2):
        for j in range(kernal_r // 2, col - kernal_r // 2):
            if np.sum(new[i - kernal_r // 2:i + kernal_r // 2 + 1,
                      j - kernal_r // 2:j + kernal_r // 2 + 1] * kernal)/new_max > 0.5:
                change[i, j] = 200
            else:
                change[i, j] = 0
    print(run)  # 计数用
img_array_pro = change
"""
img_array_pro = reshape_label * 200
cv2.imwrite('kmeans.png', img_array_pro)




