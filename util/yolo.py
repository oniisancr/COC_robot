import os
import torch
import cv2
from util.positon import screensz

class YoloCOC:
    def __init__(self, model_path=None):
        # 如果未指定路径，使用默认路径
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'best.pt')
        # 加载模型
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', model_path)  # custom/local model
        self.model.eval()  # 设置为评估模式

    def detect(self, image, range=screensz, size=640, gray=True):
        """识别所有非灰色元素

        Args:
            image (string/NumPy): image path or image
            range: 范围匹配
            size (int, optional): 图片尺寸. Defaults to 640.
            gray: 是否匹配灰色元素
        Returns:
            map: 返回confidence最大的一个元素
        """
        if image is None:
            return {}
        # 进行目标检测
        results = self.model.forward(image, size)
        names = self.model.names
        best_map = {}
        conf = {}
        boxes = {}  # 用于存储每个元素的检测框

        for i, det in enumerate(results.pred[0]):
            # 将张量转换为值
            det = det.tolist()
            name = names[int(det[5])]
            confidence = det[4]

            # 获取检测框中心点位置
            center_x = (det[0] + det[2]) / 2
            center_y = (det[1] + det[3]) / 2
            if center_x < range[0] or center_y < range[1]:
                continue
            if center_x > range[2] or center_y > range[3]:
                continue    
            if not gray:  # 过滤灰色元素
                # 获取图像中心点像素颜色
                b, g, r = self.get_pixel_color(image, center_x, center_y)
                # 判断像素颜色是否为灰色
                if b == g == r and b != 255:
                    continue  # 如果颜色是灰色，则跳过当前元素，不存储到best_map中
            if name not in conf.keys() or confidence > conf[name]:
                conf[name] = confidence
                best_map[name] = [center_x, center_y]
                boxes[name] = [det[0], det[1], det[2], det[3]]  # 存储检测框

        # 删除重合度超过一半的元素,保留置信度高的元素
        to_remove = set()
        for name1, box1 in boxes.items():
            for name2, box2 in boxes.items():
                if name1 != name2 and self.calculate_iou(box1, box2) > 0.5:
                    # 如果两个检测框的 IoU 超过 0.5，全部舍弃，避免误操作
                    to_remove.add(name1)
                    to_remove.add(name2)

        for name in to_remove:
            best_map.pop(name, None)

        return best_map

    def calculate_iou(self, box1, box2):
        """计算两个检测框的 IoU（交并比）

        Args:
            box1 (list): 第一个检测框 [x1, y1, x2, y2]
            box2 (list): 第二个检测框 [x1, y1, x2, y2]

        Returns:
            float: IoU 值
        """
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])

        # 计算交集面积
        inter_area = max(0, x2 - x1) * max(0, y2 - y1)

        # 计算并集面积
        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
        union_area = box1_area + box2_area - inter_area

        # 避免除以零
        if union_area == 0:
            return 0

        return inter_area / union_area

    def get_pixel_color(self, image, x, y):
        """获取图像指定位置的像素颜色值

        Args:
            image (string/NumPy): 图像路径或图像数组
            x (float): x 坐标
            y (float): y 坐标

        Returns:
            tuple: 返回像素的 (B, G, R) 颜色值
        """
        # 如果输入是图像路径，则加载图像
        if isinstance(image, str):
            image = cv2.imread(image)

        # 将坐标转换为整数
        x = int(round(x))
        y = int(round(y))

        # 获取指定位置的像素颜色值
        pixel_color = image[y, x]

        # 返回像素的 (B, G, R) 颜色值
        return pixel_color[0], pixel_color[1], pixel_color[2]