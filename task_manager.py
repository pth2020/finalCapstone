# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password

# =====importing libraries===========
from decimal import DivisionByZero
import os
from datetime import datetime, date

from tabulate import tabulate

# -- Setting the date format and assigning today's date to today
DATETIME_STRING_FORMAT = "%Y-%m-%d"
today = datetime.today()


# -- Line marker function for an output
def line_marker(num):
    line = ''
    if num == 30:
        line = "~" * 30
    elif num == 40:
        line = "~" * 40
    elif num == 60:
        line = "~" * 60
    elif num == 80:
        line = "~" * 80
    return line


def login():
    # ====Login Section====
    """ This code calls read_users() function to get username_password
    dictionary that stores/reads usernames and passwords from user.txt file
    to allow a user to login
    """
    # -- Dictionary that stores usernames (keys) and passwords (values)
    username_password = read_users()

    # -- Logged-in user (access to certain functions is restricted to non admin usernames)

    # -- Initialize logged in  state
    logged_in = False

    # -- Number of attempts to log in
    attempted_login = 0

    print("LOGIN\n")
    while not logged_in:
        if attempted_login == 3:
            print("Three unsuccessful login attempts!")
            print("Goodbye")
            break
            # -- User enters username and password
        curr_user_input = input("Username: ")
        curr_pass_input = input("Password: ")
        # -- User restricted from access if username is non-existent
        # or if a password is entered incorrectly
        if curr_user_input not in username_password.keys():
            print("User does not exist")
            attempted_login += 1
        elif username_password[curr_user_input] != curr_pass_input:
            print("Wrong password")
            attempted_login += 1
        else:
            print("Login Successful!")
            logged_in = True
            # -- Once user is successfully logged on, menu function is called
            menu()


# -- Function to verify if logged-in user is admin
def admin_privilege(user, password):
    has_privilege = False
    if user == 'admin' and password == 'password':
        has_privilege = True

    return has_privilege


