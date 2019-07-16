class ConfigurationObj():
    enableSkills = True  # Enables de use of party skills, also used to turn auto skill on
    enableUlt = True  # Enable the use of ultimate skills
    controlledDamage = False  # Leaves fights early to reduce damage output
    randomizedDamage = True  # Randomizes the timer to leave fight on controlled mode
    summonBosses = True  # Allow boss summoning
    run = False  # Variable used to start/stop running the code
    ptSkillSelected = 1  # Party skill selected to use
    heroSkillSelected = 1  # Hero skill selected to use
    timeout = 600  # Time to wait before reconnecting to the game after login from another device
    unstuck = 400  # Time to wait before leaving a battle because the code is stuck
    refreshBossScreen = 60  # Time without bosses to refresh the page
    menuUnstuck = 30  # Time to wait in the menu before trying to unstuck
    bossTimer = 70  # Time to wait before leaving a boss battle in controlled mode
    pixelOffset = False # Parameter used to offset pixel rgb comparison by some pixels
    fightMode = 0

    def default(self):
        self.enableSkills = True
        self.enableUlt = True
        self.controlledDamage = False
        self.randomizedDamage = True
        self.summonBosses = True
        self.run = False
        self.ptSkillSelected = 1
        self.heroSkillSelected = 1
        self.timeout = 600
        self.unstuck = 400
        self.refreshBossScreen = 60
        self.menuUnstuck = 30
        self.bossTimer = 70
        self.windowName = "NoxPlayer"
        self.pixelOffset = False
        self.fightMode = 0
