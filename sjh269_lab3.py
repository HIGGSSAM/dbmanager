"""
sjh269_lab3.py
--------------
CM50259 - Lab3 Coursework:
https://replit.com/@HIGGSSAM/CM50259-CW3#main.py
Termial interface for managing an SQLite database.

Classes:
--------
- DBOperations
- Employee
- UserInput
- FormatEmployeeInput
- Menu

Misc Functions:
---------------
- printing_data(Tuple)
- clear_terminal()

"""


import sqlite3
import re
import sys
from os import system, name
import pandas as pd
from tabulate import tabulate
import inquirer

# Disable the pylint errors from Black reformatting style on block indents

# pylint: disable=C0330
# suppress warning about too broad an exception

# pylint: disable=W0703
# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database


class DBOperations:
    """
    Contains all methods and variables associated with database manipulation.

    Variables:
    ----------
    - database_name (str)
    - sql_check_table (str)
    - sql_create_table (str)
    - sql_insert (str)
    - sql_select_top_primary_key (str)
    - sql_select_primary_key (str)
    - sql_select_all (str)
    - sql_search (str)
    - sql_search_record (str)
    - sql_update_data (str)
    - sql_delete_data (str)
    - sql_drop_table (str)

    Methods:
    --------
    - get_connection()
    - check_table() -> returns boolean
    - create_table() -> returns boolean
    - drop_table() -> returns boolean
    - check_data(tuple) -> returns boolean
    - get_next_primary_key() -> returns int
    - check_primary_key(tuple) -> returns boolean
    - insert_data(tuple)
    - get_column_headers() -> returns list
    - select_all() -> returns list
    - get_employee_record(tuple) -> returns tuple
    - update_data(tuple)
    - delete_data(tuple)

    """

    database_name = "DBName.db"

    # check database for employee table.
    sql_check_table = """

    SELECT name 
    FROM sqlite_master 
    WHERE type = "table" 
    AND name = "employees";

    """

    # creates a new table.
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS employees(
        EmployeeID INTEGER ,  
        Title TEXT NOT NULL , 
        Forename TEXT(20) NOT NULL , 
        Surname TEXT(20) NOT NULL ,
        EmailAddress  TEXT NOT NULL ,
        Salary INTEGER UNSIGNED NOT NULL ,
        PRIMARY KEY (EmployeeID));
    """

    # inserts variable data into table.
    sql_insert = """
    INSERT INTO employees (EmployeeID, Title, Forename, Surname, EmailAddress, Salary)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    # returns the top primary key value.
    sql_select_top_primary_key = """
    SELECT MAX(EmployeeID)
    FROM employees
    """

    # check if primary key value is in employee table.
    sql_select_primary_key = """
    SELECT EmployeeID
    FROM employees
    WHERE EmployeeID = ?;
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
    FROM employees 
    WHERE EmployeeID = ?;
    """

    # selects specific data from employees table.
    sql_search_record = """
    SELECT * 
    FROM employees 
    WHERE EmployeeID = (?) Title = (?), Forename = (?), Surname = (?), EmailAddress = (?), Salary = (?);
    """

    # updates an existing employee record in employees table.
    sql_update_data = """
    UPDATE employees
    SET EmployeeID = :ID, Title = :Title, Forename = :Forename, Surname = :Surname, EmailAddress = :Email, Salary = :Salary
    WHERE EmployeeID = :CurrentID;
    """

    # deletes existing employee record in employees table.
    sql_delete_data = """
    DELETE FROM employees
    WHERE EmployeeID = ?; 
    """

    # deletes an existing employees table.
    sql_drop_table = """
    DROP TABLE IF EXISTS employees;
    """

    def __init__(self):
        try:
            # ensures that database file is initialisied.
            self.connect = sqlite3.connect(self.database_name)
            # initialising cursor.
            self.cursor = None
            # closing connection to the database.
            self.connect.close()
            # if no employee table.
            if not self.check_table():
                # create an empty employee table.
                self.create_table()
        except sqlite3.DatabaseError as err:
            print(err)
            return None

    def get_connection(self):
        """Creating a connection to the database."""
        # creating a connection
        self.connect = sqlite3.connect(self.database_name)
        # creating a cursor to interact with the database.
        self.cursor = self.connect.cursor()

    def check_table(self):
        """Checks if a table exists in the database."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_check_table)
            if self.cursor.fetchone() is None:
                return False
            return True
        except sqlite3.DatabaseError as err:
            print(err)
            return None
        finally:
            self.connect.close()

    def create_table(self):
        """Creating a table in the database."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_create_table)
            self.connect.commit()
            return True
        except sqlite3.DatabaseError as err:
            print(err)
            return False
        finally:
            self.connect.close()

    def drop_table(self):
        """Removes a table from the database."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_drop_table)
            self.connect.commit()
            return True
        except sqlite3.DatabaseError as err:
            print(err)
            return False
        finally:
            self.connect.close()

    def check_data(self, tuple_data):
        """Checks if inputted data already exist in the table."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_search_record, tuple_data)
            result = self.cursor.fetchall()
            if result is None:
                return False
            return True
        except sqlite3.DatabaseError as err:
            print(err)
            return None
        finally:
            self.connect.close()

    def get_next_primary_key(self):
        """Returns the next available primary key as integer."""
        next_key = 1
        try:
            self.get_connection()
            self.cursor.execute(self.sql_select_top_primary_key)
            result = self.cursor.fetchone()[0]
            if result is None:
                return next_key
            next_key = int(result + 1)
            return next_key
        except sqlite3.DatabaseError as err:
            print(err)
            return None
        finally:
            self.connect.close()

    def check_primary_key(self, tuple_employee_id):
        """Checks if selected primary key already exists in table."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_select_primary_key, tuple_employee_id)
            if self.cursor.fetchone() is None:
                return False
            return True
        except sqlite3.DatabaseError as err:
            print(err)
            return None
        finally:
            self.connect.close()

    def insert_data(self, tuple_data):
        """Inserts data as a tuple into a table within the database."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_insert, tuple_data)
            self.connect.commit()
        except sqlite3.DatabaseError as err:
            print(err)
            return None
        finally:
            self.connect.close()

    def get_column_headers(self):
        """Returns the columns names of the Employee table."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_select_all)
            headers = [member[0] for member in self.cursor.description]
            return headers
        except sqlite3.DatabaseError as err:
            print(err)
            return None
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
        except sqlite3.DatabaseError as err:
            print(err)
            return None
        finally:
            self.connect.close()

    def get_employee_record(self, tuple_employee_id):
        """Returns a tuple of empolyee data."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_search, tuple_employee_id)
            data_tuple = self.cursor.fetchall()[0]
            return data_tuple
        except sqlite3.DatabaseError as err:
            print(err)
            return None
        finally:
            self.connect.close()

    def update_data(self, data_dic):
        """Updates an employee record in Employee Table form input tuple."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_update_data, data_dic)
            self.connect.commit()
        except sqlite3.DatabaseError as err:
            print(err)
            return None
        finally:
            self.connect.close()

    def delete_data(self, tuple_employee_id):
        """Deletes employee record from Employee Table using employee id."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_delete_data, tuple_employee_id)
            self.connect.commit()
        except sqlite3.DatabaseError as err:
            print(err)
            return None
        finally:
            self.connect.close()


