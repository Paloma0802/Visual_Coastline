from Codes.data.GeoData import GeoData


if __name__=='__main__':

    GeoImgs = GeoData("../Data/", "TIF") # 初始化类

    imgs = GeoImgs.getImages() #获取原始图片

    # 定义裁剪范围
    W1, W2 = 2000, 5000
    H1, H2 = 4000, 5300

    # 裁剪图片
    subImgs = GeoImgs.subsetImages(W1, W2, H1, H2) 
    
    # 保存相应图片（提前创建Result文件夹）
    cv2.imwrite('../Result/subimg_1.png', subImgs[0])
    cv2.imwrite('../Result/subimg_2.png', subImgs[1])