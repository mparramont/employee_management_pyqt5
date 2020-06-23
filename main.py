# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtWidgets, QtCore
from mainmenu import MainWindow
from database import Database

if __name__ == "__main__":
    import sys
#    app = QtWidgets.QApplication(sys.argv)


#    mainWindow = MainWindow()
#    mainWindow.show()


#    sys.exit(app.exec_())



#####################################
# Test salary log and position log queries
    database = Database()
    print(database.get_position_log_for_employee(2)[0])
    print(database.get_position_log_for_employee(2)[1])
    print(database.get_salary_log_for_employee(2)[0])
    print(database.get_salary_log_for_employee(2)[1])

#####################################
    # Demonstration of singleton: database can only be instantiated once
#    database1 = Database()
#    database2 = Database()

####### TEST Database.py ###########
#    database = Database()

#    print(database.get_employee_full_info()[0])
#    print(database.get_employee_full_info()[1])
