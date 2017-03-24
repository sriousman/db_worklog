# unittests.py
import unittest
import models
import wl


class TaskTests(unittest.TestCase):
    def setUp(self):
        """create test db"""
        pass

    def test_creation(self):
        """test task creation"""
        pass

    def test_edit(self):
        """test edit and update of task"""
        pass

    def test_next(self):
        """test the next function when in the task menu"""
        pass

    def test_previous(self):
        """test the previous function when in the task menu"""
        pass

    def test_delete(self):
        """test task destruction"""
        pass


class EmpTests(unittest.TestCase):
    def setUp(self):
        """create test db"""
        pass

    def test_creation(self):
        """test creation of a new employee row"""
        pass

    def test_edit(self):
        """test edit and update of employee record"""
        pass

    def test_next(self):
        """test the next function when in the emp menu"""
        pass

    def test_previous(self):
        """test the previous function when in the emp menu"""
        pass

    def test_delete(self):
        """test emp destruction and the task destruction that comes with it"""
        pass


class MenuTests(unittest.TestCase):
        def setUp(self):
            """create test db"""
            pass

        def test_menu_change(self):
            """test menu changes during selection and back"""
            pass

if __name__ == '__main__':
    unittest.main()
