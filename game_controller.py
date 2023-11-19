# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30  19:22:47 2023

@author: Rui
"""
import os
import random
import time
import cv2
import heapq
import logging
from adb import adb_swape, adb_take_screenshot, adb_tap

from config import CLICK_LOG

class GameController:
    light_screenshot = None
    gray_screenshot = None
    troop_name = []
    troop_small_name = []
    heap_tarin_troops = []      #训练任务

    def __init__(self):
        self.template_images = {}
        # 用于保存所有按钮位置，不再重新匹配
        self.btn_map = {}
        folders = ['./images/btn', './images/troops', './images/troops_small']  # 以列表形式提供文件夹路径
        for folder_path in folders:
            # 获取文件夹中所有 .png 格式的文件名
            png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
            for file in png_files:
                name = os.path.splitext(file)[0]  # 去除文件后缀
                self.template_images[name] = cv2.imread(os.path.join(folder_path, file))
                if folder_path == folders[0]:
                    self.btn_map[name] = None
                if folder_path == folders[1]:
                    self.troop_name.append(name)
                if folder_path == folders[2]:
                    self.troop_small_name.append(name)
        # 保存所有匹配的元素
        self.match_list = { }
        
        # input_string = "17,18,1,2,2,1"
        # elements = input_string.split(',')
        # for element in elements:
        #     heapq.heappush(self.heap_tarin_troops, int(element))
        # 是否重新获取屏幕图像
        self.shot_new = True

    def take_screenshot(self, grayscale=True):
        self.screenshot = adb_take_screenshot()
        self.light_screenshot = self.screenshot
        if grayscale:
            self.screenshot = cv2.cvtColor(self.screenshot, cv2.COLOR_RGB2GRAY)
            self.gray_screenshot = self.screenshot
    
    def _match_template(self, search_images, confidence = 0.95, grayscale=True):
        if self.shot_new:
            self.take_screenshot(grayscale)
        self.match_list.clear()
        #是否至少存在一个匹配对象
        flag = False
        for template_name in search_images:
            template_image = self.template_images[template_name]
            if grayscale:
                template_image = cv2.cvtColor(self.template_images[template_name], cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(self.screenshot, template_image, cv2.TM_CCORR_NORMED)
            # 找到最佳匹配位置
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val > confidence:
                self.match_list[template_name] = max_loc
                flag = True
                if template_name in self.btn_map:
                    self.btn_map[template_name] = max_loc
        return flag
    
    def gain_base(self):
        self.click_by_name("oil")
        self.click_by_name("gold")
        self.click_by_name("water")

    def yyzhan(self):
        
        op_set = {"open", "yyz", "yyz_start"}
        # 找到可以操作的状态(图片)
        while True:
            self._match_template(op_set)
            op_cover = list(set(self.match_list) & set(op_set))
            if len(op_cover) == 0:
                break
            else:
                self.click_by_name(op_cover[0])
                if "yyz_start" == op_cover[0]:
                    time.sleep(2)
                    # 回到主界面
                    self.click_by_name("close")
                    break
                op_set.remove(op_cover[0])
            time.sleep(1)

    def donate_troops(self):
        self.click_by_name("open", False)
        op_set = {"donate_troops","close_donate_window"}

        # 找到可以操作的状态(图片)
        while True:
            self._match_template(op_set)
            op_cover = list(set(self.match_list) & set(op_set))
            if len(op_cover) == 0:
                break
            else:
                if(op_cover[0] != "close_donate_window"):
                    self.click_by_name(op_cover[0])
                    op_set.remove(op_cover[0])
                else:
                    # 捐兵
                    light_items = self.get_light_items(self.troop_small_name)
                    if len(light_items) > 0:
                        self.click(list(light_items.values())[0])
                        heapq.heappush(self.heap_tarin_troops, int((list(light_items.keys())[0]).split('_')[0]))
                        if CLICK_LOG:
                            logging.info("donate " + (list(light_items.keys())[0]).split('_')[0])
                    else:
                        self.click_by_name("close_donate_window")
                        break
            time.sleep(1)
        time.sleep(1)
        self.click_by_name("close", False)
        if CLICK_LOG and len(self.heap_tarin_troops) > 0:
            logging.info('donated %d troops',len(self.heap_tarin_troops))

    def train(self):
        # 训练对应的捐兵
        if len(self.heap_tarin_troops) > 0:
            self.click_by_name("train")
            time.sleep(1 + random.random())
            self.click_by_name("train_troops", duration = 1)
            time.sleep(1 + random.random())
            while len(self.heap_tarin_troops) > 0:
                train_trops_id = str(heapq.heappop(self.heap_tarin_troops))
                if int(train_trops_id) > 16:
                    # adb shell input swipe 1129 771 600 771
                    adb_swape(1129, 771, 600, 771)
                    time.sleep(2)
                self._match_template([train_trops_id])
                if len(self.match_list) > 0:
                    self.click_by_name(list(self.match_list.keys())[0])
                    if CLICK_LOG:
                        logging.info("train " + list(self.match_list.keys())[0])
                else:
                    break
            self.click_by_name("close_window_train")

    def get_light_items(self, search_images):
        light_items = {}
        self._match_template(search_images)

        for key, value in self.match_list.items():
            b, g, r = self.light_screenshot[value[1]+30, value[0]+30] #往右下角偏移一点

            # 检查颜色是否为灰色
            if b == g and g == r:
                continue
            else:
                light_items[key] = value
        return light_items

    def click(self, loc, duration=0):
        if loc is None:
            return False
        center_x = loc[0]
        center_y = loc[1]
        time.sleep(duration)
        time.sleep(0.65+random.random())
        adb_tap(center_x+random.randint(0,10), center_y+random.randint(0,10)) # 模拟鼠标点击匹配到的目标位置
        return True

    def click_by_name(self, template_name, use_btn_buf = True, duration = 0):
        if CLICK_LOG:
            logging.info("click "+template_name)
        if template_name in self.btn_map:
            if not use_btn_buf:
                # 不使用缓存
                self.btn_map[template_name] = None       
            if self.click(self.btn_map[template_name], duration):
                return True
            else:
                self._match_template([template_name])
                return self.click(self.btn_map[template_name], duration)
        else:
            self._match_template([template_name])
            if len(self.match_list) > 0:
                return self.click(list(self.match_list.values())[0], duration)
            else:
                return False
    
    def show_rectangle(self):
        for key, value in self.match_list.items():
            # 标记匹配的位置
            bottom_right = (value[0] + self.template_images[key].shape[1], value[1] + self.template_images[key].shape[0])
            cv2.rectangle(self.screenshot, value, bottom_right, (0, 255, 0), 2)
            # 显示带有标记的屏幕截图
        cv2.imshow('Marked Targets', self.screenshot)
        cv2.waitKey(0)  # 显示 3 秒（单位为毫秒）
        cv2.destroyAllWindows()