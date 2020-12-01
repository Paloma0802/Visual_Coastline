import numpy as np
import pandas as pd
import cv2

img = cv2.imread("bi.png", 0)
cv2.imwrite("canny.jpg", cv2.Canny(img, 200, 300))
#cv2.imshow("canny", cv2.imread("canny.jpg"))
cv2.waitKey()
cv2.destroyAllWindows()