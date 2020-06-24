from PyQt5 import QtSql
from PyQt5.QtSql import *
from datetime import datetime

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


    def get_salary_log_for_employee(self, id):
        query = QSqlQuery()

        queryString = """SELECT employee.first_name as "First Name", employee.last_name as "Last Name",
                            employee.department_name as "Department name", log_salary.salary as "Salary",
                            log_salary.reason as "Reason", log_salary.date as "Date"
                            FROM employee, log_salary
                            WHERE employee.id = log_salary.employee_id AND employee.id = :id"""

        query.prepare(queryString)
        query.bindValue(":id", id)
        query.exec()

        record = query.record()
        column_number = record.count()

        header_list = []

        for i in range(column_number):
            header_list.append(record.field(i).name())

        result_list = []

        # while query has next value
        while query.next():
            sublist = []

            for i in range(column_number):
                sublist.append(query.value(i))
            result_list.append(sublist)

        return [header_list, result_list]




    def get_position_log_for_employee(self, id):
        query = QSqlQuery()

        queryString = """SELECT employee.first_name as "First Name", employee.last_name as "Last Name",
                            employee.department_name as "Department name", log_position.position as "Position",
                            log_position.date as "Date"
                            FROM employee, log_position
                            WHERE employee.id = log_position.employee_id AND employee.id = :id"""

        query.prepare(queryString)
        query.bindValue(":id", id)
        query.exec()

        record = query.record()
        column_number = record.count()

        header_list = []

        for i in range(column_number):
            header_list.append(record.field(i).name())

        result_list = []

        # while query has next value
        while query.next():
            sublist = []

            for i in range(column_number):
                sublist.append(query.value(i))
            result_list.append(sublist)

        return [header_list, result_list]



    def get_employee_full_info(self):
        query = QSqlQuery()

        #create string to story query
        query_string = """SELECT employee.id as ID, employee.first_name as "First Name", employee.last_name as "Last Name",
                    employee.birthday as "Birthday", employee.department_name as "Department Name",
                    log_salary.salary as "Salary", log_position.position as "Position"
                    FROM employee, log_salary, log_position
                    WHERE employee.id = log_salary.employee_id AND employee.id = log_position.employee_id
                    and log_salary.date = (SELECT max(date) FROM log_salary WHERE employee_id = employee.id)
                    and log_position.date = (SELECT max(date) FROM log_position WHERE employee_id = employee.id)"""
        res = query.exec(query_string)  # returns TRUE if query was executed successfully

        record = query.record()
        column_number = record.count()


        header_list = []

        for i in range(column_number):
            header_list.append(record.field(i).name())


        result_list = []

        # while query has next value
        while query.next():
            sublist = []

            for i in range(column_number):
                sublist.append(query.value(i))
            result_list.append(sublist)

        return [header_list, result_list]


    ### insert into log_salary ###
    def insert_new_salary(self, id, new_salary, reason):
        query = QSqlQuery()

        query.prepare("""insert into log_salary(employee_id, salary, date, reason)
                        values(:e_id, :salary, :date, :reason)""")
        query.bindValue(":e_id", id)
        query.bindValue(":salary", new_salary)
        # import datetime
        query.bindValue(":date", datetime.today().strftime('%Y-%m-%d'))
        query.bindValue(":reason", reason)

        return query.exec()

