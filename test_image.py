# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29  14:49:32 2023

@author: Rui
"""
import random
import time
import numpy as np
import pyautogui
import cv2

class CvTool:
    _instance = None
    def __init__(self):
        self.screenshot = None
        self.image = None 
        self.template = None
        self.loc = []
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CvTool, cls).__new__(cls)
        return cls._instance
    def locateAllOnScreen(self, image, confidence=0.9, grayscale=False):
        self.screenshot = pyautogui.screenshot()
        self.image = image
        if grayscale:
            self.screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_RGB2GRAY)
            self.template = cv2.imread(image, 0)  #以灰度图像格式读取模板图像
        else:
            self.screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_RGB2BGR)
            self.template = cv2.imread(image)
        # 模板匹配
        res = cv2.matchTemplate(self.screenshot, self.template, cv2.TM_CCORR_NORMED)
        # 找到最佳匹配位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > confidence:
            self.loc = max_loc
        else:
            self.loc = []
    def showRectangle(self):
        if len(self.loc) > 0:
            # 标记匹配的位置
            bottom_right = (self.loc[0] + self.template.shape[1], self.loc[1] + self.template.shape[0])
            cv2.rectangle(self.screenshot, self.loc, bottom_right, (0, 255, 0), 2)
            # 显示带有标记的屏幕截图
            cv2.imshow('Marked Targets', self.screenshot)
            cv2.waitKey(2000)  # 显示 2 秒（单位为毫秒）
            cv2.destroyAllWindows()
    def isMatch(self):
        return len(self.loc) > 0
    def oneLoc(self):
        if len(self.loc) > 0:
            center_x = self.loc[0] + self.template.shape[1] // 2
            center_y = self.loc[1] + self.template.shape[0] // 2
            return center_x, center_y
    def clickOne(self):
        if len(self.loc) > 0:
            time.sleep(random.randint(1, 3)+random.random())
            center_x, center_y = self.oneLoc()
            pyautogui.click(center_x+random.randint(-10,10), center_y+random.randint(-10,10))  # 模拟鼠标点击匹配到的目标位置

if __name__ == "__main__":
    cmp = CvTool()
    image_path = './images/troops_small/9_1.png'
    res = cmp.locateAllOnScreen(image_path, confidence=0.93, grayscale=True)
    if cmp.isMatch():
        cmp.showRectangle()
        # cmp.clickOne()
    else:
        print("未找到目标对象")
