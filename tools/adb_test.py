# -*- coding: utf-8 -*-
"""
Created on Sun Nov 05  11:35:38 2023

@author: Rui
"""
import subprocess
import cv2

import numpy as np

def adb_command_full(command, adb_path = 'D:/platform-tools/adb.exe'):
    return adb_path + ' '+command

def run_adb_command(command):
    try:
        output = subprocess.check_output(adb_command_full(command), shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return "Error executing command: " + e.output

def take_screenshot():
    # 执行ADB命令截取屏幕并将输出保存到变量中
    adb_process = subprocess.Popen(adb_command_full("exec-out screencap -p"), shell=True, stdout=subprocess.PIPE)
    screenshot_bytes = adb_process.stdout.read()

    # 将二进制图像数据读取为NumPy数组
    screenshot_np = np.frombuffer(screenshot_bytes, np.uint8)
    if len(screenshot_np) != 0:
    # 使用OpenCV解码图像数据
        screenshot_cv = cv2.imdecode(screenshot_np, cv2.IMREAD_COLOR)
        return screenshot_cv
    else:
        return None

if __name__ == "__main__":
    # 截取屏幕并将其保存到变量中
    screenshot = take_screenshot()
    if screenshot is not None:
        # 可以进行进一步的处理，比如显示图像
        cv2.imshow('Screenshot', screenshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # print(run_adb_command("devices"))

