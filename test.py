import sys
from PyQt5.QtWidgets import *
app = QApplication(sys.argv)
button = QPushButton("Hello", None)
button.show()
app.exec_()