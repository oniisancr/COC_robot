# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30  19:22:47 2023

@author: Rui
"""
import os
import random
import time
import cv2
from queue import Queue
import logging

from util.adb import adb_swape, adb_take_screenshot, adb_tap
from util.positon import down, vm_size, inner_chat, train, train_troops, train_spells, screensz, yyz_start, train_machine, open, close_chat
import config
from config import CLICK_LOG
from util.yolo import YoloCOC

class GameController:
    screenshot = None
    light_screenshot = None
    gray_screenshot = None
    troops_name = []
    spells_name = []
    gc_name = []
    train_troops = []      #训练任务
    train_spells = []
    train_gcs = []
    yolo = None

    def __init__(self):
        self.template_images = {}
        folders = [os.path.join(os.path.dirname(__file__), 'images', 'btns')]
        for folder_path in folders:
            # 获取文件夹中所有 .png 格式的文件名
            png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
            for file in png_files:
                name = os.path.splitext(file)[0]  # 去除文件后缀
                self.template_images[name] = cv2.imread(os.path.join(folder_path, file))
        
        # 兵种与法术
        self.troops_name = ["fashi","gebulin","yemanren","juren","qiqiu","gongjianshou","leilong","longbao","zhadanren",
                            "xueguai","kuanggong","tianshi","feilong","longqishi","pika","kuanggong","wangling","nvwu","longqishi","toushou","liequan"]
        self.spells_name = ["shandian","bingdong","kuangbao","zhiliao","tantiao","tiepi","shanghai","bianfu","yinxing"]
        self.gc_name = ["gczhanche","gcqiqiu"]

        # 用于缓存元素位置
        self.btn_map = {}
        # 保存所有匹配的元素opencv
        self.match_list = { }
        
        # 加载yolo模型
        self.yolo = YoloCOC()

        # 是否重新获取屏幕图像
        self.shot_new = True

    def take_screenshot(self, grayscale=False):
        """截屏

        Args:
            grayscale (bool, optional): 截取图片. Defaults to False.
        """
        shot = adb_take_screenshot()
        if shot is None:
            return
        self.screenshot =  shot
        self.light_screenshot = self.screenshot
        if grayscale:
            self.screenshot = cv2.cvtColor(self.screenshot, cv2.COLOR_RGB2GRAY)
            self.gray_screenshot = self.screenshot
    
    def match_yolo(self, name="", range=screensz,  grayscale=True):
        """对象检测

        Args:
            name (str, optional): 对象元素. Defaults to "".
            range (list, optional): 对象所处范围. Defaults to screensz.
            grayscale (bool, optional): 是否检测灰色对象. Defaults to True.

        Returns:
            bool: 是否存在name对象
        """
        if self.shot_new:
            self.take_screenshot()  #只截取RGB 3通道图
        self.btn_map = self.yolo.detect(image=self.screenshot, range=range, gray=grayscale)
        if name in self.btn_map.keys():
            return True
        else:
            return False
    
    def _match_template(self, search_images, confidence = 0.95, grayscale=True):
        """寻找匹配元素
        Args:
            search_images (list): 需要寻找的元素名字
            confidence (float, optional): _description_. Defaults to 0.96.
            grayscale (bool, optional): 是否使用灰度. Defaults to True.

        Returns:
            bool: 是否存在一个匹配结果
        """
        if self.screenshot is None:
            print("warnning: no screenshot!")
            return False
        if self.shot_new:
            self.take_screenshot(grayscale)
        self.match_list.clear()
        #是否至少存在一个匹配对象
        flag = False
        for template_name in search_images:
            # 降低confidence
            if template_name in self.troops_name or template_name in self.spells_name:
                cur_confidence = 0.9
            else:
                cur_confidence = confidence
            template_image = self.template_images.get(template_name)
            if template_image is None:
                return False
            if grayscale:
                template_image = cv2.cvtColor(self.template_images[template_name], cv2.COLOR_BGR2GRAY)
            try:  
                res = cv2.matchTemplate(self.screenshot, template_image, cv2.TM_CCORR_NORMED)
                 # 找到最佳匹配位置
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > cur_confidence:
                    self.match_list[template_name] = max_loc
                    flag = True
                    if template_name in self.btn_map:
                        self.btn_map[template_name] = max_loc
            except Exception as e:
                print("PNG input buffer is incomplete")
                return flag
        return flag
    
    def gain_base(self):
        center_range = [ 118, 82, 1059, 571]
        # self.take_screenshot(False)
        self.click_by_name("oil", range=center_range)
        self.click_by_name("gold", range=center_range)
        self.click_by_name("water", range=center_range)
        self.click_by_name("tombstone", range=center_range)

    def yyzhan(self):
        self.click(open)
        time.sleep(2*config.timestep)
        self.click(inner_chat)
        op_set = ["yyz"]
        if self.click_by_name(op_set[0]):
            self.click(yyz_start)
            time.sleep(config.timestep)
            self.click(close_chat)

    def donate_troops(self):
        self.click(open)
        time.sleep(2*config.timestep)
        self.click(inner_chat)
        self.click(down)
        op_set = ["donate","close"]
        split_cnt = 3
        i = 0
        while i< split_cnt:
            # 分区域检测
            if self.click_by_name(op_set[0], range=[0,(vm_size[0]/split_cnt)*i,vm_size[1],(vm_size[0]/split_cnt)*(i+1) - 0.1*vm_size[0]]):
                range=[0.3*vm_size[1], 0, vm_size[1], 0.74*vm_size[0]]  #TODO 此range不一定适用所有分辨率 # 需要包括捐兵窗口，但不能包含聊天界面
                time.sleep(2*config.timestep)
                is_swipe =False
                # 捐兵
                while self.match_yolo(op_set[1], range=range, grayscale=False):
                    find_troops = set(self.btn_map.keys()).intersection(set(self.troops_name))
                    find_spells = set(self.btn_map.keys()).intersection(set(self.spells_name))
                    find_gcs = set(self.btn_map.keys()).intersection(set(self.gc_name))
                    if find_spells:
                        if self.click_by_name(list(find_spells)[0], range, use_btn_buf=True):
                            self.train_spells.append(list(find_spells)[0])   #记录捐兵信息
                            logging.info("donate spells :" + list(find_spells)[0])
                    if find_gcs:
                        if self.click_by_name(list(find_gcs)[0], range, use_btn_buf=True):
                            self.train_gcs.append(list(find_gcs)[0])   #记录捐兵信息
                            logging.info("donate gcs :" + list(find_gcs)[0])
                    if find_troops:
                        if self.click_by_name(list(find_troops)[0], range, use_btn_buf=True):
                            self.train_troops.append(list(find_troops)[0])   #记录捐兵信息
                            logging.info("donate troops :" + list(find_troops)[0])
                    # elif not is_swipe:
                    #     adb_swape(1019,220,640,220)
                    #     is_swipe = True
                    #     time.sleep(2.5)
                    #     continue
                    if not find_troops and not find_spells and not find_gcs:
                        self.click_by_name("close")
                        break
                time.sleep(config.timestep)
            i = i + 1
        self.click(close_chat)

    def train(self):
        # 训练对应的捐兵
        if len(self.train_troops) > 0 or len(self.train_spells) > 0 or len(self.train_gcs):
            is_Swaped = False   #只滑动一次
            self.click(train)
            time.sleep(1*config.timestep + random.random())
            range = [0, 0.5*vm_size[0], vm_size[1], vm_size[0]] #TODO 此range不一定适用所有分辨率 # 训练窗口的下半部分，用于限制识别范围
            if len(self.train_troops) > 0:
                time.sleep(1*config.timestep + random.random())
                self.click(train_troops)
                time.sleep(1*config.timestep + random.random())
                try_more_troops = False
                while len(self.train_troops) > 0:
                    self.match_yolo(range=range, grayscale=False)
                    find_troops = set(self.btn_map.keys()).intersection(set(self.train_troops))
                    if find_troops:
                        for troop in find_troops:
                            if self.click_by_name(troop, range, use_btn_buf=True):
                                logging.info("train troops :" + troop)
                            self.train_troops.remove(troop)
                            break  #每次训练一个
                    # elif not is_Swaped:
                    #     is_Swaped = True
                    #     adb_swape(718, 505, 280, 508)
                    #     time.sleep(2.5)
                    else:
                        self.train_troops.clear()
                        if try_more_troops:
                            break
                        else:
                            self.train_troops = ["qiqiu","leilong"]*30
                            try_more_troops = True
            if len(self.train_spells) > 0:
                time.sleep(1*config.timestep + random.random())
                self.click(train_spells)
                time.sleep(1*config.timestep + random.random())
                while len(self.train_spells) > 0:
                    item_name = self.train_spells.pop()
                    if self.click_by_name(item_name, range=range, gray=False):
                        logging.info("train " + item_name )
            if len(self.train_gcs) > 0:
                time.sleep(1*config.timestep + random.random())
                self.click(train_machine)
                time.sleep(1*config.timestep + random.random())
                while len(self.train_gcs) > 0:
                    item_name = self.train_gcs.pop()
                    if self.click_by_name(item_name, range=range, gray=False):
                        logging.info("train " + item_name )
            self.click_by_name("close", use_btn_buf=True)

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
        adb_tap(center_x+random.randint(1,10), center_y+random.randint(1,10)) # 模拟鼠标点击匹配到的目标位置
        time.sleep(0.5*config.timestep+random.random()/2)
        return True

    def click_by_name(self, template_name, range = screensz, use_btn_buf = False, gray=True, use_cv=False):
        """根据元素名进行点击

        Args:
            template_name (string): 需要查询的元素
            range: 点击的元素所处范围 [x1,y1,x2,y2] 左上角与右下角
            use_btn_buf (bool, optional): 是否使用缓存. Defaults to False. 不使用缓存
            gray: 是否可以点击灰色
            use_cv: 是否使用opencv来匹配需要点击的对象
        Returns:
            bool: 是否成功点击
        """
        if CLICK_LOG:
            logging.info("click "+template_name)
        if not use_btn_buf:
            # 不使用缓存
            self.btn_map[template_name] = None       
        if self.click(self.btn_map.get(template_name)):
            return True
        elif use_cv:
            if self._match_template([template_name]):
                position = list(self.match_list.values())[0]
                position = [position[0]+self.template_images.get(template_name).shape[1]/2, position[1]+self.template_images.get(template_name).shape[0]/2]
                return self.click(position)
        else:
            self.match_yolo(name=template_name, range=range, grayscale=gray)
            return self.click(self.btn_map.get(template_name))
    
    def show_rectangle(self):
        for key, value in self.match_list.items():
            # 标记匹配的位置
            bottom_right = (value[0] + self.template_images[key].shape[1], value[1] + self.template_images[key].shape[0])
            cv2.rectangle(self.screenshot, value, bottom_right, (0, 255, 0), 2)
            # 显示带有标记的屏幕截图
        cv2.imshow('Marked Targets', self.screenshot)
        cv2.waitKey(0)  # 显示 3 秒（单位为毫秒）
        cv2.destroyAllWindows()