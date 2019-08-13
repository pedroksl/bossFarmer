from PySide2.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PySide2 import QtCore, QtGui
from gui.ui_mainwindow import Ui_MainWindow
from controllers import ConfigurationController
from controllers import GameController
from core import ImageImports
from core import Run

threads = []

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cc = ConfigurationController(self)
        self.gc = GameController(self.cc, self.updateTable)
        self.createConnections()
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header = self.ui.tableWidget.verticalHeader();
        header.setSectionResizeMode(QHeaderView.Stretch);
        self.imgImp = ImageImports()
        self.ui.logoLabel.setPixmap(QtGui.QPixmap(self.imgImp.logo).scaledToHeight(200))
        self.updateTable()


    def createConnections(self):
        self.ui.fightModeAButton.pressed.connect(self.setFightModeA)
        self.ui.fightModeBButton.pressed.connect(self.setFightModeB)
        self.ui.fightModeCButton.pressed.connect(self.setFightModeC)
        self.ui.fightModeDButton.pressed.connect(self.setFightModeD)
        self.ui.fightModeEButton.pressed.connect(self.setFightModeE)
        self.ui.fightModeFButton.pressed.connect(self.setFightModeF)

        self.ui.toggleControlledDamageButton.pressed.connect(self.toggleControlledDamage)
        self.ui.toggleSkillsButton.pressed.connect(self.toggleSkills)
        self.ui.changePartySkillButton.pressed.connect(self.changeSkills)
        self.ui.toggleUltButton.pressed.connect(self.toggleUlt)
        self.ui.changeHeroSkillButton.pressed.connect(self.changeUlt)
        self.ui.toggleSummonsButton.pressed.connect(self.toggleSummons)

        self.ui.toggleRunButton.pressed.connect(self.toggleRun)


    def toggleRun(self):
        if all(not thread.isAlive() for thread in threads):
            t = Run(ConCon=self.cc, GameCon=self.gc)
            t.setDaemon(True)
            threads.append(t)
            t.start()
        self.cc.toggleRun()
        self.updateTable()

    def setFightModeA(self):
        self.cc.setFightModeA()
        self.updateTable()

    def setFightModeB(self):
        self.cc.setFightModeB()
        self.updateTable()

    def setFightModeC(self):
        self.cc.setFightModeC()
        self.updateTable()

    def setFightModeD(self):
        self.cc.setFightModeD()
        self.updateTable()

    def setFightModeE(self):
        self.cc.setFightModeE()
        self.updateTable()

    def setFightModeF(self):
        self.cc.setFightModeF()
        self.updateTable()

    def toggleControlledDamage(self):
        self.cc.toggleControlledDamage()
        self.updateTable()

    def toggleSkills(self):
        self.cc.toggleSkills()
        self.updateTable()

    def toggleUlt(self):
        self.cc.toggleUlt()
        self.updateTable()

    def toggleSummons(self):
        self.cc.toggleSummons()
        self.updateTable()

    def changeSkills(self):
        self.cc.changeSkills()
        self.updateTable()

    def changeUlt(self):
        self.cc.changeUlt()
        self.updateTable()

    def updateTable(self):
        self.ui.tableWidget.setItem(0,0, QTableWidgetItem("Enable Skills"))
        self.ui.tableWidget.setItem(0,1, QTableWidgetItem(str(self.cc.configs.enableSkills)))
        self.ui.tableWidget.setItem(0,2, QTableWidgetItem("Party Skill Selected"))
        self.ui.tableWidget.setItem(0,3, QTableWidgetItem(str(self.cc.configs.ptSkillSelected)))
        self.ui.tableWidget.setItem(0,4, QTableWidgetItem("Enable Ult"))
        self.ui.tableWidget.setItem(0,5, QTableWidgetItem(str(self.cc.configs.enableUlt)))
        self.ui.tableWidget.setItem(0,6, QTableWidgetItem("Hero Skill Selected"))
        self.ui.tableWidget.setItem(0,7, QTableWidgetItem(str(self.cc.configs.heroSkillSelected)))
        self.ui.tableWidget.setItem(1,0, QTableWidgetItem("Controlled Damage"))
        self.ui.tableWidget.setItem(1,1, QTableWidgetItem(str(self.cc.configs.controlledDamage)))
        self.ui.tableWidget.setItem(1,2, QTableWidgetItem("Summon Bosses"))
        self.ui.tableWidget.setItem(1,3, QTableWidgetItem(str(self.cc.configs.summonBosses)))
        self.ui.tableWidget.setItem(1,4, QTableWidgetItem("Run Status"))
        self.ui.tableWidget.setItem(1,5, QTableWidgetItem(str(self.cc.configs.run)))
        self.ui.tableWidget.setItem(1,6, QTableWidgetItem("Boss Kills"))
        self.ui.tableWidget.setItem(1,7, QTableWidgetItem(str(self.gc.stats.killCount)))
        self.ui.tableWidget.setItem(2,0, QTableWidgetItem("Cell (2,0)"))
        self.ui.tableWidget.setItem(2,1, QTableWidgetItem("Cell (2,1)"))
        self.ui.tableWidget.setItem(2,2, QTableWidgetItem("Cell (2,2)"))
        self.ui.tableWidget.setItem(2,3, QTableWidgetItem("Cell (2,3)"))
        self.ui.tableWidget.setItem(2,4, QTableWidgetItem("Cell (2,4)"))
        self.ui.tableWidget.setItem(2,5, QTableWidgetItem("Cell (2,5)"))
        self.ui.tableWidget.setItem(2,6, QTableWidgetItem("Cell (2,6)"))
        self.ui.tableWidget.setItem(2,7, QTableWidgetItem("Cell (2,7)"))
        self.ui.tableWidget.setItem(3,0, QTableWidgetItem("Cell (3,0)"))
        self.ui.tableWidget.setItem(3,1, QTableWidgetItem("Cell (3,1)"))
        self.ui.tableWidget.setItem(3,2, QTableWidgetItem("Cell (3,2)"))
        self.ui.tableWidget.setItem(3,3, QTableWidgetItem("Cell (3,3)"))
        self.ui.tableWidget.setItem(3,4, QTableWidgetItem("Cell (3,4)"))
        self.ui.tableWidget.setItem(3,5, QTableWidgetItem("Cell (3,5)"))
        self.ui.tableWidget.setItem(3,6, QTableWidgetItem("Cell (3,6)"))
        self.ui.tableWidget.setItem(3,7, QTableWidgetItem("Cell (3,7)"))
