# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30  19:21:36 2023

@author: Rui
"""
import sys
import pyautogui
from transitions import Machine
from game_controller import GameController
import time
import config

class GameScript:
    states = ['initializing', 'waiting', 'processing', 'finishing']
    waitting_time = 0
    
    last_yyz = 0
    last_gain = 0
    
    def __init__(self):
        self.machine = Machine(model=self, states=GameScript.states, initial='initializing')
        self.game_controller = GameController()

        self.machine.add_transition('start_waiting', 'initializing', 'waiting')
        self.machine.add_transition('start_processing', 'waiting', 'processing')
        self.machine.add_transition('finish', 'processing', 'finishing')
        self.machine.add_transition('start_idle', 'processing', 'waiting')

    def take_screenshot(self):
        self.screenshot = pyautogui.screenshot()
        return self.screenshot
    
    def execute_game_action(self):

        if int(time.time()) - self.last_gain > config.gain_interval:
            self.last_gain = int(time.time())
            self.game_controller.gain_base()

        if config.yyzhan and int(time.time()) - self.last_yyz > config.yyzhan_Interval: #控制频率
            self.last_yyz = int(time.time())
            print('友谊战')
            self.game_controller.yyzhan()
        

if __name__ == "__main__":
    game_script = GameScript()
    while game_script.state != 'finishing':
        if game_script.state == 'initializing':
            time.sleep(1)
            # 启动游戏
            game_script.start_waiting()
        elif game_script.state == 'waiting':
            if game_script.waitting_time <= 0:
                game_script.waitting_time = 0
                game_script.start_processing()
            else:
                game_script.waitting_time-=1
                # 长时间未操作reload
                time.sleep(1)
        elif game_script.state == 'processing':
            game_script.execute_game_action()
            time.sleep(1)
            # if False:
            #     game_script.finish()
            # time.sleep(1)
