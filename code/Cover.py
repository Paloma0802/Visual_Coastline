from PIL import Image
import math
img1 = Image.open('rbg_canny.png')
img2 = Image.open('rbg_new.png')

#进行图片重叠  最后一个参数是图片的权值
final_img2 = Image.blend(img1, img2, (math.sqrt(5)-1)/2)
final_img2.save('final.png')