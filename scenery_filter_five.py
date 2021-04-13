import cv2
from matplotlib import pyplot as plt
import os
from PIL import Image
from PIL import ImageFilter

# 5.模糊滤镜1（风景）
def filter(t):
  file_name = 'static/scenery/original/yuantu/original.jpg'
  im = cv2.imread(file_name)
  im[:,:,:]=im[:,:,[2,1,0]]
  im = Image.fromarray(im)
  im = im.filter(ImageFilter.BLUR)
  save_path = 'static/scenery/colors/color-' +t + '.jpg'
  im.save(save_path)
