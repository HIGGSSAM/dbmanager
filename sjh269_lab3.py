import sqlite3

import subprocess
import platform

# import inquirer

# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database


class DBOperations:

    data_basename = "DBName.db"

    # check database for employee table.
    sql_check_table = """ 
    
    SELECT name 
    FROM sqlite_master 
    WHERE type = table 
    AND name = employees;

    """

    # creates a new table.
    sql_create_table = """ 
    CREATE TABLE IF NOT EXISTS employees(
        
        EmployeeID INTEGER  
        Title TEXT NOT NULL , 
        Forename TEXT NOT NULL , 
        Surname TEXT NOT NULL ,
        EmailAddress  TEXT NOT NULL ,
        Salary INTEGER UNSIGNED NOT NULL ,
    
        PRIMARY KEY (EmailAddress));
    """
    # inserts variable data into table.
    sql_insert = """
    
    INSERT INTO employees (EmployeeID, Title, Forename, Surename, Emailaddress, Salary)
    VALUES (?, ?, ?, ?, ?, ?)
    
    """

    # selects all from employee table.
    sql_select_all = "select * from employees"

    sql_search = "select * from TableName where EmployeeID = ?"
    sql_update_data = ""
    sql_delete_data = ""
    sql_drop_table = ""

    def __init__(self):
        try:
            # creating a connection
            self.connect = sqlite3.connect(self.data_basename)
            # creating a cursor to interact with the database.
            self.cursor = self.connect.cursor()
            # if no employee table.
            if not self.check_table():
                # create an empty employee table.
                self.create_table()
            # commit and save the changes.
            self.connect.commit()
        except Exception as e:
            print(e)
        finally:
            self.connect.close()

    def get_connection(self):
        """Creating a connection to the database."""
        # creating a connection
        self.connect = sqlite3.connect(self.data_basename)
        # creating a cursor to interact with the database.
        self.cursor = self.connect.cursor()

    def check_table(self):
        """Checks if a table exists in the database."""
        try:
            # creating a connection.
            self.get_connection()
            # test to see if employee table exists.
            self.cursor.execute(self.sql_check_table)
            if self.cursor.fetchone == None:
                print("Table does not exists in database.")
                return False
            else:
                print("Table exists in database.")
                return True
        except Exception as e:
            print(e)
        finally:
            self.connect.close()

    def create_table(self):
        """Creating a table in the database."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_create_table)
            self.connect.commit()
            print("Table created successfully.")
        except Exception as e:
            print(e)
            print("this is printing the table of employees already exists")
        finally:
            self.connect.close()

    def drop_table(self):
        """Removes a table from the database."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_drop_table)
            self.connect.commit()
            print("Table deleted successfully.")
        except Exception as e:
            print(e)
        finally:
            self.connect.close()

    def check_data(self, tuple_data):
        """Checks if inputted data already exist in the table."""
        pass

    def check_primary_key(self, primary_key):
        """Checks if selected primary key already exists in table."""
        pass

    def insert_data(self, tuple_data):
        """Inserts data as a tuple into a table within the database."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_insert, tuple_data)
            self.connect.commit()
            print("Inserted data successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def select_all(self):
        """Selects all the data from a Table."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_select_all)
            # saves (fetches) all data and assigns it to results.
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(e)
        finally:
            self.connect.close()

    def printing_data(self, data):
        """Formats and prints out data from a tuple to the termial."""
        for row in data:
            print(row)

    def search_data(self):
        try:
            self.get_connection()
            employeeID = int(input("Enter Employee ID: "))
            self.cursor.execute(self.sql_search, tuple(str(employeeID)))
            result = self.cursor.fetchone()
            if type(result) == type(tuple()):
                for index, detail in enumerate(result):
                    if index == 0:
                        print("Employee ID: " + str(detail))
                    elif index == 1:
                        print("Employee Title: " + detail)
                    elif index == 2:
                        print("Employee Name: " + detail)
                    elif index == 3:
                        print("Employee Surname: " + detail)
                    elif index == 4:
                        print("Employee Email: " + detail)
                    else:
                        print("Salary: " + str(detail))
            else:
                print("No Record")

        except Exception as e:
            print(e)
        finally:
            self.connect.close()

    def update_data(self):
        try:
            self.get_connection()

            # Update statement

            if result.rowcount != 0:
                print(str(result.rowcount) + "Row(s) affected.")
            else:
                print("Cannot find this record in the database")

        except Exception as e:
            print(e)
        finally:
            self.connect.close()

    # Define Delete_data method to delete data from the table. The user will need to input the employee id to delete the corrosponding record.
    def delete_data(self):
        try:
            self.get_connection()

            if result.rowcount != 0:
                print(str(result.rowcount) + "Row(s) affected.")
            else:
                print("Cannot find this record in the database")

        except Exception as e:
            print(e)
        finally:
            self.connect.close()


