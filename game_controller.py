# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30  19:22:47 2023

@author: Rui
"""
import random
import time
import cv2
import numpy as np
import pyautogui


class GameController:
    def __init__(self):
        self.template_images = {
            'oil': cv2.imread('images/btn/oil.png'),
            'water': cv2.imread('images/btn/water.png'),
            'gold': cv2.imread('images/btn/gold.png'),

            'yyz_start': cv2.imread('images/btn/yyz_start.png'),
            'yyz': cv2.imread('images/btn/yyz.png'),
            'open': cv2.imread('images/btn/open.png'),
            'close': cv2.imread('images/btn/close.png'),
            'close_window': cv2.imread('images/btn/close_window.png'),
            'add': cv2.imread('images/add.png')
        }
       

        # 保存所有匹配的元素
        self.match_list = { }   

    def take_screenshot(self):
        self.screenshot = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    
    def _match_template(self, search_images):
        self.take_screenshot()
        self.match_list.clear()
        for template_name in search_images:
            res = cv2.matchTemplate(self.screenshot, self.template_images[template_name], cv2.TM_CCORR_NORMED)
            threshold = 0.95
            loc = np.where(res >= threshold)
            if len(loc[0]) > 0:
                self.match_list[template_name] = loc
    
    def gain_base(self):
        print("收资源")
        # 任一 
        op_list = ["oil","gold","water"]
        
        self._match_template(op_list)
        for template_name in op_list:
            if self.match_list.get(template_name) is not None:
                self.clickOne(template_name)

    def yyzhan(self):
        
        op_set = {"open", "yyz", "yyz_start"}
        # 找到可以操作的状态(图片)
        while True:
            self._match_template(op_set)
            op_cover = list(set(self.match_list) & set(op_set))
            if len(op_cover) == 0:
                break
            else:
                self.clickOne(op_cover[0])
                if "yyz_start" == op_cover[0]:
                    time.sleep(2)
                    # 回到主界面
                    self._match_template(["close"])
                    if self.match_list.get("close") is not None:
                        self.clickOne("close")
                    break
                op_set.remove(op_cover[0])
            time.sleep(1)
    

    def clickOne(self, template_name):
        center_x = self.match_list[template_name][1][0] + self.template_images[template_name].shape[1] // 2
        center_y = self.match_list[template_name][0][0] + self.template_images[template_name].shape[0] // 2
        time.sleep(random.randint(1, 3)+random.random())
        pyautogui.click(center_x+random.randint(-10,10), center_y+random.randint(-10,10))  # 模拟鼠标点击匹配到的目标位置