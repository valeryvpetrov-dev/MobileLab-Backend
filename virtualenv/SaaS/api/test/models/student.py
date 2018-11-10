from django.test import TestCase

from SaaS.api.models import Student


# Create your tests here.
class TestStudent(TestCase):
    """
    CRUD operations of Student model

    Mention: Tests that require a database (namely, model tests)
    will not use your “real” (production) database.
    Separate, blank databases are created for the tests.
    """
    def setUp(self):
        Student.objects.create(name='Valery',
                               last_name='Petrov',
                               patronymic='Vladimirovich',
                               description='Django backend dev')

    def test_create_student(self):
        student = Student.objects.create(name='Valery1',
                                         last_name='Petrov1',
                                         patronymic='Vladimirovich1',
                                         description='Django backend dev1')
        self.assertIsNotNone(student)

    def test_read_student(self):
        student = Student.objects.get(name__exact='Valery')
        self.assertIsNotNone(student)

    def test_update_student(self):
        new_description = 'Django backend dev, unittest'
        Student.objects.filter(name__exact='Valery').update(description=new_description)
        student = Student.objects.get(name__exact='Valery')
        self.assertEqual(student.description, new_description)

    def test_delete_student(self):
        Student.objects.get(name__exact='Valery').delete()
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(name__exact='Valery')
