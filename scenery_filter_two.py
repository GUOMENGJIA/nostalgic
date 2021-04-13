import cv2
import matplotlib.pyplot as plt
import os
from PIL import Image
from flask import session


# 2.边缘检测滤镜（风景+人+动物  景物的效果最好）


def filter(t):
  file_name = 'static/scenery/original/yuantu/original.jpg'
  img = cv2.imread(file_name)
  img[:,:,:]=img[:,:,[2,1,0]]
  img = cv2.Canny(img,100,300)
  img = Image.fromarray(img)
  save_path = 'static/scenery/colors/color-' + t + '.jpg'
  img.save(save_path)