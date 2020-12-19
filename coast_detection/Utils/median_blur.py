import numpy as np


def median_blur(img):

    h, w = np.shape(img)
    
    img_padding = np.zeros((h+2, w+2))

    img_padding[1:h+1, 1:w+1] = img

    img_blurred = []
    for i in range(h):
        for j in range(w):
            elem = np.median(img_padding[i:i+3,j:j+3])
            img_blurred.append(elem)

    img_blurred = np.array(img_blurred)
    img_blurred = img_blurred.reshape(h, -1)

    return img_blurred