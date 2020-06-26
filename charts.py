from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import *
from PyQt5.QtWidgets import *
from database import Database


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_2.addWidget(self.widget_2, 0, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(516, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setObjectName("backButton")
        self.gridLayout.addWidget(self.backButton, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 2)
        self.gridLayout_2.setRowStretch(0, 20)
        self.gridLayout_2.setRowStretch(1, 1)


        # can consider changing the names 'widget' and 'widget_2' to something clearer in explanation
        self.firstLayout = QGridLayout(self.widget)
        self.secondLayout = QGridLayout(self.widget_2)


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Charts"))
        self.backButton.setText(_translate("MainWindow", "Back"))



class ChartsWindow(QtWidgets.QMainWindow):

    # need to pass 'mainMenu' parameter in. (We need the ability to return to mainmenu)
    def __init__(self, mainMenu):
        super(ChartsWindow, self).__init__()
        self.mainMenu = mainMenu

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.database = Database()

        self.firstChart = QChart()
        self.secondChart = QChart()
        self.firstSeries = QBarSeries()
        self.secondSeries = QPieSeries()

        self.load_first_series()

        self.firstChart.addSeries(self.firstSeries)
        self.firstChart.setTitle("Salary Statistics")

        self.firstChartView = QChartView(self.firstChart) #(self.firstChart) is the parent
        self.firstChartView.setRenderHint(QPainter.Antialiasing)

        # add chartview to layout
        self.ui.firstLayout.addWidget(self.firstChartView)



        self.ui.backButton.clicked.connect(self.back_button_clicked)



    def load_first_series(self):
        # obtain result_list from database.py Database class -> get_salary_statistics function
        resultList = self.database.get_salary_statistics()

        minBarSet = QBarSet("Min. salary")
        avgBarSet = QBarSet("Avg. salary")
        maxBarSet = QBarSet("Max. salary")

        minBarSet << resultList[0]
        avgBarSet << resultList[1]
        maxBarSet << resultList[2]

        self.firstSeries.append(minBarSet)
        self.firstSeries.append(avgBarSet)
        self.firstSeries.append(maxBarSet)


    def back_button_clicked(self):
        self.hide()
        self.mainMenu.show()


    def back_button_clicked(self):
        self.hide()
        self.mainMenu.show()
