#!/usr/bin/env python 3

from collections import OrderedDict
import datetime
import sys

from peewee import *

db = db = SqliteDatabase('worklogger.db')

menu = OrderedDict([
    ('a', add_task),
    ('v', view_tasks),
    ('f', find_task),
    ('e', edit_task),
    ('d', delete_task)
])


class Person(Model):
    """Base Model for any person.

    Attributes:
    fname - first name of the person
    lname - last name of the person
    id_num - a unique hash for identifying the person
    dob - the person's date of birth"""

    fname = CharField(max_length=30, unique=False)
    lname = CharField(max_length=50, unique=False)
    # id_num =
    dob = DateTimeField()

    class Meta:
        database = db


class Employee(Person):
    """Inherits from Person.

    Attributes:
    fname - first name of the person
    lname - last name of the person
    id_num - a unique hash for identifying the person
    dob - the person's date of birth"""

    fname = CharField(max_length=30, unique=False)
    lname = CharField(max_length=50, unique=False)
    id_num = PrimaryKeyField()
    dob = DateField()

    class Meta:
        database = db


class Task(Model):
    # task_id - unique key
    name = CharField(max_length=100, unique=False)
    created_at = DateTimeField(datetime.datetime.now)
    notes = TextField()
    owner = ForeignKeyField(Employee)
    # duration
    # created_at
    # duration
    # started_at
    # completed_at

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they dont exist"""
    db.connect()
    db.create_tables([Task], safe=True)


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            menu[choice]()


def add_task():
    """Add a task"""
    print("Enter a task name. Press ctrl+d when finished.")
    data = sys.stdin.read().strip()

    if data:
        if input('Save task? [Yn] ').lower() != 'n':
            Entry.create(name=data)
            print("Saved a task")


def view_tasks():
    """View tasks"""


def edit_task():
    """Edit a task"""


def delete_task(task):
    """Delete a task"""


if __name__ == '__main__':
    initialize()
    menu_loop()
