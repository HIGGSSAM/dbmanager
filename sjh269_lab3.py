import sqlite3

import subprocess
import platform
import inquirer
import re

# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database


class DBOperations:

    database_name = "DBName.db"

    # check database for employee table.
    sql_check_table = """ 
    
    SELECT name 
    FROM sqlite_master 
    WHERE type = table 
    AND name = employees

    """

    # creates a new table.
    sql_create_table = """ 
    CREATE TABLE employees(
        
        EmployeeID INTEGER  
        Title TEXT NOT NULL , 
        Forename TEXT(20) NOT NULL , 
        Surname TEXT(20) NOT NULL ,
        EmailAddress  TEXT NOT NULL ,
        Salary INTEGER UNSIGNED NOT NULL ,
    
        PRIMARY KEY (EmailAddress));
    """
    # inserts variable data into table.
    sql_insert = """
    
    INSERT INTO employees (EmployeeID, Title, Forename, Surename, EmailAddress, Salary)
    VALUES (?, ?, ?, ?, ?, ?)
    
    """
    # returns the top primary key value.
    sql_select_top_primary_key = """

    SELECT MAX(EmployeeID)
    FROM employees

    """

    # selects all from employee table and orders the results by employee ID.
    sql_select_all = """
    
    SELECT * 
    FROM employees 
    ORDER BY EmployeeID
    
    """

    # selects specific data from employee table.
    sql_search = """
    
    SELECT * 
    FROM TableName 
    WHERE EmployeeID = (?)
    
    """

    #
    sql_update_data = """
    
    UPDATE employees
    SET VALUES = (?, ?, ?, ?, ?, ?)
    WHERE VALUES = (?, ?, ?, ?, ?, ?);

    """

    #
    sql_delete_data = """
    
    DROP TABLE employees

    """
    sql_drop_table = ""

    def __init__(self):
        try:
            # creating a connection
            self.connect = sqlite3.connect(self.database_name)
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
        self.connect = sqlite3.connect(self.database_name)
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
            print("check table def.")
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
            print("create table def.")
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
            print("remove table def.")
        finally:
            self.connect.close()

    def check_data(self, tuple_data):
        """Checks if inputted data already exist in the table."""
        try:
            self.get_connection()
        except Exception as e:
            print(e)
        finally:
            self.connect.close()

    def get_next_primary_key(self):
        """Returns the next available primary key as integer."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_select_top_primary_key)
            result = int(self.cursor.fetchall() + 1)
            return result
        except Exception as e:
            print(e)
        finally:
            self.connect.close()

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
            self.connect.close()

    def select_all(self):
        """Selects all the data from employee table."""
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


class Userinput:
    def __init__(self, input_menu):
        self.input_menu = input_menu

    def yes_no_input(self, input_message_str):
        """User input returning boolean for a yes/no questions."""
        print(input_message_str)
        while True:
            __user_input = input("Enter Y/n: ").upper()
            if __user_input in ["Y", "YES"]:
                return True
            elif __user_input in ["N", "NO"]:
                return False
            else:
                print("Input Error: please input Y/n.")

    def input_int(self, input_message_str):
        """User input returning int value from input question."""
        pass

    def input_str(self, input_messge_str):
        """User input returning string value from input question."""
        pass

    def input_list(self, input_message_str, input_items_list):
        """User input from list menu returning a single selection value in a dic, user_selection: ."""

        questions = [
            inquirer.List(
                "user_selection",
                message=input_message_str,
                choices=input_items_list,
            )
        ]

        user_selection = inquirer.prompt(questions)
        return user_selection


class ValidateInput:
    def __init__(self) -> None:
        """No state information to be initialised."""
        pass

    def validate_employeeid_format(self, data_input):
        """Validates format of data input for employee id."""

        while True:
            try:
                return int(data_input)
            except ValueError as e:
                print("e")

    def validate_employee_title_input(self, data_input):
        """Validates the format of data inputted for employee title."""

        while True:
            try:
                return str(data_input)
            except Exception as e:
                print("e")

    def validate_employee_forename_input(self, data_input):
        """Validates the format of data inputted for employee forename."""

        while True:
            try:
                if 0 < len(data_input) <= 20:
                    return str(data_input)
                else:
                    print("Input value too long for forename data value.")
            except Exception as e:
                print("e")

    def validate_employee_surname_input(self, data_input):
        """Validates the format of data inputted for employee surname."""

        while True:
            try:
                if 0 < len(data_input) <= 20:
                    return str(data_input)
                else:
                    print("Input value too long for surname data value.")
            except Exception as e:
                print("e")

    def validate_employee_email_input(self, data_input):
        """Validates the format of data inputted for employee email."""

        while True:
            try:
                # re matching __ @ __ . __ format.
                if re.fullmatch(
                    "^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                    data_input,
                ):
                    return str(data_input)
            except Exception as e:
                print("e")

    def validate_employee_salary_input(self, data_input):
        """Validates the format of data inputted for employee salary."""

        while True:
            try:
                return float(data_input)
            except Exception as e:
                print("e")


class Menu:
    def __init__(self, admin=False):
        """Inistailises admin status, default value is false."""
        self.admin = admin

    def user_menu(self):
        """
        Displays standard user menu,
        default = non admin menu,
        Returns = int value of the user selected input."""

        input_selection = Userinput("main_menu_inputs")

        admin_selections = [
            "Create table Employee.",
            "Insert data into Employee.",
            "Select all the data from Employee table.",
            "Search for an employee.",
            "Update data - update record in Employee table.",
            "Delete data - delete record in Employee table.",
            "Exit",
        ]
        user_selections = [
            "Insert data into Employee.",
            "Select all the data from Employee table.",
            "Search for an employee.",
            "Update data - update record in Employee table.",
            "Delete data - delete record in Employee table.",
            "Exit",
        ]

        try:
            if self.admin:
                print("\n Admin Menu:\n -----------")
                selection = input_selection.input_list(
                    "Enter your selection: ", admin_selections
                )
                # convert dictionary to number and return.
                selection = (
                    admin_selections.index(selection["user_selection"]) + 1
                )
            else:
                print("\n Menu:\n -----")
                selection = input_selection.input_list(
                    "Enter your selection: ", user_selections
                )
                # convert dictionary to number and return.
                selection = (
                    user_selections.index(selection["user_selection"]) + 1
                )
            return selection
        except Exception as e:
            print(e)

    def menu_option_create_table(self):
        """ADMIN ONLY. Creating the employee table with an override option."""

        db_ops = DBOperations()
        user_inputs = Userinput("menu_create_table_inputs")

        # test does employee table exists.
        if db_ops.check_table():
            # if exists does admin want to override.
            if user_inputs.yes_no_input(
                "The table exist, do you want to override?"
            ):
                db_ops.drop_table()
                db_ops.create_table()
        else:
            db_ops.create_table()

    def menu_option_insert_data(self):
        """Inserting data into the employee table."""

        db_ops = DBOperations()
        user_inputs = Userinput("menu_2_inputs")

        while True:
            try:
                employee = Employee()
                check_validity = ValidateInput()

                # prompt user to select available id or enter another.
                if user_inputs.yes_no_input(
                    "Do you want to insert your own User ID?"
                ):
                    # get employee input data.
                    employee.set_employee_id(
                        check_validity.validate_employeeid_format(
                            input("Enter Employee ID: ")
                        )
                    )
                else:
                    # gets the next available primary key from table.
                    employee.set_employee_id(db_ops.get_next_primary_key())

                # check input is available.
                db_ops.check_primary_key(employee.get_employee_id())

                # check that input is in the correct format. ???
                employee.set_employee_title(
                    str(input("Enter Employee Title: "))
                )
                employee.set_forename(
                    check_validity.validate_employee_forename_input(
                        input("Enter Employee Forename: ")
                    )
                )
                employee.set_surname(
                    check_validity.validate_employee_surname_input(
                        input("Enter Employee Surname: ")
                    )
                )
                employee.set_email(
                    check_validity.validate_employee_email_input(
                        input("Enter Employee Email: ")
                    )
                )
                employee.set_salary(
                    check_validity.validate_employee_salary_input(
                        input("Enter Employee Salary: ")
                    )
                )

                # convert employee into tuple.
                input_data = tuple(str(employee).split("\n"))

                # NICE TO ADD
                ## Check does the employee already exist.
                # db_ops.check_data(
                #    input_data
                # )  # warning message if all but primary key is matched. do you still want to add?

                # insert data into table.
                db_ops.insert_data(input_data)

                # prompt user to insert
                if not user_inputs.yes_no_input(
                    "Do you want to enter another employee's details?"
                ):
                    return

            except Exception as e:
                print(e)

    def menu_option_display(self):
        """Selects and displays all the data for the Employee table."""

        db_ops = DBOperations()
        while True:
            try:
                data = db_ops.select_all()
                printing_data(data)
            except Exception as e:
                print(e)

    def menu_option_seaching_employee(self):
        """Displays data in employee table from user input."""
        pass

    def menu_option_update_data(self):
        """Updated current data in employee table from user input."""
        pass

    def menu_option_delete_data(self):
        """Deleting current data in employee table from user input."""
        pass


def printing_data(data_tuple):
    """Formats and prints out data from a tuple to the termial."""
    # if more than 20 records only display the first 20
    # and press Enter to move through records?

    # print out formatted table with column headers.
    for row in data_tuple:
        output = """{0}\t{1}\t{2}\t{3}\t{4}\t{5}""".format(*row)
        print(output)
        # print(row)  # format tuple into table.


def clear_terminal():
    """Clears the terminal display."""
    if platform.system() == "Windows":
        subprocess.call("cls", shell=True).communicate()
    else:
        print("\033c", end="")


# The main function will parse arguments.
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.
if __name__ == "__main__":
    while True:
        try:
            # clear_terminal()
            # choose admin status
            start_menu = Menu(True)
            __choose_menu = start_menu.user_menu()

            if __choose_menu == 1:
                start_menu.menu_option_create_table()
            elif __choose_menu == 2:
                start_menu.menu_option_insert_data()
            elif __choose_menu == 3:
                start_menu.menu_option_display()
            elif __choose_menu == 4:
                start_menu.menu_option_seaching_employee()
            elif __choose_menu == 5:
                start_menu.menu_option_update_data()
            elif __choose_menu == 6:
                start_menu.menu_option_delete_data()
            elif __choose_menu == 7:
                exit()
            else:
                print("Invalid Choice")
        except EOFError:
            exit()
        except KeyboardInterrupt:
            print("Signal: Interrupt")
            exit()
