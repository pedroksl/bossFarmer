from controllers.ConfigurationObj import ConfigurationObj

class ConfigurationController():
    configs = ConfigurationObj()

    def __init__(self, mainWindow, configDir=''):
        self.mw = mainWindow
        self.setupConfigs(configDir)

    def setConfigDir(self, configDir=''):
        setupConfigs(configDir)

    def setupConfigs(self, configDir=''):
        if configDir is '':
            self.configs.default()
        else:
            self.configs = readConfigsJson(configDir)

    def setFightModeA(self):
        self.configs.fightMode = 0

    def setFightModeB(self):
        self.configs.fightMode = 1

    def setFightModeC(self):
        self.configs.fightMode = 0

    def setFightModeD(self):
        self.configs.fightMode = 0

    def setFightModeE(self):
        self.configs.fightMode = 0

    def setFightModeF(self):
        self.configs.fightMode = 0

    def toggleControlledDamage(self):
        self.configs.controlledDamage = not self.configs.controlledDamage
        print("ControlledDamage is: %s" % self.configs.controlledDamage)

    def toggleSkills(self):
        self.configs.enableSkills = not self.configs.enableSkills
        print("enableSkills is: %s" % self.configs.enableSkills)

    def toggleUlt(self):
        self.configs.enableUlt = not self.configs.enableUlt
        print("enableUlt is: %s" % self.configs.enableUlt)

    def toggleSummons(self):
        self.configs.summonBosses = not self.configs.summonBosses
        print("Summon Bosses is: %s" % self.configs.summonBosses)

    def toggleRun(self):
        self.configs.run = not self.configs.run
        print("run is: %s" % self.configs.run)

    def changeSkills(self):
        self.configs.ptSkillSelected += 1
        if self.configs.ptSkillSelected > 3:
            self.configs.ptSkillSelected = 1
        print("Party skill selected to use: %s" % self.configs.ptSkillSelected)


    def changeUlt(self):
        self.configs.heroSkillSelected += 1
        if self.configs.heroSkillSelected > 4:
            self.configs.heroSkillSelected = 1
        print("Hero skill selected to use: %s" % self.configs.heroSkillSelected)
