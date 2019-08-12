from core import ImageImports
from core import ImageSearcher
import time
from numpy.random import randint as r

class GameController():
    def __init__(self, ConCon):
        self.cc = ConCon
        self.imgSearcher = ImageSearcher(self.cc)
        self.imgImp = ImageImports()
        if self.cc.configs.windowName is "NoxPlayer":
            self.imgImp.gameStart = self.imgImp.gameStartNox
        if self.cc.configs.windowName is "LDPlayer":
            self.imgImp.gameStart = self.imgImp.gameStartLd

    def setWindowMargins(self):
        self.imgSearcher.setWindowMargins()

    # Method that sells equipment
    def sellEquips(self):
        time1 = time.perf_counter()
        self.imgSearcher.click_random([1164, 40])  # Bag
        self.imgSearcher.click_random([580, 116])  # Equip
        self.imgSearcher.click_random([1170, 680])  # Sell
        self.imgSearcher.click_random([780, 670])  # Auto Add
        if not self.imgSearcher.searchForImageLoop(self.imgImp.equipToSell, True, time1):  # Find item Rank to Sell
            return False  # return false if didn't find it
        self.imgSearcher.click_random([650, 700])  # Close rank selection
        self.imgSearcher.click_random([975, 680])  # Auto Add
        self.imgSearcher.click_random([1165, 680])  # Sell
        time.sleep(0.2)
        self.imgSearcher.click_random([650, 700])  # Close sucess notice
        time.sleep(0.2)
        self.imgSearcher.click_random([1235, 40])  # Home Button
        time.sleep(0.2)
        self.imgSearcher.click_random([1045, 630])  # Battle Start
        time.sleep(3)  # Wait for load
        self.imgSearcher.click_random([198, 518])  # Dimensional Boss
        return True


    # Method used to leave a fight in controlled damage mode
    def exitBossFight(self):
        time1 = time.perf_counter()
        print("Let's get this battle over with!")
        if self.imgSearcher.searchForImage(self.imgImp.pauseBattle, True):
            if not self.imgSearcher.searchForImageLoop(self.imgImp.endBattle, True, time1):
                print("Didn't find the end battle button")
                return
            if not self.imgSearcher.searchForImageLoop(self.imgImp.endBattleConfirm, True, time1):
                print("Didn't find the end battle confirm button")
                return
        else:
            print("Didn't find the pause button")
            return


    # Method used to use skills and ultimes if enabled
    def fightWithSkillsAndUlt(self):
        if self.cc.configs.enableSkills:
            print("Skills are Enabled!")
            im = self.imgSearcher.screenshot()
            if self.imgSearcher.searchForImage(self.imgImp.autoSkill):
                x = 1074 if not self.cc.configs.pixelOffset else 1071
                rgb = self.imgSearcher.getPixel(x, 35, image=im)
                if rgb[0] > 150:
                    self.imgSearcher.click_exact([x, 35])

                x = 663 if not self.cc.configs.pixelOffset else 660
                rgb = self.imgSearcher.getPixel(x, 678, image=im)
                if rgb[0] > 100 and rgb[2] < 20:
                    self.imgSearcher.click_exact([x, 678])
                    time.sleep(0.4)
                    self.imgSearcher.click_random([450 + 100 * self.cc.configs.ptSkillSelected, 520])

        if self.cc.configs.enableUlt:
            print("Ultimates are Enabled!")
            if self.imgSearcher.searchForImageInArea(self.imgImp.skillReady, 600, 670, 720, 720):
                hcoord = 40
                if self.cc.configs.heroSkillSelected is 2:
                    hcoord = 320
                elif self.cc.configs.heroSkillSelected is 3:
                    hcoord = 750
                elif self.cc.configs.heroSkillSelected is 4:
                    hcoord = 1025
                self.imgSearcher.click_random([hcoord, 655])
                time.sleep(0.3)
                self.imgSearcher.click_random([640, 400])


    # Method that controls the boss fight timer and check for possible crashes
    def fightBoss(self, uncontrolled=False):
        if self.imgSearcher.searchForImage(self.imgImp.accessoryError):
            return False
        bossTimerReal = self.cc.configs.bossTimer
        time1 = time.perf_counter()
        if self.cc.configs.randomizedDamage:
            bossTimerReal = self.cc.configs.bossTimer + r(-10, 10)
        while not self.imgSearcher.searchForImage(self.imgImp.battleExit, True):
            print("Fight Boss!")
            if self.imgSearcher.searchForImage(self.imgImp.gameStart):
                return False
            if self.imgSearcher.searchForImage(self.imgImp.connectionNotice):
                return False
            if self.imgSearcher.searchForImage(self.imgImp.bossCalculating):
                return False
            if self.imgSearcher.searchForImage(self.imgImp.noticeMessage):
                self.imgSearcher.click_random([298, 518])
            if self.cc.configs.run and self.imgSearcher.searchForImage(self.imgImp.pauseWindow):
                self.imgSearcher.click_random([298, 518])

            if (self.cc.configs.controlledDamage and not uncontrolled) and time.perf_counter() - time1 > bossTimerReal:
                print("Time's over, fight's over!")
                self.exitBossFight()
                return True

            self.fightWithSkillsAndUlt()

            if time.perf_counter() - time1 > self.cc.configs.unstuck:
                self.imgSearcher.click_random([298, 518])
                print("Oops, took too long to finish the boss, might be stuck!")
                return False
        return True


    # Method called to begin a fight, navigating through menus
    def startBossFight(self, increaseDelay=False, uncontrolled=False):
        if self.imgSearcher.searchForImage(self.imgImp.accessoryError):
            return False
        time1 = time.perf_counter()
        if not self.imgSearcher.searchForImageLoop(self.imgImp.battleReady, True, time1):
            return False
        if increaseDelay:
            randomTime = 10 + r(5, 10)
            time.sleep(randomTime)
        if not self.imgSearcher.searchForImageLoop(self.imgImp.battleStart, True, time1):
            return False
        time1 = time.perf_counter()
        print("Waiting for battle to load")
        while not self.imgSearcher.searchForImage(self.imgImp.pauseBattle):
            if self.imgSearcher.searchForImage(self.imgImp.gameStart) or time.perf_counter() - time1 > self.cc.configs.refreshBossScreen:
                return False
            if self.imgSearcher.searchForImage(self.imgImp.equipFull):
                print("Oh, no, time to sell gear!")
                self.imgSearcher.click_random([298, 518])
                time.sleep(1)
                if not self.sellEquips():
                    return False
                return True
            elif self.imgSearcher.searchForImage(self.imgImp.bossDeadError):
                print("On, no, boss is already dead!")
                self.imgSearcher.click_random([298, 518])
                return False

        result = self.fightBoss(uncontrolled)
        return result


    # Method used to summon new bosses if there aren't any available
    def summonSomething(self):
        time1 = time.perf_counter()
        pos = [-1, -1]
        if self.imgSearcher.searchForImage(self.imgImp.wendyCard, precision=0.9):
            pos = self.imgSearcher.imagesearch(self.imgImp.wendyCard, precision=0.9)
        if self.imgSearcher.searchForImage(self.imgImp.gorgosCard, precision=0.9):
            pos2 = self.imgSearcher.imagesearch(self.imgImp.gorgosCard, precision=0.9)
            if pos2[0] is not -1:
                if pos[0] is -1 or pos[1] > pos2[1]:
                    pos = pos2
