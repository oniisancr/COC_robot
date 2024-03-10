# COC_robot 
Supercell Clash of Clans Auto Robot； 部落冲突自动化脚本；
- 基本功能：
    1. 自动收集资源
    2. 自动捐兵（部分）
    3. 捐兵后，自动训练

- 使用：
    1. 首先，先下载[ADB](https://dl.google.com/android/repository/platform-tools_r34.0.5-windows.zip?hl=zh-cn)工具。
    2. 安装python依赖。`pip install -r requirements.txt`
    3. config.py文件中，修改`adb_path`，为自己的adb.exe路径。
        - 可简单配置部分功能开关
    4. 启动安卓模拟器。如雷电模拟器
        - 设置分辨率：720x1280，dpi: 320。
        - 确保调试模式已开启
    5. 执行脚本game_script.py
        - 存在多个设备时，选择指定设备(不建议运行多个)

## 注意事项

- **！！当前模型仅支持的下列元素识别：**
    - 兵种：气球、雷龙、飞龙、龙宝
    - 法术：狂暴、冰冻
- 脚本可能出现错误点击的情况
    - 可使用tools路径下 `yolo_test.py` 脚本来测试当前界面识别到的元素。
    - 若未正确匹配，请使用 `getdata.py`，请截图上传issuse。后续将加入训练集，完善识别结果。
<center>
<img src="images\yolo_valid_5.png" alt="测试图片" width="50%" />
</center>
