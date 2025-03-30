@echo off

adb disconnect 127.0.0.1:16384
adb connect 127.0.0.1:16384

python main.py