# -- Function that retrieves all usernames and passwords from user.txt file
# and stores them in a dictionary - returns the dictionary
def read_users():
    user_file_name = 'user.txt'
    # If no user.txt file, write one with a default account
    if not os.path.exists(user_file_name):
        with open(user_file_name, "w") as default_file:
            default_file.write("admin;password")

    # Read in user_data
    with open(user_file_name, 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    username_password_dict = {}
    for user in user_data:
        username, password = user.split(';')
        username_password_dict[username] = password

    return username_password_dict


# -- Function that checks for duplicate usernames when registering users
def check_duplicate_user(new_user):
    # -- Making a call to read_users() to get username/password dict
    username_password = read_users()
    for user in username_password:
        if new_user == user:
            return True


# -- Function to confirm if passwords entered twice match
def confirm_password(new_password, conf_password):
    confirmed = False
    if new_password == conf_password:
        confirmed = True
    return confirmed


# -- Function to register new users
def reg_user():
    """Add a new user to the user.txt file"""

    # -- Dictionary with usernames and passwords
    username_password = read_users()

    # -- Enter username and password to access reg_user() function
    #    Only admin allowed to add a user
    user = input("Please enter your username: ")
    password = input("Please enter your password: ")

    while True:
        # Confirm if the logged-in user is admin

        if not admin_privilege(user, password):
            print("\nNo admin rights to register a user.\n")
            break

        # - Request input of a new username
        new_username = input("New Username: ")
        if check_duplicate_user(new_username):
            print("\nUser already exists.\n")
            break

        # - Request input of a new password
        new_password = input("New Password: ")
        # - Request input of password confirmation.
        password_again = input("Confirm Password: ")
        # - Check if the new password and confirmed password are the same.
        if confirm_password(new_password, password_again):
            # -- New user added to username_password dictionary
            username_password[new_username] = new_password
            print("New user added")
        else:
            print("\nPasswords do not match")
            continue

        # - User added to user.txt file
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
            break


def read_tasks():
    task_list = []
    task_file_name = 'tasks.txt'
    # Create tasks.txt if it doesn't exist
    if not os.path.exists(task_file_name):
        with open(task_file_name, "w") as default_file:
            pass

    with open(task_file_name, 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    for t_str in task_data:
        curr_t = {}
        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['id'] = task_components[0]
        curr_t['username'] = task_components[1]
        curr_t['title'] = task_components[2]
        curr_t['description'] = task_components[3]
        curr_t['due_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(str(task_components[5]), DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[6] == "Yes" else False

        task_list.append(curr_t)

    return task_list


# -- Function to add tasks for users
def add_task():
    # incremental id
    id_num = 1
    size = len(read_tasks())
    if size != 0:
        id_num += size
    # -- Dictionary with usernames and passwords
    username_password = read_users()
    # -- Number of unsuccessful attempts to create a task
    number_of_attempts = 0
    while True:
        if number_of_attempts == 3:
            break
        task_username = input("Name of person assigned to task: ")
        # -- Checks is user exists before assigning a task to the user
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            number_of_attempts += 1
            continue
        # -- Input task_title and task_description
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        if task_title == "" or task_description == "":
            print("Task title or Task description cannot be empty")
            break
        # -- Validates entered date
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
            break
        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
        # -- Default value for completed (task) is 'False' which turns to 'No' when saving into task.txt file
        new_task = {
            "id": id, "username": task_username, "title": task_title, "description": task_description,
            "due_date": due_date_time, "assigned_date": curr_date, "completed": False}

        # -- Calls read_task() function to retrieve all tasks into a dictionary
        # task_list = read_tasks()
        task_list = [new_task]
        # -- Add new assigned task to dictionary
        # -- Add new assigned task to tasks.txt file
        with open("tasks.txt", "a") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [str(t['id']), t['username'], t['title'], t['description'],
                            t['due_date'].strftime(DATETIME_STRING_FORMAT),
                            t['assigned_date'].strftime(DATETIME_STRING_FORMAT), "Yes" if t['completed'] else "No"
                            ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write) + "\n")
        print("Task successfully added.")
        break


def view_all_tasks():
    """Reads the tasks from tasks.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    """
    # -- Calls read_tasks() functions and stores all tasks into a list
    task_list = read_tasks()

    # -- Print all tasks in a table format
    # -- Headers for table
    headers = ["ID", "User", "Task", "Assigned to", "Due Date", "Date Assigned", "Task Description"]

    # -- Initialise a '2D to be' list for table data
    all_data = []

    for x in task_list:
        all_data.append(list(x.values()))

    # -- Initialise a tabulate object
    table1 = tabulate(all_data, headers=headers)
    print()
    print(table1)
    print()


# -- Function to verify if user exists in user.txt file
def user_verifier(uname, password):
    # -- To authenticate users if their username and password are registered
    user_verified = False

    # -- Dictionary with usernames and passwords
    username_password = read_users()

    try:
        if uname in username_password.keys():
            # -- Verifying username and password
            if username_password[uname] == password:
                user_verified = True
    except KeyError:
        print("Incorrect username/password")

    return user_verified


def view_my_task():
    """
    Reads a user's task from task.txt file
    and prints to the console.
    """

    # -- Number of attempts to log in
    attempted_authentication = 0

    while True:
        # -- Prompts user to enter their username and passport for verification
        username_entered = input("Enter your username: ")
        password_entered = input("Enter your password: ")

        # -- If username and password are verified it exists loop
        if user_verifier(username_entered, password_entered):
            break
        else:
            print("Username doesn't exist or one or both of username and password is/are incorrect")
            attempted_authentication += 1
            # -- Three failed authentication attempts reached
            if attempted_authentication == 3:
                break
    if attempted_authentication < 3:
        # -- Calls read_tasks() function and stores all tasks into a list for entered and verified username
        my_task_list = [t for t in read_tasks() if t['username'] == username_entered]

        # -- Checks if a user has a task/tasks assigned to them
        if len(my_task_list) == 0:
            print(f"\nNo tasks assigned to {username_entered} yet.\n")
        else:
            headers = ["ID", "Assigned to", "Task", "Task Description", "Due Date", "Date Assigned", "Task completed"]

            # -- Initialise a '2D to be' list for table data
            all_data = []

            for x in my_task_list:
                all_data.append(list(x.values()))

            table1 = tabulate(all_data, headers=headers)
            print()
            print(table1)
            print()

            # -- Calls update_task_menu and provide user with different options
        update_my_task_menu(my_task_list)
    else:
        print("\nToo many failed authentication attempts.\n")


def update_my_task_menu(my_t_list):
    # -- Task id number
    task_id_num = -1

    while True:

        try:
            # -- User prompted to select id number of their task to edit
            chosen_task_number = int(input("To edit task enter its id number: "))

            for i in range(len(my_t_list)):
                if int((my_t_list[i])['id']) == chosen_task_number:
                    task_id_num = chosen_task_number

            if task_id_num and task_id_num != -1:
                # -- Task menu
                task_menu = ''' 
                        Select your option:
                            co - set task completed
                            ed - edit task (user or due date)
                            ex - return to main menu                            
                        '''
                print(task_menu)
                break
            else:
                print("Incorrect input. Try again")
        except ValueError:
            print("Task id is empty.Try again")

    # -- User selects an option from task menu
    edit_option = input("Choose your option: ")

    # -- Option to set a selected task as completed
    if edit_option == 'co':
        update_to_complete_task(my_t_list, task_id_num)

    # -- Option to edit username and/or due date in a task
    elif edit_option == 'ed':
        while True:
            task_edit_menu = '''
                Select your option:
                    1 - Edit username
                    2 - Edit due date
                    3 - Return to main menu 
                '''
            print(task_edit_menu)

            task_edit_option = int(input("Choose your option:"))
            # -- Filter user's task into a list using task number and completeness criteria
            task_to_edit = [t for t in my_t_list if t['id'] == str(task_id_num) and not t['completed']]

            # -- List is non-empty - meaning not completed
            if task_to_edit:
                task_id = int((task_to_edit[0])['id'])

            # -- List is empty - meaning it is already completed
            else:
                print("\nTask cannot be edited. It is completed.\n")
                break

                # -- To edit username
            if task_edit_option == 1:
                update_username_task(task_to_edit, task_id)

            # -- To edit due date
            elif task_edit_option == 2:
                update_due_date_task(task_to_edit, task_id)

            elif task_edit_option == 3:
                print("\nReturning to main menu.\n")
                break
            else:
                print("Invalid option")
    elif edit_option == 'ex':
        print("\nReturning to main menu...\n")
    else:
        print("\nIncorrect input. Start all over again.\n")


def update_to_complete_task(task_list, task_number):
    read_task_list = read_tasks()
    # -- Filter user's task into a list using task number and completeness criteria
    task_to_complete = [t for t in task_list if t['id'] == str(task_number) and not t['completed']]
    # -- If list is non-empty
    if task_to_complete:
        # -- There should only be one item in it, hence task_to_complete[0]
        (task_to_complete[0])['completed'] = True

        # -- Task ID needed to update whole list (read_task_list or task_list) and task.txt file
        task_id_to_edit = int((task_to_complete[0])['id'])

        # -- Update whole list
        (read_task_list[task_id_to_edit - 1])['completed'] = True

        # -- Assign updated read_task_list to edited_task_list
        # and call update_task_file to update data in the task.txt file
        edited_task_list = read_task_list
        update_task_file(edited_task_list)

    else:
        print("Task is completed or no task available for user.")


def update_username_task(task_edit_list, t_id):
    read_task_list = read_tasks()
    edit_user = input("Enter new username: ")
    # -- Edit username for a selected task
    (task_edit_list[0])['username'] = edit_user

    # -- Edit username in the whole list
    (read_task_list[t_id - 1])['username'] = edit_user

    # -- Assign updated read_task_list to edited_task_list
    # and call update_task_file to update data in the task.txt file
    edited_task_list = read_task_list
    update_task_file(edited_task_list)


def update_due_date_task(task_edit_list, t_id):
    read_task_list = read_tasks()
    edit_due_date = datetime.strptime(input("Enter the new due date (YYYY-MM-DD): "), DATETIME_STRING_FORMAT)

    # -- Update due date in filtered list
    (task_edit_list[0])['due_date'] = edit_due_date

    # -- Update due date in the whole list
    (read_task_list[t_id - 1])['due_date'] = edit_due_date

    # -- Assign updated read_task_list to edited_task_list
    # and call update_task_file to update data in the task.txt file
    edited_task_list = read_task_list
    update_task_file(edited_task_list)


def update_task_file(task_list):
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            # -- Convert date to datetime and strip Hour:Min:Sec
            due_date_time = datetime.strptime(str(t['due_date']).strip(" 00:00:00"), DATETIME_STRING_FORMAT)
            str_attrs = [str(t['id']), t['username'], t['title'], t['description'],
                        # -- Convert date to str before updating file
                        datetime.strftime(due_date_time, '%Y-%m-%d'),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT), "Yes" if t['completed'] else "No"
                        ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write) + "\n")
    print("Task successfully updated.")