class Employee:
    """
    Contains all methods an variables accosiated with an employee.

    Variables:
    ----------
    - forename_max_lenght (int) = 20
    - surname_max_lenght (int) = 20

    Methods:
    --------
    - set_employee_id(int)
    - set_employee_title(str)
    - set_forename(str)
    - set_surname(str)
    - set_email(str)
    - set_salary(float)
    - get_employee_id() -> returns set_employee_id())
    - get_employee_title() -> returns set_employee_title()
    - get_forename() -> returns set_forename()
    - get_surname() -> returns set_surname()
    - get_email() -> returns set_email()
    - get_salary() -> returns set_salary()
    - unpack_employee_tuple(tuple)

    """

    forename_max_length = 20
    surname_max_length = 20

    def __init__(self):
        self.employee_id = 0
        self.employee_title = ""
        self.forename = ""
        self.surname = ""
        self.email = ""
        self.salary = 0.0

    def set_employee_id(self, employee_id):
        """Sets employee id."""
        self.employee_id = employee_id

    def set_employee_title(self, employee_title):
        """Sets employee title."""
        self.employee_title = employee_title

    def set_forename(self, forename):
        """Sets employee forename."""
        self.forename = forename

    def set_surname(self, surname):
        """Sets employee surname."""
        self.surname = surname

    def set_email(self, email):
        """Sets employee email."""
        self.email = email

    def set_salary(self, salary):
        """Sets employee salary."""
        self.salary = salary

    def get_employee_id(self):
        """Gets employee id."""
        return self.employee_id

    def get_employee_title(self):
        """Gets employee title."""
        return self.employee_title

    def get_forename(self):
        """Gets employee forename."""
        return self.forename

    def get_surname(self):
        """Gets employee surname."""
        return self.surname

    def get_email(self):
        """Gets employee email."""
        return self.email

    def get_salary(self):
        """Gets employee salary."""
        return self.salary

    def unpack_employee_tuple(self, data_tuple):
        """Unpacks employee tuple record."""
        self.set_employee_id(data_tuple[0])
        self.set_employee_title(data_tuple[1])
        self.set_surname(data_tuple[2])
        self.set_forename(data_tuple[3])
        self.set_email(data_tuple[4])
        self.set_salary(data_tuple[5])

    def employee_record_dic(self):
        return {
            "ID": self.employee_id,
            "Title": self.employee_title,
            "Forename": self.forename,
            "Surname": self.surname,
            "Email": self.email,
            "Salary": self.salary,
        }

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
            if __user_input in ["N", "NO"]:
                return False
            print("Input Error: Please input Y/n.")

    def input_int(self, input_message_str):
        """User input returning positive int value from input question."""

        while True:
            __user_input = input(f"Enter {input_message_str}: ")
            if __user_input == "":
                return None
            if __user_input.isdigit() and int(__user_input) > 0:
                return int(__user_input)
            print("Input Error: Please enter a positive integer Number.")

    def input_float(self, input_message_str):
        """User input returning positive float value from input question."""

        while True:
            __user_input = input(f"Enter {input_message_str}: ")
            if __user_input == "":
                return None
            if float(__user_input) and float(__user_input) > 0:
                return float(__user_input)
            print("Input Error: Please enter a positive integer Number.")

    def input_str(self, input_message_str, max_length=50):
        """User input returning string value from input question."""

        while True:
            __user_input = input(f"Enter {input_message_str}: ")
            if __user_input == "":
                return None
            if 0 < len(__user_input) < max_length:
                return __user_input
            print(
                f"""Input Error: Please enter input with
                 less than {str(max_length)} characters"""
            )

    def input_list(self, input_message_str, input_items_list):
        """
        User input from list menu returning a single selection
        value in a dic, user_selection:
        """

        questions = [
            inquirer.List(
                "user_selection",
                message=input_message_str,
                choices=input_items_list,
            )
        ]

        user_selection = inquirer.prompt(questions)
        return user_selection


