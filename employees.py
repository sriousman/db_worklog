from peewee import *

db = SqliteDatabase('employees.db')


class Employee(Model):
    username = CharField(max_length=255, unique=True)
    fname = CharField(max_length=255, unique=False)
    lname = CharField(max_length=255, unique=False)

    class Meta:
            database = db


def add_student():
    try:
        Employee.create(
            username=employee['username'],
            fname=employee['fname'],
            lname=employee['lname'],
            )
    except IntegrityError:
        employee_record = Empoyee.get(username=employee['username'])
        employee_record.fname = employee['fname']
        employee_record.lname = employee['lname']
        employee_record.save()


def get_emps_in_order():
    """Returns the employees in alphabetical order by last name"""
    employee = Employee.select().order_by(Employee.lname)


def get_emp():
    """Returns the last employee in an alphabetical list by last name"""
    employee = Employee.select().order_by(Employee.lname.desc()).get()


if __name__ == 'main':
    db.connect()
    db.create_tables([Employee], safe=True)
