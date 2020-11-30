import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import cv2

img = Image.open(r'new.TIF')

img_g = img.convert('L')
img_array = np.array(img_g)

img_array = cv2.medianBlur(img_array, 15)

row, col = img_array.shape

img_flat = img_array.flatten()
img_flat = img_flat[:, np.newaxis] / 255

km = KMeans(n_clusters=2, random_state=0).fit(img_flat)
reshape_label = np.reshape(km.labels_, img_array.shape)
"""
kernal_r = 15
kernal = np.ones((kernal_r, kernal_r))
for i in range(kernal_r):
    for j in range(kernal_r):
        kernal[i, j] = np.exp(-(i - kernal_r / 2) ** 2 - (j - kernal_r / 2) ** 2)
kernal[kernal_r // 2 - 1, kernal_r // 2 - 1] = 0
kernal /= np.sum(kernal)

new = np.zeros((row, col))
for i in range(kernal_r // 2, row - kernal_r // 2):
    for j in range(kernal_r // 2, col - kernal_r // 2):
        if np.sum(reshape_label[i - kernal_r // 2:i + kernal_r // 2 + 1,
                  j - kernal_r // 2:j + kernal_r // 2 + 1] * kernal) > 0.5:
            new[i, j] = 200
        else:
            new[i, j] = 0
img_array_pro = new
"""
img_array_pro = reshape_label * 200

img_final = Image.fromarray(img_array_pro)
#img_final.show()
#img_final.save(r'Kmeans.png')
cv2.imwrite('Kmeans.png', img_array_pro)
