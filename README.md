Project name: task_manager

Description: task_manager is a project that holds multiple files such as task_manager.py, tasks.txt, user.txt, task_overview.txt and user_overview.txt.
             task_manager.py enables a user to register users, add(assign) tasks to users, view ones tasks, view all tasks, generate reports and view statistics.
             All the text files function as databases to store data (username & password on users (user.txt), tasks assigned to users (tasks.txt), all transactions
             on tasks (task_overview.txt) such as due date, completed and incomplete tasks and all transactions on users (user_overview) such as numbers percentage of 
             their completed or incompleted tasks.

Table of contents:
   Function             Usage                                   Note
1. menu                 Menu - program starter                  Holds all primary options (register user, add task, view my task, view all tasks, generate report and view statistics
2. login                To authenticate users                   Unregistered users not allowed to login
3. admin_privilege      To authenticate admin                   Features that are restricted to admin usage only
4. reg_user             To register users                       Needs admin privilege, calls check_duplicate_user function to check duplicity
5. add_task             To add tasks                            Indexed task added with user assignee, due date, assigned date and completion of task included & read and write to text files 
6. update_task          To update tasks                         Updates tasks for completion, change due date or change assigned user, updates text files
7. display_statistics   To show statistics on user and tasks    Available only for admin
8. generate_report      Generated report on users and tasks     Report on user (total tasks assigned to user, user's number of complete, incomplete tasks and percentages)
                                                                Report on tasks (total tasks, completed, incomplete tasks and overdue tasks)


Installation: To use this project you will need to install on your computer Visual Studio Code or Pycharm or other IDE for Python.
              Install tabulate using pip command in command prompt:  pip install tabulate

Usgae section: check screenshots in this repository for more information
           
