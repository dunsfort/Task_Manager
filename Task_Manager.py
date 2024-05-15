#!/usr/bin/env python
# coding: utf-8

# In[2]:


import datetime 
import getpass 
import os.path

# Function to load user data from user.txt into a dictionary
def load_user_data():
    user_data = {}
    if os.path.exists("user.txt"):
        with open("user.txt", "r") as doc:
            for line in doc:
                username, password = line.strip().split(", ")
                user_data[username] = password
    return user_data

# Function to print menu options based on user's role
def print_options(is_admin):
    print("\nOptions:")
    if is_admin:
        print("r - register a user")
        print("s - display statistics")
        print("va - view all tasks")
    else:
        print("a - add task")
        print("va - view all tasks")
        print("vm - view my tasks")
    print("e - exit\n")

# Function to validate date format
def validate_date(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Load user data
user_data = load_user_data()

# Validate login credentials
while True:
    username = input("\nEnter your username: ")
    password = getpass.getpass("Enter your password: ")
    if username in user_data and password == user_data[username]:
        print("Login successful!")
        is_admin = username == 'admin'
        break
    else:
        print("Invalid username or password. Please try again")

# Variables to store task and user statistics 
task_count = 0
user_count = len(user_data)

# Count the number of tasks in tasks.txt
if os.path.exists("tasks.txt"):
    with open("tasks.txt", "r") as file:
        task_count = sum(1 for line in file)

# Main menu loop
while True:
    print_options(is_admin)
    choice = input("Select an option: ").lower()

    if is_admin: 
        if choice == 'r':
            new_username = input("\nEnter a new username: ")
            new_password = input("Enter a new password: ")
            password_confirmation = input("Confirm your password: ")
            if new_password == password_confirmation:    
                with open("user.txt", "a") as file:
                    file.write(f"\n{new_username}, {new_password}")
                print("User successfully added to user.txt!")
                user_count += 1 
            else:
                print("Password confirmation does not match. User not added.")

        elif choice == 's':
            print("-" * 50)
            print(f"Total number of users: {user_count}")
            print(f"Total number of tasks: {task_count}")
            print("-" * 50)

    else:
        if choice == 'a':
            assigned_to = input("\nEnter the user the task is assigned to: ")
            title = input("Enter the title of the task: ")
            description = input("Enter the description of the task: ")  

            while True:
                due_date = input("Enter the due date of the task (YYYY-MM-DD): ")
                if validate_date(due_date):
                    break
                else:
                    print("Invalid date format. Please enter in YYYY-MM-DD format.")

            current_date = datetime.datetime.today()
            with open("tasks.txt", "a") as file:
                file.write(f"\n{assigned_to}, {title}, {description}, {due_date}, No, {current_date}") 
            task_count += 1
            print("Task successfully added to tasks.txt!")

        elif choice == 'va':
            if os.path.exists("tasks.txt"):
                with open("tasks.txt", "r") as file:
                    for line in file:
                        task_data = line.strip().split(",")
                        if len(task_data) == 6:
                            assigned_to, title, description, due_date, status, creation_date = task_data
                            print(f"Assigned to : {assigned_to}") 
                            print(f"Task: {title}")
                            print(f"Description: {description}")
                            print(f"Due Date: {due_date}")
                            print(f"Status: {'Complete' if status.strip().lower() == 'yes' else 'Not completed'}")
                            print(f"Date Created: {creation_date}")
                            print("-" * 50)

        elif choice == 'vm':
            current_user = username
            found_tasks = False
            print("Username:", username)
            if os.path.exists("tasks.txt"):
                with open("tasks.txt", "r") as file:
                    tasks = file.readlines()
                for line in tasks:
                    task_data = line.strip().split(",") 
                    if len(task_data) == 6:
                        assigned_to, title, description, due_date, status, creation_date = task_data 
                        if assigned_to == current_user:
                            found_tasks = True 
                            print(f"Assigned to : {assigned_to}") 
                            print(f"Task: {title}")
                            print(f"Description: {description}")
                            print(f"Due Date: {due_date}")
                            print(f"Status: {'Complete' if status.strip().lower() == 'yes' else 'Not completed'}")
                            print(f"Date Created: {creation_date}")
                            print("-" * 50)
                if not found_tasks:
                    print("No tasks assigned to you")

    if choice == 'e':
        print('Goodbye!')
        break