class FormatEmployeeInput:
    def __init__(self) -> None:
        """No state information to be initialised."""

    def input_employee_id(self, prompt_string, employee_id_default=None):
        """Validates format of data input for employee id."""

        user_inputs = Userinput("employee_id")
        db_ops = DBOperations()

        while True:
            try:
                if employee_id_default is not None:
                    prompt_string += " [" + str(employee_id_default) + "]"
                # get inputted employee ID.
                selection = user_inputs.input_int(prompt_string)

                # get if input = None and no current value
                # then return next available employee ID.
                if selection is None and employee_id_default is None:
                    return db_ops.get_next_primary_key()

                # get if input = None and there is a current value
                # then return the current employee ID.
                if selection is None and employee_id_default is not None:
                    return employee_id_default

                # if used message then already used!
                if db_ops.check_primary_key((selection,)):
                    print("Employee ID is already used.")
                else:
                    # else return ID.
                    return int(selection)
            except Exception as e:
                print(e)

    def get_employee_id(self):
        """Gets a valid existing employee id."""

        user_inputs = Userinput("employee_id")
        db_ops = DBOperations()

        while True:
            try:
                #  Entering employee ID.
                selection = user_inputs.input_int("Enter Employee ID")
                # if input != None and it exists.
                if selection is not None and db_ops.check_primary_key(
                    (selection,)
                ):
                    return int(selection)
                print("This employee id does not exist.")
            except Exception as e:
                print(e)

    def input_employee_title(self, prompt_string, title_default=None):
        """Validates the format of data inputted for employee title."""

        user_inputs = Userinput("employee_title")

        while True:
            try:
                if title_default is not None:
                    prompt_string += " [" + title_default + "]"
                # get inputted employee title.
                selection = user_inputs.input_str(prompt_string)
                if selection is None:
                    selection = title_default
                # if input != None then return.
                if selection is not None:
                    # format so only first letter is upper case.
                    return str(selection).title()
            except Exception as e:
                print(e)

    def input_employee_forename(
        self, prompt_string, forename_default=None, max_length=50
    ):
        """Validates the format of data inputted for employee forename."""

        user_inputs = Userinput("employee_forename")

        while True:
            try:
                if forename_default is not None:
                    prompt_string += "[" + forename_default + "]"
                # get inputted employee forename.
                selection = user_inputs.input_str(prompt_string, max_length)
                if selection is None:
                    selection = forename_default
                # if input != None then return.
                if selection is not None:
                    return str(selection).title()
            except Exception as e:
                print(e)

    def input_employee_surname(
        self, prompt_string, surname_default=None, max_length=50
    ):
        """Validates the format of data inputted for employee surname."""

        user_inputs = Userinput("employee_title")

        while True:
            try:
                if surname_default is not None:
                    prompt_string += "[" + surname_default + "]"
                # get inputted employee surname.
                selection = user_inputs.input_str(prompt_string, max_length)
                if selection is None:
                    selection = surname_default
                # if input != None then return.
                if selection is not None:
                    return str(selection).title()
            except Exception as e:
                print(e)

    def input_employee_email(self, prompt_string, email_default=None):
        """Validates the format of data inputted for employee email."""

        user_inputs = Userinput("employee_title")

        while True:
            try:
                if email_default is not None:
                    prompt_string += " [" + email_default + "]"
                # get inputted employee email.
                selection = user_inputs.input_str(prompt_string)
                if selection is None:
                    selection = email_default
                # if input != None and re matching __ @ __ . __ format.
                if selection is not None and re.findall(
                    r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                    selection,
                ):
                    return str(selection)
                print("Error: ENTER a email as __ @ __ . __ .")
            except Exception as e:
                print(e)

    def input_employee_salary(self, prompt_string, salary_default=None):
        """Validates the format of data inputted for employee salary."""
        user_inputs = Userinput("employee_title")

        while True:
            try:
                if salary_default is not None:
                    prompt_string += " [" + str(salary_default) + "]"
                # get inputted employee salary.
                selection = user_inputs.input_float(prompt_string)
                if selection is None:
                    selection = salary_default
                # if input != None then return.
                if selection is not None:
                    return float(selection)
            except Exception as e:
                print(e)


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
        screen_display = Displaydata()

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

        screen_display.clear_screen()
        print(
            "\nUse the up and down arrows to move through choices available."
        )

        screen_display.hide_cursor()

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
        except Exception as err:
            print(err)
        finally:
            screen_display.show_cursor()

    def create_employee_table(self):
        """ADMIN ONLY. Creating the employee table with an override option."""

        db_ops = DBOperations()
        user_inputs = Userinput("menu_create_table_inputs")

        # test does employee table exists and what to override.
        if db_ops.check_table() and user_inputs.yes_no_input(
            "The table exists, do you want to override?"
        ):
            # output current table to csv file

            # if table could not be dropped, error.
            if not db_ops.drop_table():
                print("Error: Employee table could not be removed.")
                return
        # if table has been created print message.
        if db_ops.create_table():
            print("Employee Table has been created.")

    def insert_employee_record(self):
        """Inserting data into the employee table."""

        db_ops = DBOperations()
        user_inputs = Userinput("menu_2_inputs")
        employee = Employee()
        employee_format = FormatEmployeeInput()
        screen_display = Displaydata()

        while True:
            try:

                screen_display.clear_screen()
                print("Inserting Employee\n")

                # setting employee id from user input.
                employee.set_employee_id(
                    employee_format.input_employee_id(
                        "Employee ID or hit Enter for next ID"
                    )
                )

                # setting employee title form user input.
                employee.set_employee_title(
                    employee_format.input_employee_title("Employee title")
                )

                # setting employee forename from user input.
                employee.set_forename(
                    employee_format.input_employee_forename(
                        "Employee forename", None, employee.forename_max_length
                    )
                )

                # setting employee surname from user input.
                employee.set_surname(
                    employee_format.input_employee_surname(
                        "Employee surname", None, employee.surname_max_length
                    )
                )

                # setting employee email from user input.
                employee.set_email(
                    employee_format.input_employee_email("employee email")
                )

                # setting employee salary from user input.
                employee.set_salary(
                    employee_format.input_employee_salary("employee salary")
                )

                # convert employee into tuple.
                input_data = tuple(str(employee).split("\n"))

                # insert data into table.
                if db_ops.insert_data(input_data):
                    print("Inserted data successfully.")

                # prompt user to insert
                if not user_inputs.yes_no_input(
                    "Do you want to enter another employee's details?"
                ):
                    return

            except Exception as e:
                print(e)

    def display_employee_records(self):
        """Selects and displays all the data for the Employee table."""

        display_data = Displaydata()
        db_ops = DBOperations()
        screen_display = Displaydata()
        try:
            screen_display.clear_screen()
            print("Employee Records\n")
            # return all the data from the employee table.
            data = db_ops.select_all()
            # return all the headers from the employee table.
            headers = db_ops.get_column_headers()
            # print out the table employees to the terminal.
            display_data.printing_data(data, headers)
        except Exception as e:
            print(e)

    def seaching_employee_records(self):
        """Displays data in employee table from user input."""

        user_inputs = Userinput("menu_2_inputs")
        db_ops = DBOperations()
        employee_format = FormatEmployeeInput()
        display_data = Displaydata()
        screen_display = Displaydata()

        while True:
            try:
                screen_display.clear_screen()
                print("Search for Employee\n")

                # get user inputted empoyee id.
                data = db_ops.get_employee_record(
                    (employee_format.get_employee_id(),)
                )
                # return all the headers from the employee table.
                headers = db_ops.get_column_headers()

                # print out employee record to the terminal.
                display_data.printing_data((data,), headers)

                # prompt user to edit another employee record.
                if not user_inputs.yes_no_input(
                    "Do you want to search another employee's details?"
                ):
                    return
            except Exception as e:
                print(e)

    def update_employee_record(self):
        """Updated current data in employee table from user input."""

        db_ops = DBOperations()
        user_inputs = Userinput("menu_2_inputs")
        employee = Employee()
        employee_format = FormatEmployeeInput()
        screen_display = Displaydata()

        while True:
            try:

                screen_display.clear_screen()
                print("Updating Employee\n")
                print(
                    "Please enter a new value or press "
                    "ENTER to keep the existing value.\n"
                )

                # prompt for input employee id and save.
                employee.set_employee_id(employee_format.get_employee_id())

                # save current employeee ID.
                current_employee_id = employee.get_employee_id()

                # gets employee record for inputted id value
                # and saves values to employee.
                employee.unpack_employee_tuple(
                    db_ops.get_employee_record((employee.get_employee_id(),))
                )

                # display message: do you want to retain or change value?
                # setting employee id from user input.
                employee.set_employee_id(
                    employee_format.input_employee_id(
                        "Employee ID", employee.get_employee_id()
                    )
                )

                # setting employee title from user input.
                employee.set_employee_title(
                    (
                        employee_format.input_employee_title(
                            "Employee title", employee.get_employee_title()
                        )
                    )
                )

                # setting employee forename from user input.
                employee.set_forename(
                    (
                        employee_format.input_employee_forename(
                            "Employee forename",
                            employee.get_forename(),
                            employee.forename_max_length,
                        )
                    )
                )

                # setting employee surname from user input.
                employee.set_surname(
                    (
                        employee_format.input_employee_surname(
                            "Employee surname",
                            employee.get_surname(),
                            employee.surname_max_length,
                        )
                    )
                )

                # setting employee email from user input.
                employee.set_email(
                    (
                        employee_format.input_employee_email(
                            "Employee email", employee.get_email()
                        )
                    )
                )

                # setting employee salary from user input.
                employee.set_salary(
                    (
                        employee_format.input_employee_salary(
                            "Employee salary", employee.get_salary()
                        )
                    )
                )

                # do you want to update the details?
                if user_inputs.yes_no_input(
                    "Do you want to save and update "
                    "changes to the Employee record?"
                ):
                    # convert employee into dictionary.
                    input_data = employee.employee_record_dic()
                    input_data.update({"CurrentID": current_employee_id})

                    # update data in employee table.
                    db_ops.update_data(input_data)

                # prompt user to edit another employee record.
                if not user_inputs.yes_no_input(
                    "Do you want to enter another employee's details?"
                ):
                    return

            except Exception as e:
                print(e)

    def delete_employee_record(self):
        """Deleting current data in employee table from user input."""

        db_ops = DBOperations()
        user_inputs = Userinput("menu_2_inputs")
        employee = Employee()
        employee_format = FormatEmployeeInput()
        screen_display = Displaydata()

        while True:
            try:
                screen_display.clear_screen()
                print("Delete Employee\n")

                # ask for valid employeeID to delete.
                employee.set_employee_id(employee_format.get_employee_id())

                # do you want to delete the selected employee?
                if user_inputs.yes_no_input(
                    "Do you want to delete the selected Employee record?"
                ):
                    # delete data in employee table.
                    db_ops.delete_data((employee.get_employee_id(),))

                # prompt user to delete another employee record.
                if not user_inputs.yes_no_input(
                    "Do you want to delete another Employee record?"
                ):
                    return

            except Exception as e:
                print(e)


