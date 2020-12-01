from data.GeoData import GeoData
import cv2


if __name__=='__main__':

    GeoImgs = GeoData("../Data/") # 初始化类

    imgs = GeoImgs.getImages() #获取原始图片

    # 定义裁剪范围(按行列号)
    W1, W2 = 2000, 5000
    H1, H2 = 4000, 5300

    # 裁剪图片
    subImgs = GeoImgs.subsetImages(W1, W2, H1, H2) 
    
    # 保存相应图片（提前创建Result文件夹）
    for k in subImgs.keys():
        cv2.imwrite('../Result/subimg_{num}.png'.format(num = k), subImgs[k])

    # 把切割后的子图选两张拼到一起，看看方位是否一致
    #merged = cv2.addWeighted(subImgs[20200225],0.7,subImgs[20200422],0.3,0)
    #cv2.imwrite('../Result/merged.png', merged)