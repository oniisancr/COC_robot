# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02  21:55:23 2023

@author: Rui
"""
import sys
sys.path.append('E:\github\COC_robot')

import cv2
from game_controller import GameController

def showRectangle(screenshot, loc, length, width):
    if len(loc) > 0:
        # 标记匹配的位置
        bottom_right = (loc[0] + length, loc[1] + width)
        cv2.rectangle(screenshot, loc, bottom_right, (0, 255, 0), 2)
        # 显示带有标记的屏幕截图
        cv2.imshow('Marked Targets', screenshot)
        cv2.waitKey(0)  # 显示 2 秒（单位为毫秒）
        cv2.destroyAllWindows()


gc = GameController()

light_items = gc.get_light_items(search_images=["17_1"])
if len(light_items) > 0:
    showRectangle(gc.screenshot, list(light_items.values())[0], 125, 125)
else:
    print("未找到目标对象")