class Displaydata:
    """routines to display output"""

    def __init__(self):
        # clear the screen for new output
        self.os = name

    def clear_screen(self):
        """clears the terminal for new ouput"""
        if self.os == "nt":
            _ = system("cls")
        else:
            _ = system("clear")

    def hide_cursor(self):
        """hides terminal cursor"""
        if not self.os == "nt":
            print("\x1b[?25l")

    def show_cursor(self):
        """reveals terminal cursor"""
        if not self.os == "nt":
            print("\x1b[?25h")

    def printing_data(self, data_tuple, headers_list):
        """Formats and prints out data from a tuple to the termial."""

        user_input = Userinput("printing data input")

        # self.clear_screen()

        # creating a dataframe of all the data to be printed.
        df = pd.DataFrame(data_tuple, columns=headers_list)
        print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))

        if user_input.yes_no_input(
            "Do you want to save te output to a csv file?"
        ):
            df.to_csv("employee_records.csv", index=False)
        user_input.yes_no_input("Enter yes to continue")


if __name__ == "__main__":
    while True:
        try:
            # choose admin status
            start_menu = Menu(True)
            __choose_menu = start_menu.user_menu()

            if __choose_menu == 1:
                start_menu.create_employee_table()
            elif __choose_menu == 2:
                start_menu.insert_employee_record()
            elif __choose_menu == 3:
                start_menu.display_employee_records()
            elif __choose_menu == 4:
                start_menu.seaching_employee_records()
            elif __choose_menu == 5:
                start_menu.update_employee_record()
            elif __choose_menu == 6:
                start_menu.delete_employee_record()
            elif __choose_menu == 7:
                sys.exit()
            else:
                print("Invalid Choice")
        except EOFError:
            sys.exit()
        except KeyboardInterrupt:
            print("\nAborting Program ...\n")
            sys.exit()
