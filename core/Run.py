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
        while True:
            try:
                while True:
                    if self.cc.configs.run:
                        if self.cc.configs.fightMode == 0:
                            self.gc.findBossScreen()
                        elif self.cc.configs.fightMode == 1:
                            self.gc.fightWithSkillsAndUlt()
                    else:
                        time.sleep(2)
            except KeyboardInterrupt:
                exit()
