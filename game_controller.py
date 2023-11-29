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
from queue import Queue
import logging
from adb import adb_swape, adb_take_screenshot, adb_tap

from config import CLICK_LOG

class GameController:
    light_screenshot = None
    gray_screenshot = None
    troop_name = []
    troop_small_name = []
    spell_name = []
    spell_small_name = []
    heap_tarin_troops = []      #训练任务
    queue_tarin_spells = []

    def __init__(self):
        self.template_images = {}
        self.queue_tarin_spells = Queue()
        # 用于保存所有按钮位置，不再重新匹配
        self.btn_map = {}
        folders = ['./images/btns', './images/troops', './images/troops_small','./images/spells','./images/spells_small']  # 以列表形式提供文件夹路径
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
                if folder_path == folders[3]:
                    self.spell_name.append(name)
                if folder_path == folders[4]:
                    self.spell_small_name.append(name)
        # 保存所有匹配的元素
        self.match_list = { }
        
        # input_string = "17,18,1,2,2,1"
        # elements = input_string.split(',')
        # for element in elements:
        #     heapq.heappush(self.heap_tarin_troops, int(element))
        # input_string = "spell1,spell3,spell4,spell4,spell3,spell2"
        # elements = input_string.split(',')
        # for element in elements:
        #     self.queue_tarin_spells.put(element)

        # 是否重新获取屏幕图像
        self.shot_new = True

    def take_screenshot(self, grayscale=True):
        self.screenshot = adb_take_screenshot()
        self.light_screenshot = self.screenshot
        if grayscale:
            self.screenshot = cv2.cvtColor(self.screenshot, cv2.COLOR_RGB2GRAY)
            self.gray_screenshot = self.screenshot
    
    def _match_template(self, search_images, confidence = 0.96, grayscale=True):
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
        self.take_screenshot()
        self.shot_new = False
        self.click_by_name("oil")
        self.click_by_name("gold")
        self.click_by_name("water")
        self.shot_new = True

    def yyzhan(self):
        self.click_by_name("open")
        op_set = ["yyz", "yyz_start"]
        if self.click_by_name(op_set[0]):
            self.click_by_name(op_set[1])
            time.sleep(1)
            self.click_by_name("close")


    def donate_troops(self):
        self.click_by_name("open")
        time.sleep(2)
        op_set = ["donate_troops","close_donate_window"]
        if self.click_by_name(op_set[0]):
            time.sleep(2)
            # 捐兵
            while self._match_template([op_set[1]]):
                light_items = self.get_light_items(self.troop_small_name)
                if len(light_items) > 0:
                    self.click(list(light_items.values())[0])
                    heapq.heappush(self.heap_tarin_troops, int((list(light_items.keys())[0])[5:].split('_')[0]))
                    # if CLICK_LOG:
                    logging.info("donate troops :" + (list(light_items.keys())[0]).split('_')[0])
                else:
                    # self.click_by_name("close_donate_window", True)
                    break
            #捐法术
            while self._match_template([op_set[1]]):
                light_items = self.get_light_items(self.spell_small_name)
                if len(light_items) > 0:
                    item_pos = list(light_items.values())[0]
                    item_name = list(light_items.keys())[0]
                    self.click(item_pos)
                    self.queue_tarin_spells.put(item_name.split('_')[0])
                    # if CLICK_LOG:
                    logging.info("donate spell :" + item_name.split('_')[0])
                else:
                    self.click_by_name("close_donate_window", True)
                    break
        self.click_by_name("close")
        if CLICK_LOG and len(self.heap_tarin_troops) > 0:
            logging.info('donated %d troops',len(self.heap_tarin_troops))

    def train(self):
        # 训练对应的捐兵
        if len(self.heap_tarin_troops) > 0 or self.queue_tarin_spells.qsize() > 0:
            is_Swaped = False   #只滑动一次
            self.click_by_name("train", True)
            if len(self.heap_tarin_troops) > 0:
                time.sleep(1 + random.random())
                self.click_by_name("train_troops")
                time.sleep(1 + random.random())
                while len(self.heap_tarin_troops) > 0:
                    item_name = "troop" + str(heapq.heappop(self.heap_tarin_troops))
                    train_troops_id = str(item_name)[5:]
                    if int(train_troops_id) > 16 and not is_Swaped:
                        # adb shell input swipe 1129 771 600 771
                        adb_swape(1129, 771, 600, 771)
                        is_Swaped = True
                        time.sleep(2.5)
                    if self.click_by_name(item_name):
                        if CLICK_LOG:
                            logging.info("train " + item_name )
                    else:
                        break
            if self.queue_tarin_spells.qsize() > 0:
                time.sleep(1 + random.random())
                self.click_by_name("train_spells")
                time.sleep(1 + random.random())
                while self.queue_tarin_spells.qsize() > 0:
                    item_name = self.queue_tarin_spells.get()
                    if self.click_by_name(item_name):
                        if CLICK_LOG:
                            logging.info("train " + item_name )
                    else:
                        break
            self.click_by_name("close_window_train", True)

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

    def click(self, loc):
        if loc is None:
            return False
        center_x = loc[0]
        center_y = loc[1]
        time.sleep(0.5+random.random()/2)
        adb_tap(center_x+random.randint(5,15), center_y+random.randint(5,15)) # 模拟鼠标点击匹配到的目标位置
        time.sleep(0.5+random.random()/2)
        return True

    def click_by_name(self, template_name, use_btn_buf = False):
        if CLICK_LOG:
            logging.info("click "+template_name)
        if template_name in self.btn_map:
            if not use_btn_buf:
                # 不使用缓存
                self.btn_map[template_name] = None       
            if self.click(self.btn_map[template_name]):
                return True
            else:
                self._match_template([template_name])
                return self.click(self.btn_map[template_name])
        else:
            self._match_template([template_name])
            if len(self.match_list) > 0:
                return self.click(list(self.match_list.values())[0])
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