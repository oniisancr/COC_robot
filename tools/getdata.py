
import subprocess
import time

adb_path = 'D:/platform-tools/adb.exe'
index  = int(time.time()) % 10000
class_name = "shot"
# while True:
# for i in range(20):
subprocess.run(f"{adb_path} shell screencap -p /sdcard/screenshot.png", shell=True)
subprocess.run(f"{adb_path} pull /sdcard/screenshot.png ./{class_name}_{index}.png", shell=True)

    