def display_statistics():
    """If the user is an admin they can display statistics about number of users
    and tasks."""

    user = input("Please enter your username: ")
    password = input("Please enter your password: ")

    # -- Read all users from user.txt
    username_password = read_users()

    if not username_password:
        print("Create users first\n")
        reg_user()

    # -- Read all tasks from task.txt
    task_list = read_tasks()

    if not task_list:
        print("create tasks first\n")
        add_task()

    if admin_privilege(user, password):
        # -- Total number of users
        num_users = len(username_password.keys())
        # -- Total number of tasks
        num_tasks = len(task_list)

        print(line_marker(40))
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print(line_marker(40))

    else:
        print("Only admin has the right to view statistics on users and tasks.")


def generate_tasks_report(t_list):
    """
    This function allows user to generate report on tasks.
    """
    # -- Assigning a list parameter to task_list
    task_list = t_list

    total_tasks = len(task_list)
    completed_tasks = len([ct for ct in task_list if ct['completed']])
    incomplete_tasks = total_tasks - completed_tasks

    # -- Working out all overdue tasks of users
    overdue_tasks = len([ovd_t for ovd_t in task_list if
                        datetime.strptime(str(ovd_t['due_date'].date()), DATETIME_STRING_FORMAT) < today])
    # -- Initialising incomplete and overdue tasks percentages
    incomplete_tasks_percent = 0.0
    overdue_task_percent = 0.0
    # -- Working out incomplete and overdue tasks percentages
    try:
        incomplete_tasks_percent = (incomplete_tasks / total_tasks) * 100
        overdue_task_percent = (overdue_tasks / total_tasks) * 100
    except DivisionByZero:
        print("No tasks allocated")

    # -- Add task data to new_task_report dictionary
    new_task_report = {
        'total_tasks': str(total_tasks),
        'completed_tasks': str(completed_tasks),
        'incomplete_tasks': str(incomplete_tasks),
        'overdue_tasks': str(overdue_tasks),
        'incomplete_tasks_percent': str(incomplete_tasks_percent),
        'overdue_task_percent': str(overdue_task_percent)
    }

    # -- Add new_task_report dictionary to task_report_list
    task_report_list = [new_task_report]

    # -- Add data to task_overview.txt
    with open('task_overview.txt', 'w') as task_report_file:
        task_report_to_write = []
        for t in task_report_list:
            str_attrs = [
                t['total_tasks'],
                t['completed_tasks'],
                t['incomplete_tasks'],
                t['overdue_tasks'],
                t['incomplete_tasks_percent'],
                t['overdue_task_percent']
            ]
            task_report_to_write.append(';'.join(str_attrs))
        task_report_file.write('\n'.join(task_report_to_write))
        print("Task report successfully added.")

    # display task report on console
    print("\n~~~~~~~~~~ Task Report ~~~~~~~~~~\n")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Incomplete tasks: {incomplete_tasks}")
    print(f"Incomplete and overdue tasks: {overdue_tasks}")
    print(f"Incomplete_tasks_percent: {round(incomplete_tasks_percent, 2)}%")
    print(f"Overdue_task_percent: {round(overdue_task_percent, 2)}%")
    print(line_marker(60))


