# COC_robot 
Supercell Clash of Clans Auto Robot； 部落冲突自动化脚本；
- 基本功能：
    1. 自动收集资源
    2. 自动捐兵
    3. 捐兵后，自动训练
- 准备：
    - [ADB](https://dl.google.com/android/repository/platform-tools_r34.0.5-windows.zip?hl=zh-cn)工具
    - 分辨率：1080x2400，dpi: 392
    - 开启设备调试功能、
- 使用：
    1. config.py文件中，修改`adb_path`，为自己的adb.exe路径。
        - 可简单配置部分功能开关
    2. 启动安卓模拟器。如雷电模拟器
        - 设置分辨率：1080x2400，dpi: 392。
        - 确保调试模式已开启
    3. 执行脚本game_script.py
        - 选择指定设备(不建议运行多个)

## 注意事项

- 脚本可能出现错误点击的情况，可使用`adb_test.py`脚本来截取自己设备上的元素，并替换images路径下的相同元素。
- 由于COC经常更新，建议使用dev分支代码，其包含了对最新的问题修复。