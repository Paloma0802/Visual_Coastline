from data.GeoData import GeoData
from Utils.coastline import *
from Utils.median_blur import median_blur
from Utils.QComCheckBox import ComboCheckBox
from Utils.draw_lines import draw_lines
from Utils.predict import GM, Draw

import cv2
import sys

import numpy as np
import pandas as pd

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

        self.w2 = pg.ImageView() ## 添加图像展示的控件  # 可不可以不要在这里添加
        self.d2.addWidget(self.w2)

        # d3用于选择显示的时间范围

        self.label_cb = QtGui.QLabel("""选择展示海岸线的年份""")

        self.time_labels = ['None']
        self.cb = ComboCheckBox(['None'])

        self.w3 = pg.LayoutWidget()
        self.w3.addWidget(self.label_cb)
        self.w3.addWidget(self.cb)
        self.d3.addWidget(self.w3)

        # d4用于进行预测
        
        self.d4layout()

    def get_win(self):
        '''
        返回窗口，用于展示
        '''
        return self.win

    def d4layout(self):

        '''
        设计d4的布局
        '''

        self.w4 = pg.LayoutWidget()
        self.num = 180
        self.pred_year = 3
        self.history_year = 4
        self.now_year = 2020
        self.origin0 = [1300, 1800]

        numBtn = QtGui.QPushButton('射线条数')
        numBtn.setMinimumWidth(100)
        numText = QLineEdit()
        numText.setReadOnly(True)
        def onGetnum():
        	self.num,ok = QInputDialog.getInt(numBtn,'','射线条数')
        	if ok:
        		numText.setText(str(self.num))
        numBtn.clicked.connect(onGetnum)
        self.w4.addWidget(numBtn)
        self.w4.addWidget(numText)        

        predBtn = QtGui.QPushButton('预测年份数')
        predBtn.setMinimumWidth(100)
        predText = QLineEdit()
        predText.setReadOnly(True)
        def onGetpred():
        	self.pred_year,ok = QInputDialog.getInt(predBtn,'','输入预测出的年份数量')
        	if ok:
        		predText.setText(str(self.pred_year))
        predBtn.clicked.connect(onGetpred)
        self.w4.addWidget(predBtn)
        self.w4.addWidget(predText)     

        histBtn = QtGui.QPushButton('预测所需年份数')
        histBtn.setMinimumWidth(100)
        histText = QLineEdit()
        histText.setReadOnly(True)
        def onGethist():
        	self.history_year,ok = QInputDialog.getInt(histBtn,'','输入预测所需的年份数量')
        	if ok:
        		histText.setText(str(self.history_year))
        histBtn.clicked.connect(onGethist)
        self.w4.addWidget(histBtn, row = 1, col = 0)
        self.w4.addWidget(histText, row = 1, col = 1)

        nowBtn = QtGui.QPushButton('当前时间')
        nowBtn.setMinimumWidth(100)
        nowText = QLineEdit()
        nowText.setReadOnly(True)
        def onGetnow():
        	self.now_year,ok = QInputDialog.getInt(nowBtn,'','输入数据中最近的年份')
        	if ok:
        		nowText.setText(str(self.now_year))
        nowBtn.clicked.connect(onGetnow)
        self.w4.addWidget(nowBtn, row = 1, col = 2)
        self.w4.addWidget(nowText, row = 1, col = 3)

        predictBtn = QtGui.QPushButton('预测')
        predictBtn.setMinimumWidth(100)
        predictBtn.clicked.connect(self.Predict)
        self.w4.addWidget(predictBtn, row = 2, col = 0)

        self.d4.addWidget(self.w4)


    def fileDialog(self):

        '''
        对话窗口，用于选择数据所在的文件夹
        '''

        text = QFileDialog.getExistingDirectory(None, "请选择文件夹路径", "D:\\Qt_ui")

        GeoImgs = GeoData(text) # 初始化类
        imgs = GeoImgs.getImages() #获取原始图片

        # 定义裁剪范围(按行列号)
        W1, W2 = 2000, 5000
        H1, H2 = 4000, 5300
        # 裁剪图片
        subImgs = GeoImgs.subsetImages(W1, W2, H1, H2) 

        self.lines = {}
        self.lines_bold = {}
        self.time_labels = [k for k in subImgs.keys()]
        self.img_default = subImgs[self.time_labels[0]]
        self.row, self.col = self.img_default.shape

        for k in subImgs.keys():
            print('Processing image of date {k}'.format(k = k))            
            line, line_bold = coastline(subImgs[k])
            self.lines[k] = line
            self.lines_bold[k] = line_bold
        print('Finished')  
      
        self.d2.removeWidget(self.w2)
        self.w2.setImage(self.img_default)
        self.d2.addWidget(self.w2)
      
        self.d3.removeWidget(self.w3)
        self.w3 = pg.LayoutWidget()           
        self.cb = ComboCheckBox(self.time_labels)
        self.w3.addWidget(self.label_cb)
        self.w3.addWidget(self.cb)      
        self.d3.addWidget(self.w3)   

        self.get_time()

    def show_selected(self):
        '''
        返回被选中的年份，并展示相应年份的海岸线
        '''
        self.ret = []
        for i in range(1, len(self.items)):            
            if self.box_list[i].isChecked():
                self.ret.append(self.box_list[i].text())

        lines_bold = {}
        for k in self.ret:
            lines_bold[k] = self.lines_bold[k]
            print(lines_bold[k])

        # 将相应年份的海岸线绘制在底图上
        self.img_lined =  draw_lines(lines_bold, self.img_default)

        self.d2.removeWidget(self.w2)
        self.w2.setImage(self.img_lined)
        self.d2.addWidget(self.w2)

    def all_selected(self):
      """
      决定是否全选
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

        '''
        初始化与复选框相关的参数
        将复选动作与特定函数绑定起来
        '''
        self.box_list = self.cb.box_list
        self.state = self.cb.state
        self.items = self.cb.items

        for i in range(len(self.box_list)):

            if i == 0:
                self.box_list[i].stateChanged.connect(self.all_selected)
            else:
                self.box_list[i].stateChanged.connect(self.show_selected)
    
    def Predict(self):        
        '''
        点击预测按钮后进行预测
        '''
    # 输入canny后的图片构成的dict

        imgs = {}
        print('params', self.row, self.col, self.num, self.history_year, self.now_year, self.origin0)

        for k in self.lines.keys():  

            idx_r, idx_c = self.lines[k]
            print(idx_r, idx_c)
            imgs[k[0:4]] = np.zeros((self.row, self.col), dtype = np.uint8)
            imgs[k[0:4]][idx_r, idx_c] = 255
            cv2.imwrite(r'F:\LEARNING\2_Graduate\Lessons\Visulization\Final_PJ\Visual_Coastline\Result\img_canny.png', imgs[k[0:4]])

        for time in imgs.keys():
            
            print('times', time, type(time)) 
            final_dict = {}  # 输出字典用于后续预测
            pred_df = pd.DataFrame(None)
            # 输入图片，进行canny，这里可以去掉，连接上一步直接调取变量即可
            img = imgs[time]

            # 描点
            a = 0
            for alpha in np.arange(0, np.pi, np.pi / self.num):
                try:
                    left, right = Draw(alpha, img, self.row, self.col, self.origin0)
                except:
                    left,right = [alpha, -1], [np.pi + alpha, -1]
                    pass
                final_dict[left[0]] = left[1]
                final_dict[right[0]] = right[1]
                a += 1
                # print(a)
            pred_df['theta'] = final_dict.keys()
            print('pred_df0', pred_df)
            pred_df[str(time)] = final_dict.values()
            print('pred_df[str(time)]', pred_df[str(time)])
            print('pred_df', pred_df)
        pred_df = pred_df.sort_values(by='theta')
        print('pred_df.sorted', pred_df)
        pred_df = pred_df[np.min(pred_df.iloc[:, 1:].values, axis=1) > 0]
        print('pred_df1', pred_df)

        # 开始预测

        pred_dict = {}
        for i in range(len(pred_df['theta'].values)):
            theta_i = pred_df.iloc[i, 0]
            pred_x = pred_df.iloc[i, max(1, len(imgs) - self.history_year + 1):].values
            gm = GM(pred_x)
            try:
                gm.fit(pred_x)
                pred_conf = gm.confidence()
                pred = np.array(gm.predict(m = self.pred_year)[ - self.pred_year:])
                if pred_x[0]==pred_x[1] and pred_x[0]==np.average(pred_x):
                    pred_dict[theta_i] = np.average(pred_x) * np.ones(self.pred_year)
                else:
                    pred_dict[theta_i] = pred
            except:
                pass

        for k in range(self.now_year + 1, self.now_year + self.pred_year + 1):
            j = 0
            new_array = np.zeros((self.row, self.col))
#            self.lines_bold = {}
            print('pred_dict', pred_dict.keys())
            for i in pred_dict.keys():
                try:
                    x = np.rint(self.origin0[0] - pred_dict[i] * np.sin(i))
                    y = np.rint(self.origin0[1] + pred_dict[i] * np.cos(i))
                    x_k = int(x[k - self.now_year - 1])
                    y_k = int(y[k - self.now_year - 1])
                    print('x_k,y_k', x_k, y_k)
                    new_array[x_k, y_k] = 255
                    j += 1
                except:
                    pass

            print(np.where(new_array==255))
            print(new_array)

            edge_mod = np.zeros((self.row, self.col))
            flag = new_array / 255
            for i in range(3, self.row - 3):
                for j in range(3, self.col - 3):
                    if np.sum(flag[i - 3:i + 4, j - 3:j + 4]) / 49 > 0.01:
                        edge_mod[i, j] = 255

            self.lines_bold[str(k) +'_pred'] = np.where(edge_mod == 255)
#            print(self.lines_bold[str(k) + '_pred'])
#            print(self.lines_bold)

        self.time_labels = [k for k in self.lines_bold.keys()]
        self.d3.removeWidget(self.w3)
        self.w3 = pg.LayoutWidget()           
        self.cb = ComboCheckBox(self.time_labels)
        self.w3.addWidget(self.label_cb)
        self.w3.addWidget(self.cb)      
        self.d3.addWidget(self.w3)   
        self.get_time()

if __name__=='__main__':

    app = QApplication(sys.argv)
    Display = display()
    win = Display.get_win()
    win.show()
    sys.exit(app.exec_())

#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtGui.QApplication.instance().exec_()

    # 把切割后的子图选两张拼到一起，看看方位是否一致
    #merged = cv2.addWeighted(subImgs[20200225],0.7,subImgs[20200422],0.3,0)
    #cv2.imwrite('../Result/merged.png', merged)
