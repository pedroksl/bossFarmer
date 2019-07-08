# Importation of the files required to run this code properly
import time
import threading
import pyautogui
from numpy.random import randint as r
from pynput import keyboard
from pynput.keyboard import Key, Listener, Controller
from imagesearch import *

# Definition of the keyboard commands that will control the application
keyEnableHotkeys = Key.f12
keyControl = keyboard.KeyCode(char='l')
keySkills = keyboard.KeyCode(char='k')
keyUlt = keyboard.KeyCode(char='u')
keyStop = keyboard.KeyCode(char='p')
keySwitchMode = keyboard.KeyCode(char='m')
keySummon = keyboard.KeyCode(char='b')
keyHeroSkillSelect = keyboard.KeyCode(char=',')
keyPartySkillSelect = keyboard.KeyCode(char='.')

# Definition of global variables used to define the behaviour of the application
hotkeysEnabled = True  # Enables the use of keyboard hotkeys to control app
enableSkills = True  # Enables de use of party skills, also used to turn auto skill on
enableUlt = True  # Enable the use of ultimate skills
controlledDamage = True  # Leaves fights early to reduce damage output
randomizedDamage = True  # Randomizes the timer to leave fight on controlled mode
summonBosses = False  # Allow boss summoning
run = True  # Variable used to start/stop running the code
fightMode = 0  # Switches between fight modes -> 0 = boss fight, 1 = use skills and ult on whatever you are doing
ptSkillSelected = 3  # Party skill selected to use
heroSkillSelected = 1  # Hero skill selected to use
timeout = 600  # Time to wait before reconnecting to the game after login from another device
unstuck = 300  # Time to wait before leaving a battle because the code is stuck
menuUnstuck = 30  # Time to wait in the menu before trying to unstuck
bossTimer = 70  # Time to wait before leaving a boss battle in controlled mode

# Path to the image files
accesoryReady = "Images/1_accessoryReady.bmp"
battleParticipate = "Images/2_battleParticipate.bmp"
battleReady = "Images/3_battleReady.bmp"
battleStart = "Images/4_battleStart.bmp"
partySkill = "Images/5_partySkill.bmp"
skillReady = "Images/6_skillReady.bmp"
battleExit = "Images/7_battleExit.bmp"
rewardCheck = "Images/8_rewardCheck.bmp"
rewardConfirm = "Images/9_rewardConfirm.bmp"
battleIcon = "Images/battleIcon.bmp"
closeEvent = "Images/closeEvent.bmp"
connectionNotice = "Images/connectionNotice.bmp"
equipFull = "Images/equipFull.bmp"
gameStart = "Images/gameStart.bmp"
homeIcon = "Images/homeIcon.bmp"
touchStart = "Images/touchStart.bmp"
xIcon = "Images/xIcon.bmp"
autoSkill = "Images/autoSkill.bmp"
bossCalculating = "Images/bossCalculating.bmp"
pauseBattle = "Images/pauseBattle.bmp"
endBattle = "Images/endBattle.bmp"
endBattleConfirm = "Images/endBattleConfirm.bmp"
ownBoss = "Images/ownBoss.bmp"
wendyCard = "Images/wendyCard.bmp"
gorgosCard = "Images/gorgosCard.bmp"
summonConfirm = "Images/summonConfirm.bmp"
doneSummoning = "Images/doneSummoning.bmp"
loginReward = "Images/loginReward.bmp"
equipToSell = "Images/equipToSell.bmp"
accessoryError = "Images/accessoryError.bmp"
bossDeadError = "Images/bossDeadError.bmp"