class Employee:
    def __init__(self):
        self.employee_id = 0
        self.employee_title = ""
        self.forename = ""
        self.surname = ""
        self.email = ""
        self.salary = 0.0

    def set_employee_id(self, employee_id):
        self.employee_id = employee_id

    def set_employee_title(self, employee_title):
        self.employee_title = employee_title

    def set_forename(self, forename):
        self.forename = forename

    def set_surname(self, surname):
        self.surname = surname

    def set_email(self, email):
        self.email = email

    def set_salary(self, salary):
        self.salary = salary

    def get_employee_id(self):
        return self.employee_id

    def get_employee_title(self):
        return self.employee_title

    def get_forename(self):
        return self.forename

    def get_surname(self):
        return self.surname

    def get_email(self):
        return self.email

    def get_salary(self):
        return self.salary

    def __str__(self):
        return (
            str(self.employee_id)
            + "\n"
            + self.employee_title
            + "\n"
            + self.forename
            + "\n"
            + self.surname
            + "\n"
            + self.email
            + "\n"
            + str(self.salary)
        )


class userinput:
    def __init__(self) -> None:
        pass


def admin_menu():
    print("\n Admin Menu:")
    print("**********")
    print(" 1. Create table EmployeeUoB")
    print(" 2. Insert data into EmployeeUoB")
    print(" 3. Select all data into EmployeeUoB")
    print(" 4. Search an employee")
    print(" 5. Update data (to update a record")
    print(" 6. Delete data (to delete a record")
    print(" 7. Exit\n")
    return


def user_menu():
    print("\n Menu:")
    print("**********")
    # print(" 1. Create table EmployeeUoB")
    print(" 2. Insert data into EmployeeUoB")
    print(" 3. Select all data into EmployeeUoB")
    print(" 4. Search an employee")
    print(" 5. Update data (to update a record")
    print(" 6. Delete data (to delete a record")
    print(" 7. Exit\n")
    return


def clear_terminal():

    if platform.system() == "Windows":
        subprocess.call("cls", shell=True).communicate()
    else:
        print("\033c", end="")


def menu_select1():

    db_ops = DBOperations()

    db_ops.create_table()
    # test does employee table exists.
    if db_ops.check_table():
        # if exists does admin want to override.
        print("The table exist, do you want to override?")
        __user_input = input("Enter Y/n: ")
        if __user_input == "Y":
            # drop table
            db_ops.drop_table()
            # create new table
            db_ops.create_table()
        elif __user_input == "n":
            # exits
            exit  # look into error here.
        else:
            # invalid selection
            pass  # to do.
    else:
        db_ops.create_table()


def menu_select2():

    db_ops = DBOperations()
    while True:
        try:
            employee = Employee()
            # get employee input data.
            employee.set_employee_id(int(input("Enter Employee ID: ")))
            # offer next available id or input --> check input is available.
            db_ops.check_primary_key(employee.get_employee_id())

            employee.set_employee_title(str(input("Enter Employee Title: ")))
            employee.set_forename(str(input("Enter Employee Forename: ")))
            employee.set_surname(str(input("Enter Employee Surname: ")))
            employee.set_email(str(input("Enter Employee Email: ")))
            employee.set_salary(int(input("Enter Employee Salary: ")))

            # check that input is in the correct format.
            # ???

            # convert employee into tuple.
            input_data = tuple(str(employee).split("\n"))

            # Check does the employee already exist.
            db_ops.check_data(input_data)

            # insert data into table.
            db_ops.insert_data(input_data)

            # prompt user to insert
            print("The table exist, do you want to override?")
            __user_input = input("Enter Y/n: ")
            if __user_input == "Y":
                continue
            elif __user_input == "n" or "N":
                exit
        except Exception as e:
            print(e)


# The main function will parse arguments.
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.
if __name__ == "__main__":
    while True:
        try:
            # display_menu()
            __choose_menu = int(input("Enter your choice: "))
            if __choose_menu == 1:
                menu_select1()
            elif __choose_menu == 2:
                menu_select2()
            elif __choose_menu == 3:
                db_ops.select_all()
            elif __choose_menu == 4:
                db_ops.search_data()
            elif __choose_menu == 5:
                db_ops.update_data()
            elif __choose_menu == 6:
                db_ops.delete_data()
            elif __choose_menu == 7:
                exit(0)
            else:
                print("Invalid Choice")
        except EOFError:
            exit()
        except KeyboardInterrupt:
            print("signal: interrupt")
            exit()
