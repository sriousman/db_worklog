# models.py

import datetime
from peewee import *

DATABASE = SqliteDatabase('worklog.db')


class Employee(Model):
    fname = CharField(max_length=100, unique=False)
    lname = CharField(max_length=100, unique=False)

    class Meta:
        database = DATABASE
        order_by = ('lname', 'fname')


class Task(Model):
    name = CharField(max_length=100, unique=False)
    notes = TextField()
    employee = ForeignKeyField(Employee, related_name='tasks')
    duration = IntegerField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = '-timestamp',
