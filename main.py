# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication
from gui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    if window.runThread.isAlive():
        window.ui.fightModeAButton.label = '1'
    sys.exit(app.exec_())
