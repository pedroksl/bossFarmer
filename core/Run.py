import threading
import time
from controllers import ConfigurationController
from controllers import GameController
from core import ImageImports

class Run(threading.Thread):
    def __init__(self, ConCon, GameCon):
        self.cc = ConCon
        self.gc = GameCon
        threading.Thread.__init__(self)

    def run(self):
        self.gc.setWindowMargins()
        while self.cc.configs.run:
            if self.cc.configs.fightMode == 0:
                self.gc.findBossScreen()
                time.sleep(2)
            elif self.cc.configs.fightMode == 1:
                self.gc.fightWithSkillsAndUlt()
                time.sleep(1)
            elif self.cc.configs.fightMode == 2:
                self.gc.findTrialTowerScreen()
                time.sleep(2)
            elif self.cc.configs.fightMode == 4:
                self.gc.findMissionScreen()
                time.sleep(2)
            elif self.cc.configs.fightMode == 5:
                self.gc.testMode()
                time.sleep(1)
