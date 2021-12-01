import sqlite3

# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database


class DBOperations:

    data_basename = "DBName.db"

    # creates a tables if non exists.
    sql_create_table_firsttime = """ 
    SELECT * FROM sqlite_master ;
    """

    # creates a new table.
    sql_create_table = """ 
    CREATE TABLE employees(
        
        EmployeeID INTEGER  
        Title TEXT NOT NULL , 
        Forename TEXT NOT NULL , 
        Surname TEXT NOT NULL ,
        EmailAddress  TEXT NOT NULL ,
        Salary INTEGER UNSIGNED NOT NULL ,
    
        PRIMARY KEY (EmailAddress));
    """

    sql_insert = ""
    sql_select_all = "select * from TableName"
    sql_search = "select * from TableName where EmployeeID = ?"
    sql_update_data = ""
    sql_delete_data = ""
    sql_drop_table = ""

    def __init__(self):
        try:
            # creating a connection
            self.connect = sqlite3.connect(self.data_basename)
            # creating a cursor to interact with the database.`
            self.cursor = self.connect.cursor()
            # executing a command.
            # test to see if table exists.
            self.cursor.execute(self.sql_create_table_firsttime)
            # commit and save the changes.
            self.connect.commit()
        except Exception as e:
            print(e)
            print("this one is printing the table employees already exists")
        finally:
            self.connect.close()

    def get_connection(self):
        """Creating a connection to the database."""
        # creating a connection
        self.connect = sqlite3.connect(self.data_basename)
        # creating a cursor to interact with the database.
        self.cursor = self.connect.cursor()

    def create_table(self):
        """Creating a table in the database."""
        try:
            self.get_connection()
            self.cursor.execute(self.sql_create_table)
            self.connect.commit()
            print("Table created successfully")
        except Exception as e:
            print(e)
            print("this is printing the table of employees already exists")
        finally:
            self.connect.close()

    def drop_table(self):
        """Removes a table from the database."""
        pass

    def recreate_table(self):
        """???"""
        pass

    def insert_data(self):
        """Inserts data into a Table within the database."""
        try:
            self.get_connection()

            # check that input is in the correct format.
            # HMMM does the employee exist already.

            employee = Employee()
            # remove input employee id
            # find max current employeeid and + 1.
            employee.set_employee_id(int(input("Enter Employee ID: ")))
            # create new employee details
            # tile--> drop down menu.
            # forename and surename --> string input.
            # email string input with correct formatting.
            # salary --> int input 2 d.p.
            self.cursor.execute(
                self.sql_insert, tuple(str(employee).split("\n"))
            )
            self.connect.commit()
            print("Inserted data successfully")
            # do you want to add another
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def select_all(self):
        try:
            self.get_connection()
            self.cursor.execute(self.sql_select_all)
            results = self.cursor.fetchall()

            # think how you could develop this method to show the records

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


class userinput:
    def __init__(self) -> None:
        pass


def display_menu():
    print("\n Menu:")
    print("**********")
    print(" 1. Create table EmployeeUoB")
    print(" 2. Insert data into EmployeeUoB")
    print(" 3. Select all data into EmployeeUoB")
    print(" 4. Search an employee")
    print(" 5. Update data (to update a record")
    print(" 6. Delete data (to delete a record")
    print(" 7. Exit\n")
    return


def menu_select1(dp_ops):

    db_ops.create_table()
    # test does employee table exists.
    # if exists does admin want to override.
    # if yes:
    # drop table
    # create table
    # exit
    pass


def menu_select2(dp_ops):

    while True:
        try:
            # check that input is in the correct format.
            # HMMM does the employee exist already.
            # remove input employee id
            # find max current employee_id and + 1.
            # create new employee details
            # tile--> drop down menu.
            # forename and surename --> string input.
            # email string input with correct formatting.
            # salary --> int input 2 d.p.
            # do you want to add another
            db_ops.insert_data()
        except Exception as e:
            print(e)
        finally:
            pass


# The main function will parse arguments.
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.
if __name__ == "__main__":
    while True:
        try:
            display_menu()
            __choose_menu = int(input("Enter your choice: "))
            db_ops = DBOperations()
            if __choose_menu == 1:
                menu_select1(dp_ops)
                # db_ops.create_table()
            elif __choose_menu == 2:
                menu_select2(dp_ops)
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
