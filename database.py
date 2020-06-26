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



    # conditionList is for filtering query results
    def get_employee_full_info(self, conditionList):
        query = QSqlQuery()

        #create string to story query
        query_string = """SELECT employee.id as ID, employee.first_name as "First Name", employee.last_name as "Last Name",
                    employee.birthday as "Birthday", employee.department_name as "Department Name",
                    log_salary.salary as "Salary", log_position.position as "Position"
                    FROM employee, log_salary, log_position
                    WHERE employee.id = log_salary.employee_id AND employee.id = log_position.employee_id
                    AND log_salary.date = (SELECT max(date) FROM log_salary WHERE employee_id = employee.id)
                    AND log_position.date = (SELECT max(date) FROM log_position WHERE employee_id = employee.id)"""

        ### SET THE CONDITION (for filtering)
        ## conditionList example
        ## [["id", 2], ["first_name", "Paul"]]
        condition = ""
        list_length = len(conditionList)

        for i in range(list_length - 1):
            condition += conditionList[i][0]
            condition += " = "
            condition += conditionList[i][1]
            condition += " and "

        # for the last condition, we don't need 'and'
        if list_length > 0:
            condition += conditionList[list_length - 1][0]
            condition += " = "
            condition += conditionList[list_length - 1][1]

        if condition:  # if condition is not Empty
            query_string += " and " + condition

        print(query_string)






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
        query.bindValue(":date", datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        query.bindValue(":reason", reason)

        return query.exec()


    ### insert into log_position ###
    def insert_new_position(self, id, new_position):
        query = QSqlQuery()

        query.prepare("""insert into log_position(employee_id, position, date)
                        values(:e_id, :position, :date)""")
        query.bindValue(":e_id", id)
        query.bindValue(":position", new_position)
        # import datetime
        query.bindValue(":date", datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

        return query.exec()


    ### get id of last employee which was added into database
    def get_last_employee_id(self):
        query = QSqlQuery()

        res = query.exec("""select max(id) from employee""")

        # there are existing employees
        if query.next():
            return query.value(0)

        return 0    # this should not return, because we will always insert an employee, before we insert anything into log_salary, or log_position


    ### insert new employee ###
    def insert_new_employee(self, employeeFullInfo):
        query = QSqlQuery()

        # Use a prepare statement, as we can use some variables in place of values
        query.prepare("""insert into employee(first_name, last_name, birthday, department_name)
                        values(:fn, :ln, :birthday, :department)""")

        query.bindValue(":fn", employeeFullInfo.first_name)
        query.bindValue(":ln", employeeFullInfo.last_name)
        query.bindValue(":birthday", employeeFullInfo.birthday)
        query.bindValue(":department", employeeFullInfo.department)

        query.exec()


        # we also need to input a salary and position for every new employee
        id = self.get_last_employee_id()
        query.prepare("""insert into log_position(employee_id, position, date)
                        values(:e_id, :pos, :date)""")
        query.bindValue(":e_id", id)
        query.bindValue(":pos", employeeFullInfo.position)
        query.bindValue(":date", datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        query.exec()

        query.prepare("""insert into log_salary(employee_id, salary, date)
                        values(:e_id, :salary, :date)""")
        query.bindValue(":e_id", id)
        query.bindValue(":salary", employeeFullInfo.salary)
        query.bindValue(":date", datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        query.exec()


    ### delete employee ###
    def delete_employee(self, id):
        query = QSqlQuery()

        query.prepare("""delete from employee where id = :id""")
        query.bindValue(":id", id)
        query.exec()

        # delete employee's record from log_salary
        query.prepare("""delete from log_salary where employee_id = :id""")
        query.bindValue(":id", id)
        query.exec()

        # delete employee's record from log_position
        query.prepare("""delete from log_position where employee_id = :id""")
        query.bindValue(":id", id)
        query.exec()