# Class used to listen to keyboard input and update the application
class keyboardInterrupt(threading.Thread):
    def run(self):
        def on_press(key):
            if key == keyEnableHotkeys:
                global hotkeysEnabled
                hotkeysEnabled = not hotkeysEnabled
                print("HotkeysEnabled is: %s" % hotkeysEnabled)
            if hotkeysEnabled:
                if key == keyControl:
                    global controlledDamage
                    controlledDamage = not controlledDamage
                    print("ControlledDamage is: %s" % controlledDamage)
                if key == keySkills:
                    global enableSkills
                    enableSkills = not enableSkills
                    print("enableSkills is: %s" % enableSkills)
                elif key == keyUlt:
                    global enableUlt
                    enableUlt = not enableUlt
                    print("enableUlt is: %s" % enableUlt)
                elif key == keySummon:
                    global summonBosses
                    summonBosses = not summonBosses
                    print("Summon Bosses is: %s" % summonBosses)
                elif key == keyStop:
                    global run
                    run = not run
                    print("run is: %s" % run)
                elif key == keyHeroSkillSelect:
                    global heroSkillSelected
                    heroSkillSelected += 1
                    if heroSkillSelected > 4:
                        heroSkillSelected = 1
                    print("Hero skill selected to use: %s" % heroSkillSelected)
                elif key == keyPartySkillSelect:
                    global ptSkillSelected
                    ptSkillSelected += 1
                    if ptSkillSelected > 3:
                        ptSkillSelected = 1
                    print("Party skill selected to use: %s" % ptSkillSelected)
                elif key == keySwitchMode:
                    global fightMode
                    fightMode += 1
                    if fightMode > 1:
                        fightMode = 0
                    print("fightMode is: %s" % fightMode)

        # listener = keyboard.Listener(on_press=on_press, on_release=0)
        #
        # while hotkeysEnabled:
        #     if not listener.isAlive():
        #         listener.start()

        with Listener(on_press=on_press, on_release=0) as listener:
            try:
                listener.join()
            except KeyError:
                print("Unexpected key pressed'.")
                self.run()


# Method that sells equipment
def sellEquips():
    time1 = time.perf_counter()
    click_random([1164, 40])  # Bag
    click_random([580, 116])  # Equip
    click_random([1170, 680])  # Sell
    click_random([780, 670])  # Auto Add
    if not searchForImageLoop(equipToSell, True, time1):  # Find item Rank to Sell
        return False  # return false if didn't find it
    click_random([650, 700])  # Close rank selection
    click_random([975, 680])  # Auto Add
    click_random([1165, 680])  # Sell
    time.sleep(0.2)
    click_random([650, 700])  # Close sucess notice
    time.sleep(0.2)
    click_random([1235, 40])  # Home Button
    time.sleep(0.2)
    click_random([1045, 630])  # Battle Start
    time.sleep(3)  # Wait for load
    click_random([198, 518])  # Dimensional Boss
    return True


# Method used to leave a fight in controlled damage mode
def exitBossFight():
    time1 = time.perf_counter()
    print("Let's get this battle over with!")
    if searchForImage(pauseBattle, True):
        if not searchForImageLoop(endBattle, True, time1):
            print("Didn't find the end battle button")
            return
        if not searchForImageLoop(endBattleConfirm, True, time1):
            print("Didn't find the end battle confirm button")
            return
    else:
        print("Didn't find the pause button")
        return


# Method used to use skills and ultimes if enabled
def fightWithSkillsAndUlt():
    if enableSkills:
        print("Skills are Enabled!")
        if searchForImage(autoSkill):
            image = screenshot()
            rgb = image.getpixel((1074 + hMargin, 35 + vMargin))
            if rgb[0] > 150:
                click_random([1074, 37])

        if searchForImage(partySkill):
            im = screenshot()
            rgb = im.getpixel((663 + hMargin, 678 + vMargin))
            if rgb[0] > 100:
                click_exact([663, 678])
                time.sleep(0.4)
                click_random([450 + 100 * ptSkillSelected, 520])

    if enableUlt:
        print("Ultimates are Enabled!")
        if searchForImageInArea(skillReady, 600, 670, 720, 720):
            hcoord = 40
            if heroSkillSelected is 2:
                hcoord = 320
            elif heroSkillSelected is 3:
                hcoord = 750
            elif heroSkillSelected is 4:
                hcoord = 1025
            click_random([hcoord, 655])
            time.sleep(0.3)
            click_random([640, 400])


# Method that controls the boss fight timer and check for possible crashes
def fightBoss():
    if searchForImage(accessoryError):
        return
    bossTimerReal = bossTimer
    time1 = time.perf_counter()
    if randomizedDamage:
        bossTimerReal = bossTimer + r(-10, 10)
    while not searchForImage(battleExit, True):
        print("Fight Boss!")
        if searchForImage(gameStart):
            return
        if searchForImage(connectionNotice):
            return
        if searchForImage(bossCalculating):
            return

        if controlledDamage and time.perf_counter() - time1 > bossTimerReal:
            print(controlledDamage)
            print("Time's over, fight's over!")
            exitBossFight()

        fightWithSkillsAndUlt()

        if time.perf_counter() - time1 > unstuck:
            break


