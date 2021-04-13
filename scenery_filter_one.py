#边界加强（风景）
import cv2
import numpy as np
# from flask import session
from matplotlib import pyplot as plt
import os
from PIL import Image
from PIL import ImageFilter


def filter(t):
  testpath = 'static/scenery/original/yuantu/original.jpg'
  save_path = 'static/scenery/colors/color-' +t + '.jpg'
  im = cv2.imread(testpath)
  im[:,:,:]=im[:,:,[2,1,0]]
  im = Image.fromarray(im)
  im = im.filter(ImageFilter.EDGE_ENHANCE)
  im.save(save_path)
