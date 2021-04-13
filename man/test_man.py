import os
import numpy as np
import matplotlib.pyplot as plt
from flask import session
from skimage.color import lab2rgb, rgb2lab, rgb2gray
import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import datasets, transforms


class GrayscaleImageFolder(datasets.ImageFolder):
    '''Custom images folder, which converts images to grayscale before loading'''

    def __getitem__(self, index):
        path, target = self.imgs[index]
        img = self.loader(path)
        if self.transform is not None:
            img_original = self.transform(img)
            img_original = np.asarray(img_original)
            img_lab = rgb2lab(img_original)
            img_lab = (img_lab + 128) / 255
            img_ab = img_lab[:, :, 1:3]
            img_ab = torch.from_numpy(img_ab.transpose((2, 0, 1))).float()
            img_original = rgb2gray(img_original)
            img_original = torch.from_numpy(img_original).unsqueeze(0).float()
        return img_original, img_ab, target


class ColorizationNet(nn.Module):
    def __init__(self, input_size=128):
        super(ColorizationNet, self).__init__()
        MIDLEVEL_FEATURE_SIZE = 128
        ## First half: ResNet
        resnet = models.resnet18(num_classes=365)
        # Change first conv layer to accept single-channel (grayscale) input
        resnet.conv1.weight = nn.Parameter(resnet.conv1.weight.sum(dim=1).unsqueeze(1))
        # Extract midlevel features from ResNet-gray
        self.midlevel_resnet = nn.Sequential(*list(resnet.children())[0:6])
        ## Second half: Upsampling
        self.upsample = nn.Sequential(
            nn.Conv2d(MIDLEVEL_FEATURE_SIZE, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(128, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(64, 32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 2, kernel_size=3, stride=1, padding=1),
            nn.Upsample(scale_factor=2)
        )

    def forward(self, input):
        # Pass input through ResNet-gray to extract features
        midlevel_features = self.midlevel_resnet(input)
        # Upsample to get colors
        output = self.upsample(midlevel_features)
        return output


def to_rgb(grayscale_input, ab_input, save_path=None):
    plt.clf()  # clear matplotlib
    color_image = torch.cat((grayscale_input, ab_input), 0).numpy()  # 横着拼接图片
    color_image = color_image.transpose((1, 2, 0))  # rescale for matplotlib
    color_image[:, :, 0:1] = color_image[:, :, 0:1] * 100
    color_image[:, :, 1:3] = color_image[:, :, 1:3] * 255 - 128
    color_image = lab2rgb(color_image.astype(np.float64))
    plt.imsave(arr=color_image, fname=save_path)


# 测试单张/多张图片代码
def test_man():

    test_transforms = transforms.Compose([transforms.Resize(220), transforms.CenterCrop(224)])
    # test_imagefolder = GrayscaleImageFolder('D:/郭/大学课程/4-大四/毕业设计/照片上色/static/man/original/', test_transforms)
    test_imagefolder = GrayscaleImageFolder('./static/man/original/', test_transforms)
    test_loader = torch.utils.data.DataLoader(test_imagefolder, batch_size=1, shuffle=False)

    model = ColorizationNet()
    # model.load_state_dict(torch.load('D:/郭/大学课程/4-大四/毕业设计/照片上色/man/人物-model-epoch-54-losses-0.001934.pth'))
    model.load_state_dict(torch.load('./man/人物-model-epoch-54-losses-0.001934.pth'))
    model.eval()


    for i, (input_gray, input_ab, target) in enumerate(test_loader):
        output_ab = model(input_gray)
        # 将图像保存到文件
        for j in range(len(output_ab)):
            save_path = 'static/man/colors/color-' + str(session['man']) + '.jpg'
            to_rgb(input_gray[j].cpu(), ab_input=output_ab[j].detach().cpu(), save_path=save_path)
