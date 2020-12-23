# -*- coding: utf-8 -*-
"""
This example demonstrates the use of pyqtgraph's dock widget system.

The dockarea system allows the design of user interfaces which can be rearranged by
the user at runtime. Docks can be moved, resized, stacked, and torn out of the main
window. This is similar in principle to the docking system built into Qt, but 
offers a more deterministic dock placement API (in Qt it is very difficult to 
programatically generate complex dock arrangements). Additionally, Qt's docks are 
designed to be used as small panels around the outer edge of a window. Pyqtgraph's 
docks were created with the notion that the entire window (or any portion of it) 
would consist of dockable components.

"""
import cv2
from PyQt5.QtWidgets import (QApplication, QWidget, QInputDialog, QFormLayout,
                             QPushButton, QLineEdit)


import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.console
import numpy as np

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
d2 = Dock("Dock2 - Console", size=(500,300), closable=True)
d3 = Dock("Dock3", size=(500,400))
d4 = Dock("Dock4 (tabbed) - Plot", size=(500,200))
d5 = Dock("Dock5 - Image", size=(500,200))
d6 = Dock("Dock6 (tabbed) - Plot", size=(500,200))
area.addDock(d1, 'left')      ## place d1 at left edge of dock area (it will fill the whole space since there are no other docks yet)
area.addDock(d2, 'right')     ## place d2 at right edge of dock area
area.addDock(d3, 'bottom', d1)## place d3 at bottom edge of d1
area.addDock(d4, 'right')     ## place d4 at right edge of dock area
area.addDock(d5, 'left', d1)  ## place d5 at left edge of d1
area.addDock(d6, 'top', d4)   ## place d5 at top edge of d4

## Test ability to move docks programatically after they have been placed
area.moveDock(d4, 'top', d2)     ## move d4 to top edge of d2
area.moveDock(d6, 'above', d4)   ## move d6 to stack on top of d4
area.moveDock(d5, 'top', d2)     ## move d5 to top edge of d2


## Add widgets into each dock

## first dock gets save/restore buttons

#btnGetSel = QPushButton('列表选择输入对话框', self)
#btnGetSel.setMinimumWidth(min_width)
#btnGetSel.clicked.connect(self.onGetSelItem)
#self.infoSel = QLineEdit(self)
#self.infoSel.setReadOnly(True)

w1 = pg.LayoutWidget()
label = QtGui.QLabel(""" --说明-- 
本界面实现海岸线绘制及预测功能，用户需提前准备海岸卫星图片，并指定图片数据所在的位置。
""")
saveBtn = QtGui.QPushButton('数据目录')
saveBtn.setMinimumWidth(100)
infoText = QLineEdit()
infoText.setReadOnly(True)

def onGetText():
	print('running')
	text,ok=QInputDialog.getText(saveBtn,'输入数据所在目录','数据所在目录')
	if ok:
		infoText.setText(str(text))

saveBtn.clicked.connect(onGetText)
w1.addWidget(label, row=0, col=0)
w1.addWidget(saveBtn, row=1, col=0)
d1.addWidget(w1)
#state = None
#def save():
#    global state
#    state = area.saveState()
#def load():
#    global state
#    area.restoreState(state)
#saveBtn.clicked.connect(save)

w2 = pg.console.ConsoleWidget()
#size, ok = QtGui.QInputDialog.getDouble(None, "Create HDF5 Dataset?", "This demo requires a large HDF5 array. To generate a file, enter the array size (in GB) and press OK.", 2.0)
d2.addWidget(w2)

## Hide title bar on dock 3
d3.hideTitleBar()
img = cv2.imread('../../Result/img_coast_20200822.png')
w3 = pg.ImageView()
w3.setImage(img)
#w5.setImage(img)
#w3 = pg.PlotWidget(title="海岸线绘制")
#w3.plot(np.random.normal(size=100))
d3.addWidget(w3)

w4 = pg.PlotWidget(title="Dock 4 plot")
w4.plot(np.random.normal(size=100))
d4.addWidget(w4)

w5 = pg.ImageView()
w5.setImage(np.random.normal(size=(100,100)))
d5.addWidget(w5)

w6 = pg.PlotWidget(title="Dock 6 plot")
w6.plot(np.random.normal(size=100))
d6.addWidget(w6)

win.show()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()