# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31  23:31:49 2023
由于匹配准确度问题，放弃使用
@author: Rui
"""

import cv2
import os

folder_path = '../images/troops'
resize_percent = 0.665

files = os.listdir(folder_path)

for file in files:
    if file.endswith('.png'):
        file_path = os.path.join(folder_path, file)
        image = cv2.imread(file_path)  # 读取图像

        # 获取原始图像尺寸
        height, width = image.shape[:2]

        # 计算百分比对应的新尺寸
        new_width = int(width * resize_percent)
        new_height = int(height * resize_percent)
        dim = (new_width, new_height)

        # 缩放图像 INTER_AREA
        resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        # 构建新文件名
        filename, file_extension = os.path.splitext(file)
        new_filename = filename + '_1' + file_extension
        new_file_path = os.path.join('../images/troops_small', new_filename)

        # 保存缩小和重命名后的图像
        # cv2.imwrite(new_file_path, resized_image)