# -- Function allows user to generate report on users.
def generate_users_report(t_list):
    """
    Function receives all task list as an argument
    """

    # -- Dictionary with usernames and passwords
    username_password = read_users()

    users = len(list(username_password))
    total_tasks = len(t_list)
    user_task = {}
    user_report_list = []

    # -- Loops through each user and each task to generate various data
    for user in username_password:
        user_total_tasks = 0
        user_total_completed_tasks = 0
        user_incomplete_task_overdue = 0
        for tasks in t_list:
            # -- Matches a user with a user registered in a task
            if user == tasks['username']:
                # -- Matching user assigned to a new variable (user_name)
                user_name = user
                # -- Increments the number of tasks assigned to a user
                user_total_tasks += 1
                if tasks['completed']:
                    # -- Increments the number of completed tasks for the user
                    user_total_completed_tasks += 1
                elif (not tasks['completed'] and
                    datetime.strptime(str(tasks['due_date'].date()), DATETIME_STRING_FORMAT) < today):
                    # -- Increments the number of incomplete and overdue tasks for the user
                    user_incomplete_task_overdue += 1

                    # -- Adding all data to user_task dictionary
                try:
                    user_task.update({"user": user_name, "user_total_tasks": user_total_tasks,
                                    "user_completed_tasks": user_total_completed_tasks,
                                      "user_total_tasks_percent": round(((user_total_tasks / total_tasks) * 100), 2),
                                    "user_completed_tasks_percent": round(
                                          ((user_total_completed_tasks / user_total_tasks) * 100), 2),
                                    "user_incomplete_tasks_percent": round(
                                          (((user_total_tasks - user_total_completed_tasks) / user_total_tasks) * 100),
                                    2),
                                    "user_incomplete_tasks_overdue_percent": round(
                                          ((user_incomplete_task_overdue / user_total_tasks) * 100), 2)})

                except ZeroDivisionError:
                    print("User not assigned to any task")

                user_report_list.append(user_task)
                user_task = {}
            else:
                continue

    # -- Writing user task data to user_overview.txt
    with open('user_overview.txt', 'w') as user_report_file:
        user_report_to_write = []
        for t in user_report_list:
            str_attrs = [
                str(t['user']),
                str(t['user_total_tasks']),
                str(t['user_completed_tasks']),
                str(t['user_total_tasks_percent']),
                str(t['user_completed_tasks_percent']),
                str(t['user_incomplete_tasks_percent']),
                str(t['user_incomplete_tasks_overdue_percent'])
            ]
            user_report_to_write.append(';'.join(str_attrs))
        user_report_file.write(str(users) + ";" + str(total_tasks) + "\n")
        user_report_file.write('\n'.join(user_report_to_write))
        print("User report successfully added.")

    headers = ["User", "Tot tasks", "Comp. tasks", "Tot tasks %", "Completed tasks %", "Incomplete task %",
            "Incomplete & Overdue %"]

    all_data = []

    for x in user_report_list:
        all_data.append(list(x.values()))

    print("\n~~~~~~~~~~ User Report ~~~~~~~~~~\n")
    print(tabulate(all_data, headers=headers))
    print()


