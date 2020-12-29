from data.GeoData import GeoData
from Utils.coastline import *
from Utils.median_blur import median_blur
from Utils.QComCheckBox import ComboCheckBox

import cv2
import sys

from PyQt5.QtWidgets import *

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from pyqtgraph.dockarea import *

# 定义必要的操作函数

# 设置选择数据目录后对数据进行的操作

class display(QWidget):
    
    def __init__(self):
        super(display, self).__init__()

        '''
         初始化界面及窗口
        '''
#        app = QtGui.QApplication([])
        self.win = QtGui.QMainWindow()
        area = DockArea()
        self.win.setCentralWidget(area)
        self.win.resize(1000,500)
        self.win.setWindowTitle('海岸线绘制')

        '''
        创建子界面并设定其相对位置
        '''
        pg.setConfigOptions(imageAxisOrder='row-major')

        self.d1 = Dock("数据目录", size=(1, 1))   ## dock1, 用于选择数据所在目录  
        self.d2 = Dock("结果展示", size=(500,500)) ## dock2，用于展示绘制好的海岸线 
        self.d3 = Dock("时间范围选择", size = (500,200)) ## dock3, 用于选择显示的时间范围
        self.d4 = Dock("预测", size= (500,200))

        self.d1.hideTitleBar() ##隐去dock的标题
        self.d2.hideTitleBar()
        self.d3.hideTitleBar()
        self.d4.hideTitleBar()

        area.addDock(self.d1, 'left')      ## 把d1放到窗口左侧 
        area.addDock(self.d2, 'bottom', self.d1) ## 把d2放到d1下方
        area.addDock(self.d3, 'right', self.d1) ## 把d3放到d2右侧 
        area.addDock(self.d4, 'right', self.d2) ## 把d4放到d2右侧

        '''
        为每个dock添加控件
        '''

        ## d1用于获取数据所在目录
        w1 = pg.LayoutWidget()
        label = QtGui.QLabel(""" --说明-- 
        本界面实现海岸线绘制及预测功能，用户需提前准备海岸卫星图片，并指定图片数据所在的位置。
        """)
        dataBtn = QtGui.QPushButton('数据目录')
        dataBtn.setMinimumWidth(100)
        infoText = QLineEdit()
        infoText.setReadOnly(True)

        dataBtn.clicked.connect(self.fileDialog)
        w1.addWidget(label, row=0, col=0)
        w1.addWidget(dataBtn, row=1, col=0)
        self.d1.addWidget(w1)

        # d2用于展示绘制结果

        self.w3 = pg.ImageView() ## 添加图像展示的控件  # 可不可以不要在这里添加
        self.d2.addWidget(self.w3)

        # d3用于选择显示的时间范围

        label_cb = QtGui.QLabel("""时间范围""")

        self.time_labels = ['None']
        self.cb = ComboCheckBox(['None'])

        self.d3.addWidget(label_cb)
        self.d3.addWidget(self.cb)

        # d4用于进行预测

    def get_win(self):
         return self.win

    def fileDialog(self):

        text = QFileDialog.getExistingDirectory(None, "请选择文件夹路径", "D:\\Qt_ui")

        img_temp = cv2.imread(r'F:\LEARNING\2_Graduate\Lessons\Visulization\Final_PJ\Visual_Coastline\Result\img_coast_20200822.png')

        GeoImgs = GeoData(text) # 初始化类
        imgs = GeoImgs.getImages() #获取原始图片

        # 定义裁剪范围(按行列号)
        W1, W2 = 2000, 5000
        H1, H2 = 4000, 5300
        # 裁剪图片
        subImgs = GeoImgs.subsetImages(W1, W2, H1, H2) 
        self.time_labels = [k for k in subImgs.keys()]

        for k in subImgs.keys():
            img_coast = subImgs[k]
            break
    #        print('Processing image of date {k}'.format(k = k))
    #        img_coast = coastline(subImgs[k])
    #        break
    #    print('Finished')

        self.d2.removeWidget(self.w3)
        self.w3.setImage(img_coast)
        self.d2.addWidget(self.w3)

        self.d3.removeWidget(self.cb)
        self.cb = ComboCheckBox(self.time_labels)
        self.get_time()

        self.d3.addWidget(self.cb)

    def show_selected(self):
        self.ret = []
        for i in range(1, len(self.items)):            
            if self.box_list[i].isChecked():
                self.ret.append(self.box_list[i].text())

    def all_selected(self):
      """
      decide whether to check all
      :return:
      """
      # change state
      if self.state == 0:
        self.state = 1
        for i in range(1, len(self.items)):
          self.box_list[i].setChecked(True)
      else:
        self.state = 0
        for i in range(1, len(self.items)):
          self.box_list[i].setChecked(False)
      self.show_selected()

    def get_time(self):

        self.box_list = self.cb.box_list
        self.state = self.cb.state
        self.items = self.cb.items

        for i in range(len(self.box_list)):

            if i == 0:
                self.box_list[i].stateChanged.connect(self.all_selected)
            else:
                self.box_list[i].stateChanged.connect(self.show_selected)

        


if __name__=='__main__':

    app = QApplication(sys.argv)
    Display = display()
    win = Display.get_win()
    win.show()
    sys.exit(app.exec_())



#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtGui.QApplication.instance().exec_()

    #    pg.image(img_median, title="median")
    #    img_coast = coastline(subImgs[k])
    #    cv2.imwrite('/root/Coastline/Result/img_coast_{k}.png'.format(k = k), img_coast)
    
    # 保存相应图片（提前创建Result文件夹）
    #for k in subImgs.keys():
    #    cv2.imwrite('../Result/subimg_{num}.png'.format(num = k), subImgs[k])

    # 把切割后的子图选两张拼到一起，看看方位是否一致
    #merged = cv2.addWeighted(subImgs[20200225],0.7,subImgs[20200422],0.3,0)
    #cv2.imwrite('../Result/merged.png', merged)