# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30  19:21:36 2023

@author: Rui
"""
from datetime import timedelta
import os
import subprocess
import sys
from transitions import Machine
from util.adb import adb_command, adb_command_full
from game_controller import GameController
import time
import config
import logging
import re

# 配置日志记录到文件
logging.basicConfig(filename='coc_robot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filemode='w')

offline_timer = 0
wait_wakeup_timer = 0

def check_prepare():
    if not os.path.exists(config.adb_path):
        print("no adb.exe")
        exit(0)
    
    cmd = adb_command_full( " devices", device = False)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    # 解析输出
    matches = re.findall(re.compile("(emulator-\d+)"), result.stdout)

    # 检查是否存在设备，需要开启开发者模式
    if len(matches) == 0:
        print("Pls confirm USB Debugging Mode has opened!")
        exit(0)
    elif len(matches) == 1:
        config.device_name = matches[0]
    else:
        if config.device_name == "":
            print("please select devices: ")
            for idx in range(len(matches)):
                print(f"{idx} : {matches[idx]}")
            print("please select devices: ")
            select_id = input()
            try:
                select_id = int(select_id)
                if select_id >= 0 and select_id < len(matches):
                    config.device_name = matches[select_id]
                else:
                    print("Invalid input! Exiting...")
                    exit(0)
            except ValueError:
                print("Invalid input! Exiting...")
                exit(0)

def update_text(text):
    sys.stdout.write("\r\033[K" + text)
    sys.stdout.flush()

def seconds_to_hms_string(seconds):
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

class GameScript:
    states = ['initializing', 'waiting', 'processing', 'finishing']
    waitting_time = 0
    start_task = False
    
    last_yyz = 0
    last_gain = 0
    last_donate = 0
    
    def __init__(self):
        self.machine = Machine(model=self, states=GameScript.states, initial='initializing')
        self.game_controller = GameController()

        self.machine.add_transition('initializing2waiting', 'initializing', 'waiting')
        self.machine.add_transition("waiting2initializing", 'waiting', 'initializing')
        self.machine.add_transition('start_processing', 'waiting', 'processing')
        self.machine.add_transition('finish', 'processing', 'finishing')
        self.machine.add_transition('start_init', 'waiting', 'initializing')
        self.machine.add_transition('processing2waiting','processing','waiting')

      
    def init(self):
        global offline_timer
        offline_timer = config.MAX_ONLINE_TIME

        # 转到等待状态
        self.waitting_time = 0
        self.initializing2waiting()
    
    def keep_clear_home(self):
        '''
        关闭主界面其余窗口，避免因误触界面其他按钮导致脚本暂停
        '''
        # 多次关闭，避免进入n级菜单
        for n in range(3):
            # 只使用一张截图判断
            game_script.game_controller.take_screenshot()
            game_script.game_controller.shot_new = False
            
            # 关闭窗口window
            if game_script.game_controller.click_by_name("close_window"):
                continue
            # 长时间未操作
            if game_script.game_controller.click_by_name("reload", use_cv=True):
                continue
            game_script.game_controller.shot_new = True
    
    def execute_game_action(self):
        global offline_timer
        if int(time.time()) - self.last_gain > config.gain_interval:
            if self.start_task is False:
                self.keep_clear_home()
                self.start_task = True
            if config.CLICK_LOG:
                logging.info("gain_base")
            update_text(f"processing. {seconds_to_hms_string(offline_timer)} s remaining. task: gain resourse") 
            self.last_gain = int(time.time())
            self.game_controller.gain_base()
            offline_timer -= int(time.time()) - self.last_gain

        if config.yyzhan and int(time.time()) - self.last_yyz > config.yyzhan_Interval: #控制频率
            if self.start_task is False:
                self.keep_clear_home()
                self.start_task = True
            if config.CLICK_LOG:
                logging.info('start yyzhan')
            update_text(f"processing. {seconds_to_hms_string(offline_timer)} s remaining. task: yyzhan")
            self.last_yyz = int(time.time())
            self.game_controller.yyzhan()
            offline_timer -= int(time.time()) - self.last_yyz
        
        if config.donate_troops and int(time.time()) - self.last_donate > config.donate_Interval:
            if self.start_task is False:
                self.keep_clear_home()
                self.start_task = True
            if config.CLICK_LOG:
                logging.info('start donate_troops')
            update_text(f"processing. {seconds_to_hms_string(offline_timer)} s remaining. task: donate troops")
            self.last_donate = int(time.time())
            self.game_controller.donate_troops()
            offline_timer -= int(time.time()) - self.last_donate
        if len(self.game_controller.train_troops) > 0 or len(self.game_controller.train_spells) > 0:
            update_text(f"processing. {seconds_to_hms_string(offline_timer)} s remaining. task: train troops")
            self.last_train = int(time.time())
            self.game_controller.train()
            offline_timer -= int(time.time()) - self.last_train
        
        self.start_task = False

if __name__ == "__main__":
    game_script = GameScript()
    while game_script.state != 'finishing':
        if game_script.state == 'initializing':
            update_text(f"initializing... ")
            check_prepare()
            print(f"select device: {config.device_name}")
            time.sleep(1)
            # 回到主界面
            adb_command("shell input keyevent 3")
            time.sleep(1)
            # 启动游戏--腾讯
            adb_command("shell am start -n com.tencent.tmgp.supercell.clashofclans/com.supercell.titan.tencent.GameAppTencent")
            game_script.init()
            sys.stdout.write("\n")
        elif game_script.state == 'waiting':
            update_text(f"waiting... {seconds_to_hms_string(wait_wakeup_timer)} s remaining")
            time.sleep(1)
            if wait_wakeup_timer > 0:
                wait_wakeup_timer -= 1
                if wait_wakeup_timer == 0 and to_init:
                    game_script.waiting2initializing()
                    sys.stdout.write("\n")
                continue
            to_init = True
            # 是否已经进入主界面
            if game_script.game_controller.match_yolo("add"):
                game_script.start_processing()
                continue
            # 系统维护 等待5分钟重试
            # if game_script.game_controller._match_template(["reload_maintenance"]):
            #     wait_wakeup_timer = 300
            #     # 退出
            #     adb_command("shell am force-stop com.tencent.tmgp.supercell.clashofclans")
            #     continue
            # # 版本更新
            # if game_script.game_controller._match_template(["new_version"]):
            #     game_script.game_controller.click_by_name("new_version_yes")
            #     wait_wakeup_timer = 60
            #     to_init = False
            #     continue
            #  # 版本更新安装，仅适用于雷电9模拟器
            # if game_script.game_controller.click_by_name("install"):
            #     to_init = False
            #     wait_wakeup_timer = 60
            #     continue
            # # 打开新版本
            # if game_script.game_controller.click_by_name("open_new_version"):
            #     to_init = False
            #     continue
            # # 更新错误
            # if game_script.game_controller._match_template(["update_error"],confidence=0.965):
            #     game_script.game_controller.click_by_name("exit") #退出
            #     wait_wakeup_timer = 10
            #     continue
            # # 被攻击中
            # if game_script.game_controller._match_template(["onatttacked"]):
            #     continue
            # 被攻击中-->回营
            game_script.game_controller.click_by_name("back_home")
            # 关闭活动界面
            game_script.game_controller.click_by_name("close_window")
            # 关闭月度大活动结算、升级完成
            game_script.game_controller.click_by_name("confirm")
            # 长时间未操作
            game_script.game_controller.click_by_name("reload", use_cv=True)

        elif game_script.state == 'processing':
            update_text(f"processing. {seconds_to_hms_string(offline_timer)} s remaining. task: idl")      
            if offline_timer > 0:
                time.sleep(1)
                offline_timer -= 1
                if offline_timer == 0:
                    # 退出
                    adb_command("shell am force-stop com.tencent.tmgp.supercell.clashofclans")
                    wait_wakeup_timer = config.WAKEUP_TIME
                    offline_timer = config.MAX_ONLINE_TIME
                    game_script.processing2waiting()
                    sys.stdout.write("\n")
            game_script.execute_game_action()
            offline_timer = offline_timer if offline_timer > 0 else 1
            #game_script.finish()