#        if pos[0] is -1 and not self.imgSearcher.searchForImage(self.imgImp.acquireBoss):
#            self.imgSearcher.click_scroll([1000, 500], "up", 300)
#            time.sleep(1)
#            self.summonSomething()
        if pos[0] is not -1:
            self.imgSearcher.click_random([pos[0] + 160, pos[1] + 30])
            self.imgSearcher.searchForImageLoop(self.imgImp.summonConfirm, True, time1)
            return True
        return False


    # Method that monitors the boss window, starting fights, collecting reward, etc
    def bossKillingLoop(self):
        time1 = time.perf_counter()
        bossNotFound = False
        #self.summonSomething()
        while self.cc.configs.run:
            print("Boss Killing Loop!")
            if self.imgSearcher.searchForImage(self.imgImp.connectionNotice) or self.imgSearcher.searchForImage(self.imgImp.gameStart):
                print("Oops, connection error or crash!")
                return
            if self.imgSearcher.searchForImage(self.imgImp.noticeMessage) or self.imgSearcher.searchForImage(self.imgImp.questClear):
                self.imgSearcher.click_random([298, 518])
            self.imgSearcher.searchForImage(self.imgImp.battleExit, True)
            if self.imgSearcher.searchForImage(self.imgImp.accessoryError) or self.imgSearcher.searchForImage(self.imgImp.accessoryLagError):
                self.imgSearcher. click_random([298, 518])
            if self.imgSearcher.searchForImage(self.imgImp.accesoryReady):
                rgb = self.imgSearcher.getPixel(683, 628)
                if rgb[2] < 100:
                    print("Accessory is ready!")
                    self.imgSearcher.click_exact([683, 628])
                    time.sleep(1)
                    self.imgSearcher.click_random([298, 518])
                    continue
            if self.imgSearcher.searchForImage(self.imgImp.rewardCheck, True):
                print("Getting reward!")
                if not self.imgSearcher.searchForImageLoop(self.imgImp.rewardAcquired, True, time1):
                    return
                if not self.imgSearcher.searchForImageLoop(self.imgImp.rewardConfirm, True, time1):
                    return
            if self.imgSearcher.searchForImage(self.imgImp.ownBoss):
                pos = self.imgSearcher.imagesearch(self.imgImp.ownBoss)
                if pos[0] is not -1:
                    rgb = self.imgSearcher.getPixel(pos[0] + 650, pos[1] + 20, True)
                    if rgb[0] > 200 and rgb[2] < 100:
                        print("Killing my own boss!")
                        self.imgSearcher.click_random([pos[0] + 650, pos[1] + 20])
                        if not self.startBossFight(False, True):
                            return
                        time.sleep(1)
                        bossNotFound = False
                        time1 = time.perf_counter()
                        continue
            if self.imgSearcher.searchForImage(self.imgImp.battleParticipate, True):
                print("Found a new boss!")
                if not self.startBossFight(bossNotFound):
                    return
                bossNotFound = False
                time1 = time.perf_counter()
            elif self.cc.configs.summonBosses and not self.imgSearcher.searchForImage(self.imgImp.ownBoss) and self.imgSearcher.searchForImage(self.imgImp.doneSummoning, precision=0.95):
                bossNotFound = not self.summonSomething()
            elif self.imgSearcher.searchForImage(self.imgImp.bossCalculating):
                self.imgSearcher.searchForImage(self.imgImp.homeIcon, True)
                return
            else:
                bossNotFound = True
            time.sleep(3)
            if time.perf_counter() - time1 > self.cc.configs.refreshBossScreen:
                self.imgSearcher.searchForImage(self.imgImp.homeIcon, True)
                return
        print("Run is off, stopping farm.")


    # Method used to restart the game in case of a crash
    def restartTheGame(self):
        print("Restart the Game!")
        time1 = time.perf_counter()
        pos = self.imgSearcher.imagesearch(self.imgImp.gameStart)
        if pos[0] is not -1:
            # self.imgSearcher.click_random([1050, 225])
            self.imgSearcher.click_image_middle(self.imgImp.gameStart, pos)
            if not self.imgSearcher.searchForImageLoop(self.imgImp.touchStart, True, time1):
                print("Couldn't find the touch to start button. :(")
                return False
            time1 = time.perf_counter()
            if not self.imgSearcher.searchForImageLoop(self.imgImp.closeEvent, True, time1):
                print("Couldn't close the event notice. :(")
                return False
            return True
        return False


    def findHomeScreen(self):
        if self.imgSearcher.searchForImage(self.imgImp.connectionNotice, True):
            print("Someone logged in, let's wait for some time out.")
            time.sleep(self.cc.configs.timeout)
        if self.imgSearcher.searchForImage(self.imgImp.noticeMessage) or self.imgSearcher.searchForImage(self.imgImp.questClear):
            self.imgSearcher.click_random([298, 518])
        if self.imgSearcher.searchForImage(self.imgImp.accessoryError):
            self.imgSearcher.click_random([298, 518])
        if self.imgSearcher.searchForImage(self.imgImp.touchStart, True):
            print("Failed to click on Touch to Start during restart.")
        if self.imgSearcher.searchForImage(self.imgImp.closeEvent, True):
            print("Failed to click on Close Event during restart.")
        if self.imgSearcher.searchForImage(self.imgImp.gameStart):
            print("Did we crash?")
            if not self.restartTheGame():
                return
        while self.imgSearcher.searchForImage(self.imgImp.xIcon, True):
            time.sleep(1)
        while self.imgSearcher.searchForImage(self.imgImp.homeIcon, True):
            time.sleep(1)

        if self.imgSearcher.searchForImage(self.imgImp.loginReward):
            self.imgSearcher.click_random([298, 518])


    # Method used to find the boss screen no matter what window of the game you are
    def findBossScreen(self):
        if self.imgSearcher.searchForImage(self.imgImp.dbossScreen):
            self.bossKillingLoop()
        else:
            print("Find Boss Screen!")
            self.findHomeScreen()
