from collections import OrderedDict
import datetime
import pdb
import os
import sys

from peewee import *

from models import Employee, Task
import helpers

DATABASE = SqliteDatabase('worklog.db')
current_menu = 0
current_emp = None
current_task = None


def delete_employee():
    """Delete Employee"""
    emp = Employee.get(Employee.id == current_emp)
    if input('Delete Employee {} {}? [Yy]: '.format(
                                        emp.fname,
                                        emp.lname)).lower() != 'n':
        next_employee()
        emp.delete_instance()


def next_employee():
    """Next Employee in list"""
    # pdb.set_trace()
    global current_emp
    duplicates = Employee.select().where(
        Employee.lname == current_emp.lname,
        Employee.fname > current_emp.fname
        )

    next_emps = Employee.select().where(Employee.lname > current_emp.lname)
    if duplicates:
        current_emp = duplicates.get()
    else:
        if next_emps:
            current_emp = next_emps.get()
        else:
            current_emp = Employee.select().get()


def previous_employee():
    """Previous Employee in list"""
    global current_emp
    duplicates = Employee.select().where(
        Employee.lname == current_emp.lname,
        Employee.fname < current_emp.fname
        )
    next_emps = (
            Employee
            .select()
            .order_by(Employee.lname.desc(), Employee.fname.desc())
            .where(Employee.lname < current_emp.lname))
    if duplicates:
        current_emp = duplicates.get()
    else:
        if next_emps:
            current_emp = next_emps.get()
        else:
            current_emp = (
                        Employee
                        .select()
                        .order_by(Employee.lname.desc()).get())


def select_employee():
    """Select Employee"""
    global current_menu
    global current_task
    current_menu = 1
    if current_emp.tasks.count():
        current_task = current_emp.tasks.get()
    else:
        print("\nThis Employee has no tasks...\n")
        if input("Would you like to add one? [Yy]").lower() != 'n':
            add_task()
            current_task = current_emp.tasks.get()


def add_employee():
    """Add an Employee"""
    fname = input("Enter employee's first name: ")
    lname = input("Enter employee's last name: ")

    if input('Save Employee? [Yy] ').lower() != 'n':
        Employee.create(fname=fname, lname=lname)
        print("Saved Successfully")


def edit_employee():
    """Edit Employee"""
    print('--------------------------------------------------------------\n')
    print('EDITING: {} {}\n'.format(current_emp.lname, current_emp.fname))
    print('--------------------------------------------------------------')
    first = input("\tfirst: ")
    last = input("\tlast: ")
    update = (
            Employee
            .update(fname=first, lname=last)
            .where(Employee.id == current_emp.id)
            )
    if input("Would you like to save the changes? [Yy] ").lower() != 'n':
        update.execute()


def initialize():
    """Create the database and the table if they don't exist."""
    global current_emp
    global current_task
    clear()
    DATABASE.connect()
    DATABASE.create_tables([Employee], safe=True)
    DATABASE.create_tables([Task], safe=True)
    if Employee.select().count() == 0:
        print(
                "There are not currently any Employees."
                "  Please add your first Employee."
                )
        add_employee()
    current_emp = Employee.get()
    if current_emp.tasks:
        current_task = current_emp.tasks.get()
    current_menu = 0


