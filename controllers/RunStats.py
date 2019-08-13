class RunStats():
    def __init__(self, updateTable):
        self.killCount = 0
        self.updateTable = updateTable

    def bossKilled(self):
        self.killCount += 1
        self.updateTable()
