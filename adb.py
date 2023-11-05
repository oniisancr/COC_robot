# -*- coding: utf-8 -*-
"""
Created on Sun Nov 05  19:38:38 2023

@author: Rui
"""

# 使用adb控制设备
import subprocess
import time

import cv2
import numpy as np


def adb_command_full(command, adb_path = 'D:/platform-tools/adb.exe'):
    return adb_path + ' ' +command

def adb_take_screenshot():
    # 执行ADB命令截取屏幕并将输出保存到变量中
    adb_process = subprocess.Popen(adb_command_full("exec-out screencap -p"), shell=True, stdout=subprocess.PIPE)
    screenshot_bytes = adb_process.stdout.read()
    # 将二进制图像数据读取为NumPy数组
    screenshot_np = np.frombuffer(screenshot_bytes, np.uint8)
    # 使用OpenCV解码图像数据
    screenshot_cv = cv2.imdecode(screenshot_np, cv2.COLOR_RGB2BGR)
    return screenshot_cv
def adb_tap(x, y):
    adb_command = adb_command_full( f"shell input tap {x} {y}")
    subprocess.run(adb_command, shell=True)

def adb_swape(x1, x2, y1, y2):
    adb_command = adb_command_full( f"shell input swipe {x1} {x2} {y1} {y2}")
    subprocess.run(adb_command, shell=True)

def adb_command(cmd):
    adb_command = adb_command_full( cmd)
    subprocess.run(adb_command, shell=True)
    time.sleep(2)