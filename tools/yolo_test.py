import torch
from adb_test import take_screenshot

# 加载YOLOv5模型ultralytics/yolov5
model = torch.hub.load('ultralytics/yolov5', 'custom', '../util/best.pt')  # custom/local model
names = model.names

# img_path = '../coc_datasets/valid/yolo_valid_10.png'
# results = model.forward(img_path, size=1280)


results = model.forward(take_screenshot(), size=1280)
# 获取目标数量和检测结果
num_targets = len(results.pred[0]) if results and results.pred is not None else 0

print(f"检测到 {num_targets} 个目标:")

# 遍历每个检测到的目标并打印相似度
for i, det in enumerate(results.pred[0]):
    class_id = int(det[5])
    confidence = det[4]
    print(f"目标 {i + 1} - 类别: {names[class_id]}, 相似度: {confidence:.2f},坐标:{det[0]:.0f},{det[1]:.0f},{det[2]:.0f},{det[3]:.0f}")

results.show()

# import torch
# model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt', source='local')
# img_path = '../coc_datasets/valid/yolo_valid_10.png'
# result = model.forward(img_path, size=1280)
# result.show()