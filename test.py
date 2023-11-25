import time

def update_console_data():
    for i in range(10):
        # 模拟更新的数据
        data_to_display = f"数据更新: {i}"

        # 使用 ANSI 转义码将光标移动到行首
        print(f"\r{data_to_display.ljust(80)}", end="", flush=True)

        # 等待1秒
        time.sleep(1)
# 运行更新函数
update_console_data()
