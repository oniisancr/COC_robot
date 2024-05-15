import torch
import cv2
from util.positon import screensz

class YoloCOC:
    def __init__(self, model_path='best.pt'):
        # 加载模型
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', model_path)  # custom/local model
        self.model.eval()  # 设置为评估模式

    def detect(self, image, range=screensz, size=1280, gray=True):
        """识别所有非灰色元素

        Args:
            image (string/NumPy): image path or image
            range: 范围匹配
            size (int, optional): 图片尺寸. Defaults to 1280.
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
            if not gray: #过滤灰色元素
                # 获取图像中心点像素颜色
                b, g, r = self.get_pixel_color(image, center_x, center_y)
                # 判断像素颜色是否为灰色
                if b == g == r and b != 255:
                    continue  # 如果颜色是灰色，则跳过当前元素，不存储到best_map中
                elif name not in conf.keys() or confidence > conf[name]:
                    conf[name] = confidence
                    best_map[name] = [center_x, center_y]
            else:
                if name not in conf.keys() or confidence > conf[name]:
                    conf[name] = confidence
                    best_map[name] = [center_x, center_y]
        return best_map
    
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