#            if self.imgSearcher.searchForImage(self.imgImp.noxClose, True):
#                time.sleep(1)
#                im = self.imgSearcher.screenshot(windowName="Reminder")
#                im.save("Test.png")
#                self.imgSearcher.click_random([824, 400], windowName="Reminder")

            if self.imgSearcher.searchForImage(self.imgImp.battleIcon, True):
                print("Time to search for some fights!")
                while not self.imgSearcher.searchForImage(self.imgImp.dbossButton, True):
                    self.imgSearcher.searchForImage(self.imgImp.dailyButton, True)
                time.sleep(2)
                self.bossKillingLoop()
            else:
                self.imgSearcher.click_random([298, 518])


    def fightTowerLevel(self):
        time1 = time.perf_counter()
        while not self.imgSearcher.searchForImage(self.imgImp.battleExit, True):
            print("Fight!")
            if self.imgSearcher.searchForImage(self.imgImp.gameStart):
                return False
            if self.imgSearcher.searchForImage(self.imgImp.connectionNotice):
                return False
            if self.imgSearcher.searchForImage(self.imgImp.noticeMessage) or self.imgSearcher.searchForImage(self.imgImp.questClear):
                self.imgSearcher.click_random([298, 518])
            if self.cc.configs.run and self.imgSearcher.searchForImage(self.imgImp.pauseWindow):
                self.imgSearcher.click_random([298, 518])

            self.fightWithSkillsAndUlt()

            if time.perf_counter() - time1 > self.cc.configs.towerStuck:
                self.imgSearcher.click_random([298, 518])
                print("Oops, took too long to finish the boss, might be stuck!")
                return False
        return True


    def trialFarmingLoop(self):
        time1 = time.perf_counter()
        while self.cc.configs.run:
            print("Trial Tower Farming Loop!")
            if self.imgSearcher.searchForImage(self.imgImp.connectionNotice) or self.imgSearcher.searchForImage(self.imgImp.gameStart):
                print("Oops, connection error or crash!")
                return
            if self.imgSearcher.searchForImage(self.imgImp.noticeMessage) or self.imgSearcher.searchForImage(self.imgImp.questClear):
                self.imgSearcher.click_random([298, 518])
            self.imgSearcher.searchForImage(self.imgImp.battleExit, True)
            if self.imgSearcher.searchForImage(self.imgImp.battleReady, True):
                if not self.imgSearcher.searchForImageLoop(self.imgImp.battleStart, True):
                    return False
                print("Waiting for battle to load")
                while not self.imgSearcher.searchForImage(self.imgImp.pauseBattle):
                    time.sleep(1)
                if not self.fightTowerLevel():
                    return False
            time.sleep(1)
        print("Run is off, stopping farm.")
        return True


    def findTrialTowerScreen(self):
        print("Find Trial Tower Screen!")
        self.findHomeScreen()

        if self.imgSearcher.searchForImage(self.imgImp.battleIcon, True):
            print("Time to clear that tower!")
            while not self.imgSearcher.searchForImage(self.imgImp.ttowerButton, True):
                self.imgSearcher.searchForImage(self.imgImp.challengeButton, True)
            time.sleep(2)
            if self.trialFarmingLoop():
                return True


    def clickRandomCard(self):
        firstCard = [200, 350]
        secondCard = [500, 350]
        thirdCard = [800, 350]
        fourthCard = [100, 350]
        randomNumber = r(1,4)
        if randomNumber is 1:
            self.imgSearcher.click_exact(firstCard)
        elif randomNumber is 2:
            self.imgSearcher.click_exact(secondCard)
        elif randomNumber is 3:
            self.imgSearcher.click_exact(thirdCard)
        elif randomNumber is 4:
            self.imgSearcher.click_exact(fourthCard)
        time.sleep(5)
        return

    def missionFarmLoop(self):
        time1 = time.perf_counter()
        while self.cc.configs.run:
            print("Mission farming loop!")
            if self.imgSearcher.searchForImage(self.imgImp.cardSelection):
                self.clickRandomCard()
            if self.imgSearcher.searchForImage(self.imgImp.playAgain):
                rgb = self.imgSearcher.getPixel(970, 640)
                if rgb[2] < 150:
                    print("Energy is over.")
                    return False
                self.imgSearcher.searchForImage(self.imgImp.playAgain, True)
                time1 = time.perf_counter()
                time.sleep(1)
            if self.imgSearcher.searchForImage(self.imgImp.cardSelection):
                self.clickRandomCard()
            if self.imgSearcher.searchForImage(self.imgImp.gameStart):
                return False
            if self.imgSearcher.searchForImage(self.imgImp.connectionNotice):
                return False
            if self.imgSearcher.searchForImage(self.imgImp.noticeMessage) or self.imgSearcher.searchForImage(self.imgImp.questClear):
                self.imgSearcher.click_random([298, 518])
            if self.cc.configs.run and self.imgSearcher.searchForImage(self.imgImp.pauseWindow):
                self.imgSearcher.click_random([298, 518])

            self.fightWithSkillsAndUlt()

            if time.perf_counter() - time1 > self.cc.configs.towerStuck:
                self.imgSearcher.click_random([298, 518])
                print("Oops, took too long to finish the mission, might be stuck!")
                return False
        print("Run is off, stopping farm.")
        return True


    def findMissionScreen(self):
        print("Find Mission Screen!")
        self.findHomeScreen()

        if self.imgSearcher.searchForImage(self.imgImp.adventureIcon, True):
            print("Time to fight some monsters!")
            time1 = time.perf_counter()
            self.imgSearcher.searchForImageLoop(self.imgImp.mission17, True, time1)
            time.sleep(1)
            self.imgSearcher.click_exact([45, 400]) # 45 for 3, 525 for 6 and 1100 for 9
            time.sleep(1)
            if not self.imgSearcher.searchForImageLoop(self.imgImp.battleReady, True, time1):
                return
            if not self.imgSearcher.searchForImageLoop(self.imgImp.missonStart, True, time1):
                return
            self.missionFarmLoop()

    def testMode(self):
        self.imgSearcher.click_exact([1025, 41])
        self.imgSearcher.enumChilds()