# Method called to begin a fight, navigating through menus
def startBossFight(uncontrolled=False):
    if searchForImage(accessoryError):
        return False
    time1 = time.perf_counter()
    global controlledDamage
    saveControlledDamage = controlledDamage
    if uncontrolled:
        controlledDamage = False
    if not searchForImageLoop(battleReady, True, time1):
        return False
    if not searchForImageLoop(battleStart, True, time1):
        return False
    if (searchForImage(equipFull)):
        print("Oh, no, time to sell gear!")
        click_random([298, 518])
        time.sleep(1)
        if not sellEquips():
            return False
    elif searchForImage(bossDeadError):
        print("On, no, boss is already dead!")
        click_random([298, 518])
        return False
    else:
        time1 = time.perf_counter()
        fightBoss()
        controlledDamage = saveControlledDamage
    return True


# Method used to summon new bosses if there aren't any available
def summonSomething():
    time1 = time.perf_counter()
    pos = [-1, -1]
    if searchForImage(wendyCard):
        pos = imagesearch(wendyCard)
    if searchForImage(gorgosCard):
        pos2 = imagesearch(gorgosCard)
        if pos2[0] is not -1:
            if pos[0] is -1 or pos[1] > pos2[1]:
                pos = pos2
    if pos[0] is not -1:
        click_random(([pos[0] + 160, pos[1] + 30]))
        if not searchForImageLoop(summonConfirm, True, time1):
            return
        time.sleep(8)
        click_random([1200, 700])


# Method that monitors the boss window, starting fights, collecting reward, etc
def bossKillingLoop():
    time1 = time.perf_counter()
    while run:
        print("Boss Killing Loop!")
        if searchForImage(connectionNotice) or searchForImage(gameStart):
            print("Oops, connection error or crash!")
            return
        if searchForImage(accessoryError):
            click_random([298, 518])
        if searchForImage(accesoryReady):
            image = screenshot()
            rgb = image.getpixel((683 + hMargin, 628 + vMargin))
            if rgb[2] < 100:
                print("Accessory is ready!")
                click_exact([683, 628])
                time.sleep(1)
                click_random([298, 518])
        if searchForImage(rewardCheck, True):
            print("Getting reward!")
            time.sleep(2)
            click_random([298, 518])
            if not searchForImageLoop(rewardConfirm, True, time1):
                return
        if searchForImage(ownBoss):
            pos = imagesearch(ownBoss)
            if pos[0] is not -1:
                image = screenshot()
                rgb = image.getpixel((pos[0] + 650, pos[1] + 20))
                if rgb[0] > 200 and rgb[2] < 100:
                    print("Killing my own boss!")
                    click_random([pos[0] + 650, pos[1] + 20])
                    if not startBossFight(True):
                        return
                    time.sleep(1)
                    continue
        if searchForImage(battleParticipate, True):
            print("Found a new boss!")
            if not startBossFight():
                return
        elif summonBosses and not searchForImage(ownBoss) and searchForImage(doneSummoning):
            summonSomething()
        elif searchForImage(bossCalculating):
            return
        time.sleep(1)


# Method used to restart the game in case of a crash
def restartTheGame():
    print("Restart the Game!")
    if searchForImage(gameStart):
        click_random([1050, 225])
        if not searchForImageLoop(touchStart, True):
            print("Couldn't find the touch to start button. :(")
            return False
        if not searchForImageLoop(closeEvent, True):
            print("Couldn't close the event notice. :(")
            return False
        return True
    return False


# Method used to find the boss screen no matter what window of the game you are
def findBossScreen():
    print("Find Boss Screen!")
    if searchForImage(connectionNotice, True):
        print("Someone logged in, let's wait for some time out.")
        time.sleep(timeout)
    if searchForImage(accessoryError):
        click_random([298, 518])
    if searchForImage(gameStart):
        print("Did we crash?")
        if not restartTheGame():
            return
    if searchForImage(touchStart, True):
        print("Failed to click on Touch to Start during restart.")
    if searchForImage(closeEvent, True):
        print("Failed to click on Close Event during restart.")
    while searchForImage(xIcon, True):
        time.sleep(1)
    while searchForImage(homeIcon, True):
        time.sleep(1)

    if searchForImage(loginReward):
        click_random([298, 518])

    if searchForImage(battleIcon, True):
        print("Time to search for some fights!")
        time.sleep(3)
        click_random([198, 518])
        time.sleep(2)
        bossKillingLoop()


# Main method, containing main loop
def main():
    setWindowMargins()
    keybThread = keyboardInterrupt(name="Interrupts thread")
    keybThread.start()
    while True:
        try:
            while True:
                if run:
                    if fightMode == 0:
                        findBossScreen()
                    elif fightMode == 1:
                        fightWithSkillsAndUlt()
        except KeyboardInterrupt:
            exit()


main()
