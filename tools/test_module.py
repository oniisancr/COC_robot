# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02  21:55:23 2023

@author: Rui
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))  
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))  
sys.path.append(parent_dir)  

import cv2
from game_controller import GameController
from game_script import check_prepare

def showRectangle(screenshot, loc, length, width):
    if len(loc) > 0:
        # 标记匹配的位置
        bottom_right = (loc[0] + length, loc[1] + width)
        cv2.rectangle(screenshot, loc, bottom_right, (0, 255, 0), 2)
        # 显示带有标记的屏幕截图
        cv2.imshow('Marked Targets', screenshot)
        cv2.waitKey(0)  # 显示 2 秒（单位为毫秒）
        cv2.destroyAllWindows()

check_prepare()
gc = GameController()
gc.take_screenshot()
# light_items = gc.get_light_items(search_images=["17_1"])
# if len(light_items) > 0:
#     showRectangle(gc.screenshot, list(light_items.values())[0], 125, 125)
# else:
#     print("未找到目标对象")


gc._match_template(search_images=["close_activity","reload"],grayscale= True)
print("result: ")
for k, v in gc.match_list.items():
    print(k)
    showRectangle(gc.screenshot, list(v), 20, 20)

# gc.click_by_name("close_activity", use_cv=True)
