# COC_robot

> *⚠️ WARNING: Using automation scripts may violate game terms and result in account bans. This script is for educational purposes only. Use at your own risk!*

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/oniisancr/COC_robot)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/oniisancr/COC_robot)](https://github.com/oniisancr/COC_robot/commits/main)
[![Star History](https://api.star-history.com/svg?repos=oniisancr/COC_robot&type=Date)](https://star-history.com/#oniisancr/COC_robot)

<div align="center">
  <a href="README.md"><kbd>🇨🇳 中文</kbd></a> |
  <strong><kbd>🇺🇸 English</kbd></strong>
</div>

---

## Table of Contents

- [COC\_robot](#coc_robot)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Compatibility](#compatibility)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Quick Start](#quick-start)
    - [Custom Resolution](#custom-resolution)
  - [Model Training](#model-training)
    - [Dataset Preparation](#dataset-preparation)
    - [Training Command](#training-command)
  - [Notes](#notes)
  - [FAQ](#faq)
  - [Acknowledgements](#acknowledgements)

---

## Features

✅ **Auto Resource Collection**  

- Automated gold mine/elixir collector harvesting  
- Storage capacity detection via YOLOv5 model

⚔️ **Auto Troop Donation (Beta)**  

- Supports Electro Dragon/Balloon donations  
- Auto-train troops after donation

🔧 **Custom Configuration**  

- Multi-resolution support (1080p/720p/custom)  
- Modular feature toggle

---

## Compatibility

| Component       | Version Requirement      |
|-----------------|--------------------------|
| Clash of Clans  | v14.xxx (2023-10-01)     |
| LDPlayer        | 9.0.xx or higher         |
| OS              | Windows 10/11            |
| Python          | 3.9.1+                   |

---

## Getting Started

### Prerequisites

1. **Set Up ADB**  
   - Download [ADB Toolkit](https://dl.google.com/android/repository/platform-tools-latest-windows.zip)  
   - Add to system PATH ([Guide](https://www.xda-developers.com/install-adb-windows-macos-linux/))

2. **Install Python Dependencies**  

   ```bash
   pip install -r requirements.txt
   ```

### Quick Start

1. **Edit Configuration**  

   ```python
   # config.py
   adb_path = "C:/platform-tools/adb.exe"  # ← Replace with your path
   device_vm_size = 0  # 1080x2400 (default)
   enable_donate = True
   ```

2. **Start Emulator**  
   - Recommended resolution:  
     - **1080x2400** (DPI 440)  
     - **720x1280** (DPI 320)  
   - Enable USB Debugging

3. **Run Script**  

   ```bash
   python main.py
   ```

### Custom Resolution

1. Add new resolution config in `position.py`:  

   ```python
   elif device_vm_size == 2:  # Custom resolution
       COLLECTOR_POS = (x1, y1, x2, y2)
   ```

2. Submit a Pull Request to improve compatibility!

---

## Model Training

### Dataset Preparation

- [Data Annotation Guide](model/windows_v1.8.1/readme.md)  

```bash
model/
├── dataset/          # Labeled dataset
│   ├── images/       # Screenshot samples
│   └── labels/       # YOLO format labels
└── yolov5/           # Training code
```

### Training Command

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

[Full Training Guide](model/coc_train.ipynb)

---

## Notes

1. **Supported Elements**  

   | Type       | Names                      |
   |------------|----------------------------|
   | Troops     | Electro Dragon, Balloon    |
   | Spells     | Rage, Freeze, Lightning    |

2. **Debug Tools**  
   - Test UI recognition in real-time:  

     ```bash
     python tools/yolo_test.py
     ```

---

## FAQ

<details>
<summary>🔧 ADB Connection Failed?</summary>

1. Verify USB Debugging is enabled in emulator  
2. Restart ADB service:

   ```bash
   adb kill-server && adb start-server
   ```

3. Try different USB port/emulator version

</details>

<details>
<summary>🖱️ Inaccurate Click Positions?</summary>

1. Ensure emulator resolution is 1080x2400  
2. Adjust coordinates in `position.py`

</details>

---

## Acknowledgements

- Object detection framework [YOLOv5](https://github.com/ultralytics/yolov5)  

---

<sub>🐛 [Submit Issue](https://github.com/oniisancr/COC_robot/issues)</sub>
