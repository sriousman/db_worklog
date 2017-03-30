# unittests.py
import unittest
from playhouse.test_utils import test_database
from peewee import *
from models import Task, Employee
import wl

test_db = SqliteDatabase(':memory:')


class TaskTests(unittest.TestCase):
    def create_test_data(self):
        """create test db"""
        emps = [
            Employee.create(fname='Greg', lname='Covington'),
            Employee.create(fname='Greg', lname='Covington'),
            Employee.create(fname='Jeff', lname='Covington')
            ]
        for emp in emps:
            for i in range(10):
                Task.create(
                            name='task-%d' % i,
                            duration=30+i,
                            notes='This is task %d' % i,
                            employee=emp
                            )

    def test_creation(self):
        """test task creation"""
        with test_database(test_db, (Employee, Task)):
            # This data will be created in 'test_db'
            self.create_test_data()

            self.assertEqual(
                Employee.select().get().tasks.get().name, 'task-9')

    def test_edit_task(self):
        """test edit and update of task"""
        with test_database(test_db, (Employee, Task)):
            # This data will be created in 'test_db'
            self.create_test_data()
            task = Task.select().where(Task.name == 'task-9').get()
            task.duration = 45
            task.save()
            self.assertEqual(task.duration, 45)

    def test_next(self):
        """test the next function when in the task menu"""
        with test_database(test_db, (Employee, Task)):
            # This data will be created in 'test_db'
            self.create_test_data()
            task = Task.get()
            wl.current_task = task
            wl.next_task()
            self.assertNotEqual(wl.current_task.id, task.id)
            self.assertEqual(wl.current_task.id, task.id-1)

    def test_previous(self):
        """test the previous function when in the task menu"""
        with test_database(test_db, (Employee, Task)):
            # This data will be created in 'test_db'
            self.create_test_data()
            task = Task.get()
            wl.current_task = task
            wl.previous_task()
            self.assertNotEqual(wl.current_task.id, task.id)
            self.assertEqual(wl.current_task.id, 1)

    def test_delete_task(self):
        """test task destruction"""
        with test_database(test_db, (Employee, Task)):
            # This data will be created in 'test_db'
            self.create_test_data()
            task = Task.get(id=1)
            wl.current_task = task
            wl.delete_task()
            with self.assertRaises(Exception):
                Task.get(id=1).delete_instance()


class EmpTests(unittest.TestCase):
    def create_test_data(self):
        """create test db"""
        emps = [
            Employee.create(fname='Greg', lname='Covington'),
            Employee.create(fname='John', lname='Covington'),
            Employee.create(fname='Jeff', lname='Dovington')
            ]
        for emp in emps:
            for i in range(10):
                Task.create(
                            name='task-%d' % i,
                            duration=30+i,
                            notes='This is task %d' % i,
                            employee=emp
                            )

    def test_employee_creation(self):
        """test creation of a new employee row"""
        with test_database(test_db, (Employee, Task)):
            # This data will be created in 'test_db'
            self.create_test_data()
            self.assertTrue(Employee.get())

    def test_edit_employee(self):
        """test edit and update of employee record"""
        pass

    def test_next_employee(self):
        """test the next function when in the emp menu"""
        with test_database(test_db, (Employee, Task)):
            # This data will be created in 'test_db'
            self.create_test_data()
            emp = Employee.get()
            wl.current_emp = Employee.get()
            wl.next_employee()
            self.assertNotEqual(wl.current_emp.id, emp.id)
            self.assertEqual(wl.current_emp.id, 2)

    def test_previous_employee(self):
        """test the previous function when in the emp menu"""
        with test_database(test_db, (Employee, Task)):
            # This data will be created in 'test_db'
            self.create_test_data()
            emp = Employee.get()
            wl.current_emp = Employee.get()
            wl.previous_employee()
            self.assertEqual(wl.current_emp.id, 3)
            wl.previous_employee()
            self.assertEqual(wl.current_emp.id, 2)

    def test_delete(self):
        """test emp destruction and the task destruction that comes with it"""
        pass


class MenuTests(unittest.TestCase):
    def setUp(self):
        """create test db"""
        pass

    def test_back(self):
        """test menu changes during selection and back"""
        pass

if __name__ == '__main__':
    unittest.main()
