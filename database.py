from PyQt5 import QtSql
from PyQt5.QtSql import *

# Singleton: can only instantiate it once
class Database:
    is_instantiated = False

    def __init__(self):
        if not Database.is_instantiated:
            print("Database has been instantiated!")
            self.db = QSqlDatabase.addDatabase("QSQLITE") #we are using SQLITE
            #specify path to database in next line
            self.db.setDatabaseName("/home/terry/Documents/Qt Projects/EmployeeManagementPyQt/database/database.db")
            self.db.open()
            Database.is_instantiated = True
        else:
            print("Database has already been created!")