def clear():
    """Clear the screen and print the program header"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(helpers.header)


def print_employees():
    print("\nEmployees:")
    print('-----------\n')
    for employee in Employee.select():
        if employee == current_emp:
            if current_menu != 0:
                print("       {}, {}".format(employee.lname, employee.fname))
            else:
                print("    >> {}, {}".format(employee.lname, employee.fname))
            print()
            if current_emp.tasks.count() == 0:
                print("\t\t\tNo Tasks")
            else:
                print_tasks()
        else:
            print("       {}, {}".format(employee.lname, employee.fname))
        print()


def print_tasks():
    global current_task
    if current_emp.tasks:
        print('\t\t----------------------------------------------')
        print("\t\tname\t\t\t   datetime")
        print('\t\t----------------------------------------------\n')

        for task in current_emp.tasks:
            if task == current_task:
                if current_menu == 1:
                    print("\t     >> {0!s:<11s}\t\t{1!s:^10s}".format(
                                                            task.name,
                                                            task.timestamp))
                else:
                    print("\t\t{0!s:<11s}\t\t{1!s:^10s}".format(
                        task.name,
                        task.timestamp.strftime('%A %B %d, %Y %I:%M%p')))

                if current_menu == 1:
                    print_task(current_task)
            else:
                print("   ".rjust(5), end='')
                print("\t\t{0!s:<11s}\t\t{1!s:^10s}".format(
                    task.name, task.timestamp))
            print()
        print('\t\t----------------------------------------------')
    else:
        pass


def print_task(task):
    indent = "                           "
    print()
    print(indent + '='*(len(task.notes)+7))
    print(
            "{indent}Duration: {0!s:<20s}\n"
            "{indent}Notes: {1!s:<20s}".format(
                                        task.duration,
                                        task.notes,
                                        indent="                           "))
    print(indent + '='*(len(task.notes)+7))


def add_task():
    """Add a Task"""

    name = input("Enter task name: ").strip()
    duration = int(input("Enter task duration: ").strip())
    data = input("Enter task notes: ").strip()

    if data:
        if input('Save Task? [Yy] ').lower() != 'n':
            Task.create(
                        notes=data,
                        name=name,
                        employee=current_emp,
                        duration=duration
                        )

            print("Saved Successfully!")


def view_tasks(emp, search_query=None):
    """View tasks."""
    if search_query:
        tasks = tasks.where(Task.content.contains(search_query))

    for task in emp.tasks:
        timestamp = task.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        # clear()
        print('='*len(timestamp) + '\n')
        print(timestamp)
        print('\n' + '='*len(timestamp) + '\n')
        print(
            "\tName: {0!s:<20s}\n\tDuration: "
            "{1!s:<20s}\n\tNotes: {2!s:<20s}\n\tID: {2!s:<20s}".format(
                                            task.name,
                                            task.duration,
                                            task.notes,
                                            task.id))
        print('\n' + '='*len(timestamp))
        print('n) next Task')
        print('d) delete Task')
        print('q) return to main menu')

        next_action = input('Action: [nq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_Task(Task)


def search_tasks():
    """Search tasks for a string."""
    view_tasks(input('Search query: '))


def menu_loop():
    """Show the menu"""
    clear()
    choice = None
    menus = [emp_menu, task_menu]

    while choice != 'q':
        clear()
        menus[current_menu][0]()
        print('--------------------------------------------------------------')
        print()
        print("Enter 'q' to quit.")
        for key, value in menus[current_menu][1].items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('\nAction: ').lower().strip()

        if choice in menus[current_menu][1]:
            menus[current_menu][1][choice]()


def back():
    """Go Back"""
    global current_menu
    current_menu = current_menu - 1


def order_tasks():
    """Order tasks in list"""


def search_tasks():
    """Search Tasks in list"""


def edit_task():
    """Edit Task"""
    global current_task
    print('--------------------------------------------------------------\n')
    print("EDITING TASK\n")
    print('--------------------------------------------------------------')

    name = input("\tname:")
    duration = input("\tduration: ")
    notes = input("\tnotes: ")
    if name:
        current_task.name = name
    if duration:
        current_task.duration = int(duration)
    if notes:
        current_task.notes = notes
    if input("Would you like to save the changes? [Yy] ").lower() != 'n':
        current_task.save()


def delete_task():
    """Delete Task"""
    task = Task.select().where(Task.id == current_task.id).get()

    if input('Delete Task {} {}? [Yy] '.format(
            task.name,
            task.timestamp)).lower() != 'n':
        next_task()
        task.delete_instance()


def next_task():
    """Next Task"""
    global current_task
    next_task = Task.select().where(Task.timestamp < current_task.timestamp)
    if next_task:
        current_task = next_task.get()
    else:
        current_task = Task.select().get()


def previous_task():
    """Previous Task"""
    global current_task
    next_task = Task.select().where(Task.timestamp > current_task.timestamp)
    if next_task:
        current_task = next_task.select().order_by(Task.timestamp).get()
    else:
        current_task = Task.select().order_by(Task.timestamp).get()

emp_menu = (print_employees, OrderedDict([
    ('a', add_employee),
    ('e', edit_employee),
    ('d', delete_employee),
    ('n', next_employee),
    ('p', previous_employee),
    ('s', select_employee)
  ]))

task_menu = (print_employees, OrderedDict([
    ('a', add_task),
    ('e', edit_task),
    ('d', delete_task),
    ('n', next_task),
    ('p', previous_task),
    ('b', back)
]))


if __name__ == '__main__':
    initialize()
    menu_loop()