def generate_report():
    """
    Provides user options to view task report and/or user report
    """
    task_list = read_tasks()
    report_menu = """
        Select the type of report you want to view:
            1. Tasks report
            2. Users report
            0. Return to main menu 
    :"""
    while True:
        print("~~~~~~  Report  ~~~~~~")
        user_option = input(report_menu)
        if user_option == '1':
            generate_tasks_report(task_list)
        elif user_option == '2':
            generate_users_report(task_list)
        elif user_option == '0':
            break
        else:
            print("Incorrect choice.Try again")


def menu():
    """
    Main menu where program begins once user is successfully logged on
    """
    menu_options = """Select one of the following options below:
    r  - register user
    a  - add task
    va - view all tasks
    vm - view my tasks
    gr - generate reports
    ds - display statistics
    e  - exit
    :"""

    while True:
        print("~~~~~~  Task Manager  ~~~~~~")
        user_option = input(menu_options)
        if user_option == 'r':
            reg_user()
        elif user_option == 'a':
            add_task()
        elif user_option == 'va':
            view_all_tasks()
        elif user_option == 'vm':
            view_my_task()
        elif user_option == 'gr':
            generate_report()
        elif user_option == 'ds':
            display_statistics()
        elif user_option == 'e':
            print("Goodbye!")
            break


if __name__ == '__main__':
    login()