# COC_robot 
Supercell Clash of Clans Auto Robot； 部落冲突自动化脚本；
- 功能：
    1. 自动收集资源
    2. 自动捐兵
    3. 捐兵后，自动训练

- 准备：
    - [ADB](https://dl.google.com/android/repository/platform-tools_r34.0.5-windows.zip?hl=zh-cn)工具
    - 分辨率：1080x2400，dpi: 392
    - 开启设备调试功能、
    - python库：cv2

- 使用：
    1. config.py文件中，修改`adb_path`，为自己的adb.exe路径。
        - 可简单配置部分功能开关
    2. 启动安卓模拟器。
        - 设置分辨率：1080x2400，dpi: 392。
        - 确保调试模式已开启
    3. 执行脚本game_script.py
由于COC经常更新，建议使用dev分支代码，其包含了最新的问题修复。
---

## （OP） **期待你的提交**
1. 开发环境：
    - 雷电9安卓模拟器。 64位安卓9
    - 可使用adb_test.py 来截取更多的元素。
2. 希望你能参与完善的功能： （提交到dev分支）
    - 部落竞赛
    - 部落战
    - 打鱼
    - bug修复
    - ...
