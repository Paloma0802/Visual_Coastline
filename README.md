# Visual_Coastline

## Requirements

rasterio  (for GeoData)

numpy  sklearn  skimage  opencv  math  (for coastline detection)

PyQt5  pyqtgraph (for GUI)



## 项目内容

coast_detection是代码目录

main.py内构建了交互界面，把图像处理的过程嵌入到了交互界面中。

data文件夹存放与数据读取相关的代码

Utils文件夹存放各种数据处理和展示的方法，目前包括median_blur.py和coastline.py，后者定义了聚类、反转等绘制过程所需的函数。使用时可以单独import每个函数，实现所需的目的，也可以直接import coastline函数，该函数引用其它函数完成了完整的绘制流程，可以直接得到画好海岸线的图。

使用时还需要创建两个目录：Data，Result，这两个文件夹与Codes并列，分别用于存放原始数据与处理结果。

其中Data目录下请放入  【从国家地理云上下载的压缩文件直接解压后的文件夹】  无需更改文件夹名称与TIF文件名称

## GeoData使用方法

data文件夹下定义了一个叫做GeoData的数据类，它可以像其它库一样被import，包含两个初始化参数：

data_path : Data文件夹所在的绝对路径

Band: 需要使用的数据波段，默认为B5，使用时可以不显式指定

初始化GeoData之后，它会从Data目录下读入所有满足波段条件的TIF文件，并生成对应的时间标签。

调用GeoImgs中的getImages()方法，可以返回从Data目录读入的图片文件（未切割）。这些图片以dict的形式组织到一起，用对应的时间标签作为key可以获得特定时间的图片。

调用GeoImgs中的subsetImages(W1, W2, H1, H2)方法，可以返回按指定行列号切割的图片，同样以dict形式返回，key是时间标签。W1, W2, H1, H2分别是列号和行号。

以上两个函数不会将切割后的图片（或原始图片）写入png文件，需要自行CV2.imwrite（）

建议在Codes目录下写主函数，如果在其它目录下编程且需要导入GeoData模块，则要加入如下代码:

import sys

sys.path.append('GeoData.py文件所在绝对路径')

## To do:

1、实现灰色预测（顺便试着实现一下不依赖初始点的方法）

1.5、把合并多条海岸线的代码合并到主程序里

2、绘制窗口，实现界面独立于pythonIDE的功能, 与主程序合并，（后续需要考虑点击预测、时间线的图例（可能要用到matplotlib？），或者特定地区的预测（下拉框选择），有时间的话选择时间线的显示）

3、TIF文件里能不能读到图片拍摄的日期？随机输入图片序列是需要确定它们的日期的

4、试着自己实现threshold和canny（可能会把各个函数从coastline里分离出来，写成单独的py文件，方便调试）

5、更改截取子图的方式，换成用地理坐标截取（现在是用array的行列号截取的）(但如果是可以自由放缩的界面，就不需要搞这个了)




