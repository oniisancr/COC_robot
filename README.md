
# COC_robot

> *⚠️ 警告：使用自动化脚本可能违反游戏条款，存在封号风险。本脚本仅供学习交流，请勿用于主账号！*  
> *⚠️ Warning: Using automation scripts may violate game terms. Use at your own risk!*

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/oniisancr/COC_robot)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/oniisancr/COC_robot)](https://github.com/oniisancr/COC_robot/commits/main)
[![Star History](https://api.star-history.com/svg?repos=oniisancr/COC_robot&type=Date)](https://star-history.com/#oniisancr/COC_robot)

<div align="center">
  <a href="README-en.md"><kbd>🇺🇸 English</kbd></a> |
  <strong><kbd>🇨🇳 中文</kbd></strong>
</div>

---

## 目录

- [COC\_robot](#coc_robot)
  - [目录](#目录)
  - [功能](#功能)
  - [兼容性](#兼容性)
  - [使用方法](#使用方法)
    - [前置条件](#前置条件)
    - [快速开始](#快速开始)
    - [自定义分辨率](#自定义分辨率)
  - [自定义模型训练](#自定义模型训练)
    - [数据集准备](#数据集准备)
    - [训练命令](#训练命令)
  - [注意事项](#注意事项)
  - [常见问题](#常见问题)
  - [致谢](#致谢)

---

## 功能

✅ **自动资源收集**  

- 支持金矿、圣水收集器的定时收取  

⚔️ **自动捐兵（Beta）**  

- 支持雷龙、气球兵捐赠  
- 支持狂暴法术、冰冻法术、闪电法术捐赠
- 捐赠后自动训练部队

🔧 **自定义配置**  

- 多分辨率适配（1080p/720p/自定义）  
- 功能模块开关控制

---

## 兼容性

| 组件           | 版本要求               |
|----------------|-----------------------|
| 部落冲突       | v14.xxx (2023-10-01)  |
| 雷电模拟器     | 9.0.xx 或更高         |
| 操作系统       | Windows 10/11         |
| Python         | 3.9.1+                |

---

## 使用方法

### 前置条件

1. **配置 ADB**  
   - 下载 [ADB 工具包](https://dl.google.com/android/repository/platform-tools-latest-windows.zip)  
   - 解压后添加至系统 PATH（[教程](https://www.xda-developers.com/install-adb-windows-macos-linux/)）

2. **安装 Python 依赖**  

   ```bash
   pip install -r requirements.txt
   ```

### 快速开始

1. **编辑配置文件**  

   ```python
   # config.py
   adb_path = "C:/platform-tools/adb.exe"  # ← 修改为你的路径
   device_vm_size = 0  # 1080x2400（默认）
   enable_donate = True
   ```

2. **启动模拟器**  
   - 分辨率设置：  
     - **推荐**：1080x2400 (DPI 440)  
     - **备用**：720x1280 (DPI 320)  
   - 启用 USB 调试模式

3. **运行脚本**  

   ```bash
   python main.py
   ```

### 自定义分辨率

1. 在 `position.py` 中添加新分辨率配置：  

   ```python
   elif device_vm_size == 2:  # 自定义分辨率
       COLLECTOR_POS = (x1, y1, x2, y2)
   ```

2. 提交 Pull Request 帮助完善适配！

---

## 自定义模型训练

### 数据集准备

- [数据标注说明](model\windows_v1.8.1\readme.md)

```bash
model/
├── dataset/          # 标注数据集
│   ├── images/       # 截图样本
│   └── labels/       # YOLO 格式标注
└── yolov5/           # 训练代码
```

### 训练命令

```bash
cd model/yolov5
python train.py \
    --imgsz 640 \
    --batch-size 1\
    --epochs 1000 \
    --data ../data.yaml\
    --weights ../../util/best.pt\
    --patience 0 \
    --hyp ../hyp.game-ui.yaml

```

[查看完整训练指南](model/coc_train.ipynb)

---

## 注意事项

1. **支持识别的元素**  

   | 类型   | 名称                     |
   |--------|--------------------------|
   | 部队   | 雷龙、气球兵       |
   | 法术   | 狂暴、冰冻、闪电         |

2. **调试工具**  
   - 使用 `tools/yolo_test.py` 实时测试界面识别：  

     ```bash
     python tools/yolo_test.py
     ```

---

## 常见问题

<details>
<summary>🔧 ADB 连接失败怎么办？</summary>

1. 检查模拟器的 USB 调试模式是否开启  
2. 重启 ADB 服务：

   ```bash
   adb kill-server && adb start-server
   ```

3. 尝试更换 USB 端口或模拟器版本

</details>

<details>
<summary>🖱️ 脚本点击位置不准确？</summary>

1. 确保模拟器分辨率为1080x2400

2. 根据错误地方调整 `position.py` 中的坐标

</details>

---

## 致谢

- 目标检测框架 [YOLOv5](https://github.com/ultralytics/yolov5)  

---

<sub>🐛 [提交 Issue](https://github.com/oniisancr/COC_robot/issues)</sub>
