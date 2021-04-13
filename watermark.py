import cv2
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def addWaterMark(testpath,save_path):
    # file_name = 'static/animal/original/yuantu/original-0.jpg'
    img = cv2.imread(testpath)
    img[:, :, :] = img[:, :, [2, 1, 0]]
    img = Image.fromarray(img)
    img = img.convert('RGBA')
    # 新建一个空白图片,尺寸与原图片一样
    txt = Image.new('RGBA', img.size, (0, 0, 0, 0))
    # print(type(txt))  #<class 'PIL.Image.Image'>
    # ImageFont.truetype(file,size) 设置字体(路径,大小)
    fnt = ImageFont.truetype("framd.ttf", 24)
    # 操作新建的空白图片>>将新建的图片添入画板
    d = ImageDraw.Draw(txt)
    # 在新建的图片上添加字体
    d.text((txt.size[0] - 100, txt.size[1] - 30), "Nostalgia", font=fnt, fill=(255, 255, 255, 255))
    # 合并两个图片
    img = Image.alpha_composite(img, txt)
    img = img.convert('RGB')
    # img.save(os.path.join('outputs/watermark', file_name))
    # save_path = 'static/scenery/colors/color-' + t + '.jpg'
    img.save(save_path)
