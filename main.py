# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtWidgets, QtCore
from mainmenu import MainWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)


    mainWindow = MainWindow()
    mainWindow.show()


    sys.exit(app.exec_())
