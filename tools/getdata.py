import subprocess
import time
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import adb_path  # Absolute import now works

index  = int(time.time()) % 100000
class_name = "shot"
subprocess.run(f"{adb_path} shell screencap -p /sdcard/screenshot.png", shell=True)
subprocess.run(f"{adb_path} pull /sdcard/screenshot.png ../model/dataset/images/{class_name}_{index}.png", shell=True)


