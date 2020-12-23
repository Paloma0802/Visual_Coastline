from data.GeoData import GeoData
from Utils.coastline import *
from Utils.median_blur import median_blur

import cv2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QInputDialog, 
                             QPushButton, QMainWindow, QFileDialog)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from pyqtgraph.dockarea import *

app = QtGui.QApplication([])
win = QtGui.QMainWindow()
area = DockArea()
win.setCentralWidget(area)
win.resize(1000,500)
win.setWindowTitle('海岸线绘制')

## Create docks, place them into the window one at a time.
# that size arguments are only a suggestion; docks will still have to
## fill the entire dock area and obey the limits of their internal widgets.

pg.setConfigOptions(imageAxisOrder='row-major')

d1 = Dock("Dock1", size=(1, 1))     ## give this dock the minimum possible size
d3 = Dock("Dock3", size=(500,400))
area.addDock(d1, 'left')      ## place d1 at left edge of dock area (it will fill the whole 
area.addDock(d3, 'bottom', d1)## place d3 at bottom edge of d1

## Add widgets into each dock

## first dock gets data directory
w1 = pg.LayoutWidget()
label = QtGui.QLabel(""" --说明-- 
本界面实现海岸线绘制及预测功能，用户需提前准备海岸卫星图片，并指定图片数据所在的位置。
""")
saveBtn = QtGui.QPushButton('数据目录')
saveBtn.setMinimumWidth(100)
infoText = QLineEdit()
infoText.setReadOnly(True)

def fileDialog():

    text = QFileDialog.getExistingDirectory(None, "请选择文件夹路径", "D:\\Qt_ui")

    img_temp = cv2.imread(r'F:\LEARNING\2_Graduate\Lessons\Visulization\Final_PJ\Visual_Coastline\Result\img_coast_20200822.png')

    GeoImgs = GeoData(text) # 初始化类
    imgs = GeoImgs.getImages() #获取原始图片

    # 定义裁剪范围(按行列号)
    W1, W2 = 2000, 5000
    H1, H2 = 4000, 5300
    # 裁剪图片
    subImgs = GeoImgs.subsetImages(W1, W2, H1, H2) 

    for k in subImgs.keys():
        print('Processing image of date {k}'.format(k = k))
        img_coast = coastline(subImgs[k])
        break
    print('Finished')

    global d3, d1, area, w3

    d3.removeWidget(w3)
    w3.setImage(img_coast)
    d3.addWidget(w3)

saveBtn.clicked.connect(fileDialog)
w1.addWidget(label, row=0, col=0)
w1.addWidget(saveBtn, row=1, col=0)
d1.addWidget(w1)

## Hide title bar on dock 3
d3.hideTitleBar()
w3 = pg.ImageView()
img_default = cv2.imread(r'F:\LEARNING\2_Graduate\Lessons\Visulization\Final_PJ\Visual_Coastline\coast_detection\Utils\default.PNG')
w3.setImage(img_default)
d3.addWidget(w3)

win.show()

if __name__=='__main__':

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

    #    pg.image(img_median, title="median")
    #    img_coast = coastline(subImgs[k])
    #    cv2.imwrite('/root/Coastline/Result/img_coast_{k}.png'.format(k = k), img_coast)
    
    # 保存相应图片（提前创建Result文件夹）
    #for k in subImgs.keys():
    #    cv2.imwrite('../Result/subimg_{num}.png'.format(num = k), subImgs[k])

    # 把切割后的子图选两张拼到一起，看看方位是否一致
    #merged = cv2.addWeighted(subImgs[20200225],0.7,subImgs[20200422],0.3,0)
    #cv2.imwrite('../Result/merged.png', merged)
