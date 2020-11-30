from glob import glob
import numpy as np
import rasterio
import json, re, itertools, os
import matplotlib.pyplot as plt
import cv2 
from sklearn import preprocessing
from sklearn.cluster import KMeans

class GeoData():

    def __init__(self, data_path, ext):

        print("Searching for '%s' files in %s" % (ext, data_path))
        self.fileList = glob(os.path.join(data_path,"*."+ext))
        print("Found %d 'tif' files" % len(self.fileList))
        # It finally reads and loads selected images into arrays.
        print("Loading images")
        self.loads = [rasterio.open(bandPath) for bandPath in self.fileList]
        self.images = [load.read()[0] for load in self.loads]
        print("Done")

    def getImages(self):
        return self.images

    def getMinBounds(self):

        self.leftBound = np.min([self.loads[i].bounds.left for i in range(len(self.loads))])
        self.topBound = np.min([self.loads[i].bounds.top for i in range(len(self.loads))])
        self.rightBound = np.max([self.loads[i].bounds.right for i in range(len(self.loads))])
        self.bottomBound = np.max([self.loads[i].bounds.bottom for i in range(len(self.loads))])

    def subsetImages(self, w1, w2, h1, h2):

        # This function subsets images according the defined sizes.
        print("Subsetting images (%s:%s, %s:%s)" % (w1, w2, h1, h2))
        self.getMinBounds()
        subimgs = []
        reg = []
        for i in range(len(self.images)):

            load = self.loads[i]
            cols_left = (load.bounds.left - self.leftBound)/30
            reg_left =  np.insert(self.images[i], np.repeat(0,cols_left),0,axis=1) 

            cols_top = (load.bounds.top - self.topBound)/30
            reg_top = np.insert(reg_left, np.repeat(0,cols_top), 0, axis=0) # 到这里为止还是正常的图片

            h, w = np.shape(reg_top)
            cols_right = int((self.rightBound - load.bounds.right)/30)
            reg_right = np.append(reg_top, np.zeros((h,cols_right), dtype=np.uint16), axis=1)

            h, w = np.shape(reg_right)
            cols_bottom = int((self.bottomBound - load.bounds.bottom )/30)
            reg_full = np.append(reg_right, np.zeros((cols_bottom, w), dtype=np.uint16), axis=0)

            subimg = reg_full[h1:h2, w1:w2]
            subimgs.append(subimg)
            reg.append(reg_full)

        print("Done")
        return subimgs,reg, reg_left, reg_top, reg_right


if __name__=='__main__':

    date = "2014-02-01"
    GeoImgs = GeoData("../Data/"+ date, "TIF")
    imgs = GeoImgs.getImages()

    W1, W2 = 2000, 5000
    H1, H2 = 4000, 5300

    subImgs, reg, reg_left, reg_top, reg_right = GeoImgs.subsetImages(W1, W2, H1, H2) 
    
    cv2.imwrite('../Result/subimg_1.png', subImgs[0])
    cv2.imwrite('../Result/subimg_2.png', subImgs[1])
#    cv2.imwrite('../Result/reg_full_1.png', reg[0])
#    cv2.imwrite('../Result/reg_full_2.png', reg[1])

