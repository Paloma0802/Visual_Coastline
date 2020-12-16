# Visual_Coastline

## 项目内容

Codes是代码目录

data文件夹存放与数据读取相关的代码

Utils文件夹包括一个文件coastline.py，里面定义了聚类、反转等绘制过程所需的函数。使用时可以单独import每个函数，实现所需的目的，也可以直接import coastline函数，该函数引用其它函数完成了完整的绘制流程，可以直接得到画好海岸线的图。

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

main.py可作为demo参考

## To do:

1、更改截取子图的方式，换成用地理坐标截取（现在是用array的行列号截取的）

2、其它方法是打包到GeoData里，还是另写一个类之类的？

3、试着自己实现median blur和reverse（可能会把各个函数从coastline里分离出来，写成单独的py文件，方便调试）



