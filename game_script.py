# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30  19:21:36 2023

@author: Rui
"""
from transitions import Machine
from adb import adb_command
from game_controller import GameController
import time
import config
import logging
# 配置日志记录到文件
logging.basicConfig(filename='coc_robot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filemode='w')

offline_timer = 0
wait_wakeup_timer = 0

class GameScript:
    states = ['initializing', 'waiting', 'processing', 'finishing']
    waitting_time = 0
    
    last_yyz = 0
    last_gain = 0
    last_donate = 0
    
    def __init__(self):
        self.machine = Machine(model=self, states=GameScript.states, initial='initializing')
        self.game_controller = GameController()

        self.machine.add_transition('initializing2waiting', 'initializing', 'waiting')
        self.machine.add_transition("waiting2initializing", 'waiting', 'initializing')
        self.machine.add_transition('start_processing', 'waiting', 'processing')
        self.machine.add_transition('finish', 'processing', 'finishing')
        self.machine.add_transition('start_init', 'waiting', 'initializing')
        self.machine.add_transition('processing2waiting','processing','waiting')

      
    def init(self):
        global offline_timer
        offline_timer = config.MAX_ONLINE_TIME

        # 转到等待状态
        self.waitting_time = 5
        self.initializing2waiting()
    
    def keep_clear_home(self):
        '''
        关闭主界面其余窗口，避免因误触界面其他按钮导致脚本暂停
        '''
        # 只使用一张截图判断
        game_script.game_controller.take_screenshot(True)
        game_script.game_controller.shot_new = False
        
        # 关闭大窗口window  -（误触add、商店、布局、）
        if game_script.game_controller.click_by_name("close_window", False):
            return
        # 关闭中窗口window  -（误触邮件、进攻、设置）
        if game_script.game_controller.click_by_name("close_medium_window", False):
            return
        # 关闭批量升级window
        if game_script.game_controller.click_by_name("close_update_window", False):
            return
        # 误触建筑物
        if game_script.game_controller._match_template(["target_info"]):
            # 点击草坪
            game_script.game_controller.click_by_name("grass",False)
        # 关闭超级兵界面
        if game_script.game_controller.click_by_name("close_supertroop_window", False):
            return
        # 关闭每周精选close_weekly_window
        if game_script.game_controller.click_by_name("close_weekly_window", False):
            return
        
        game_script.game_controller.shot_new = True
    
    def execute_game_action(self):
        self.keep_clear_home()

        if int(time.time()) - self.last_gain > config.gain_interval:
            self.last_gain = int(time.time())
            if config.CLICK_LOG:
                logging.info("gain_base")
            self.game_controller.gain_base()

        if config.yyzhan and int(time.time()) - self.last_yyz > config.yyzhan_Interval: #控制频率
            self.last_yyz = int(time.time())
            if config.CLICK_LOG:
                logging.info('start yyzhan')
            self.game_controller.yyzhan()
        
        if config.donate_troops and int(time.time()) - self.last_donate > config.donate_Interval:
            if config.CLICK_LOG:
                logging.info('start donate_troops')
            self.game_controller.donate_troops()
            self.last_donate = time.time()
        self.game_controller.train()

if __name__ == "__main__":
    game_script = GameScript()
    while game_script.state != 'finishing':
        if game_script.state == 'initializing':
            time.sleep(1)
            # 回到主界面
            adb_command("shell input keyevent 3")
            time.sleep(1)
            # 启动游戏--腾讯
            adb_command("shell am start -n com.tencent.tmgp.supercell.clashofclans/com.supercell.titan.tencent.GameAppTencent")
            time.sleep(10)
            game_script.init()
        elif game_script.state == 'waiting':
            if wait_wakeup_timer > 0:
                time.sleep(10)
                wait_wakeup_timer -= 10
                if wait_wakeup_timer == 0:
                    game_script.waiting2initializing()
                continue
            # 系统维护 等待5分钟重试
            if game_script.game_controller._match_template(["reload_maintenance"]):
                wait_wakeup_timer = 300
                # 退出
                adb_command("shell am force-stop com.tencent.tmgp.supercell.clashofclans")
                continue
            # 更新错误
            if game_script.game_controller._match_template(["update_error"],confidence=0.965):
                game_script.game_controller.click_by_name("exit") #退出
                wait_wakeup_timer = 10
                continue
            # 被攻击中
            if game_script.game_controller._match_template(["onatttacked"]):
                time.sleep(1)
                continue
            # 被攻击中-->回营
            game_script.game_controller.click_by_name("back_home")
            # 关闭活动界面
            game_script.game_controller.click_by_name("close_window")
            # 关闭月度大活动结算、升级完成
            game_script.game_controller.click_by_name("confirm")
            # 突袭奖励
            game_script.game_controller.click_by_name("close_tuxi_window")
            # 长时间未操作
            game_script.game_controller.click_by_name("reload")
            # 是否已经进入主界面
            if not game_script.game_controller._match_template(["add"]):
                time.sleep(1)
                continue
            
            if game_script.waitting_time <= 0:
                game_script.start_processing()
            else:
                game_script.waitting_time -= 5
                time.sleep(5)

        elif game_script.state == 'processing':            
            if offline_timer > 0:
                time.sleep(1)
                offline_timer -= 1
                if offline_timer == 0:
                    # 退出
                    adb_command("shell am force-stop com.tencent.tmgp.supercell.clashofclans")
                    wait_wakeup_timer = config.WAKEUP_TIME
                    offline_timer = config.MAX_ONLINE_TIME
                    game_script.processing2waiting()
            game_script.execute_game_action()
            #game_script.finish()