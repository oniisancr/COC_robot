# 数据标注说明

- `labelImg.exe` 用于标注的工具，预定义文本的顺序不可修改。但可以新增。
- **`data.yaml` 文件内的`Classes name` 必须与`predefined_classes.txt`  顺序一致**

- 请按照下列名字，增加标注。可扩充修改。尽量使用拼音标注元素。

    ```python
    # 兵种与法术
    self.troops_name = ["fashi","gebulin","yemanren","juren","qiqiu","gongjianshou","leilong","longbao","zhadanren",
                        "xueguai","kuanggong","tianshi","feilong","longqishi","pika","kuanggong","wangling","nvwu","longqishi","toushou","liequan"]
    self.spells_name = ["shandian","bingdong","kuangbao","zhiliao","tantiao","tiepi","shanghai","bianfu","yinxing"]
    self.gc_name = ["gczhanche","gcqiqiu"]
    ```

- 具体操作教程
  - 将新图片元素放入`dataset\images`。请统一分辨率为 `1080 * 2400`, dpi `440`。
  - 打开`labelImg.exe`
  - open dir 选择 `dataset\images`, save dir 选择 `dataset\labels`
  - 点击 create 继续画框标注

- 可使用tools路径下 `getdata.py` 抓取新截图。截图会自动放入`dataset\images`

- **标记完的数据，可直接回传至本仓库。以便他人训练优化模型。**
