from glob import glob
import numpy as np
import rasterio
import cv2 
import os

class GeoData():

    def __init__(self, data_path, Band = 'B5'):
        '''
        初始化类，读入data路径下全部图片
        data_path : 数据文件夹的绝对路径
        Band : 指定波段，默认为B5
        '''
        
        # 载入数据路径
        print("Searching for '%s' files in %s" % (Band, data_path))
        self.fileList = glob(os.path.join(data_path, '*' , "*{Band}*.TIF".format(Band = Band)))
        print("Found %d  %s 'tif' files" % (len(self.fileList), Band))

        # 载入数据
        print("Loading images")
        self.loads = {}
        self.images = {}
        for bandPath in self.fileList :
            time_label = os.path.split(bandPath)[-1].split('_')[-4]
            load = rasterio.open(bandPath)
            image = load.read()[0]
            self.loads[time_label] = load
            self.images[time_label] = image
        print("Done")

    def getImages(self):
        '''
        获取原始图片
        以dict形式返回，dict的key名称是数据的时间标签，如‘20200612’，每个key下含有一张图片
        '''
        return self.images

    def getMinBounds(self):
        '''
        获取图组的最大边界范围
        '''        
        self.leftBound = np.min([self.loads[k].bounds.left for k in self.loads.keys()])
        self.topBound = np.min([self.loads[k].bounds.top for k in self.loads.keys()])
        self.rightBound = np.max([self.loads[k].bounds.right for k in self.loads.keys()])
        self.bottomBound = np.max([self.loads[k].bounds.bottom for k in self.loads.keys()])

    def subsetImages(self, w1, w2, h1, h2):
        '''
        分割子图
        以dict形式返回，dict的key名称是数据的时间标签，如‘20200612’，每个key下含有一张图片
        '''
        # This function subsets images according the defined sizes.
        print("Subsetting images (%s:%s, %s:%s)" % (w1, w2, h1, h2))
        self.getMinBounds()
        self.subimgs = {}
        
        for k in self.images.keys():

            load = self.loads[k]
            cols_left = (load.bounds.left - self.leftBound)/30
            reg_left =  np.insert(self.images[k], np.repeat(0,cols_left),0,axis=1) 

            cols_top = (load.bounds.top - self.topBound)/30
            reg_top = np.insert(reg_left, np.repeat(0,cols_top), 0, axis=0) 

            h, w = np.shape(reg_top)
            cols_right = int((self.rightBound - load.bounds.right)/30)
            reg_right = np.append(reg_top, np.zeros((h,cols_right), dtype=np.uint16), axis=1)

            h, w = np.shape(reg_right)
            cols_bottom = int((self.bottomBound - load.bounds.bottom )/30)
            reg_full = np.append(reg_right, np.zeros((cols_bottom, w), dtype=np.uint16), axis=0)

            subimg = reg_full[h1:h2, w1:w2]
            self.subimgs[k] = subimg
            
        print("Done")
        return self.subimgs



