'''
cv2.imread 读取图片的通道是 BGR(210)，而 plt 展示出来的顺序是 RGB(012)
所以，我们在 cv2.imread 读取图片的时候，只需要调整一下通道顺序即可。
'''

##复古风滤镜（风景）
#import cv2
#import numpy as np
#from matplotlib import pyplot as plt
#import os
#from PIL import Image
#os.makedirs('outputs/filter(复古)', exist_ok=True)
#for file in os.listdir('image'):
#  file_name=os.path.basename(file) #获得文件名
#  img = Image.open('image/'+file_name)
#  img=np.array(img)
#  img[:,:,:]=img[:,:,[2,1,0]]
#  img = Image.fromarray(img)
#  img.save(os.path.join('outputs/filter(复古)', file_name))
#  plt.imshow(img)
#  plt.show()
  
  
#复古风滤镜（风景） 2
import cv2
import os
from PIL import Image



def filter(t):
  file_name='static/scenery/original/yuantu/original.jpg'
  im = cv2.imread(file_name)
  #复古滤镜
  im[:,:,:]=im[:,:,[0,1,2]] 
#  im[:,:,:]=im[:,:,[0,2,1]] 淡粉色
#  im[:,:,:]=im[:,:,[2,1,0]] 原图
#  im[:,:,:]=im[:,:,[2,0,1]] 淡绿色
#  im[:,:,:]=im[:,:,[1,2,0]] 淡紫色
#  im[:,:,:]=im[:,:,[1,0,2]] 偏紫偏绿
  im = Image.fromarray(im)
  save_path = 'static/scenery/colors/color-' + t + '.jpg'
  im.save( save_path)
