
# 坐标信息
# adb shell getevent -l
# adb shell input tap 631 554

# adb shell wm density
# adb shell wm size

from config import device_vm_size

# 不同分辨率下的btn位置
if device_vm_size == 0:
    vm_size = [1080, 2400] # [width, height]竖屏
    screensz = [0, 0, vm_size[1], vm_size[0]] #横屏
    inner_chat = [796, 373] # 跳转部落内聊天按钮的位置
    down = [78, 946] # 跳转到最后
    train = [102,798]   # 左下角训练按钮
    train_troops = [831, 100]   # 跳转训练部队按钮的位置
    train_spells = [1119, 100]
    train_machine = [1433, 100]
    quick_train = [1744, 100]
    yyz_start = [1714, 660]
    open = [98, 498]    # 打开左侧聊天界面按钮的位置
    close_chat = [798, 551] # 关闭左侧聊天界面按钮的位置
elif device_vm_size == 1:
    vm_size = [720, 1280]
    screensz = [0, 0, 1280, 720]
    inner_chat = [533, 203]
    down = [53, 608]
    train = [46,519]
    train_troops = [382, 54]
    train_spells = [587, 56]
    train_machine = [800, 53]
    quick_train = [1000, 58]
    yyz_start = [986, 420]
    open = [50, 322]
    close_chat = [531, 366]