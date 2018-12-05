from django.test import TestCase

from ...models.student import Student
from ...models.skill import Skill


# Create your tests here.
class TestStudentSkill(TestCase):
    """
    CRUD operations of Student-Skill relationship model (Many-to-many)

    Mention: Tests that require a database (namely, model tests)
    will not use your “real” (production) database.
    Separate, blank databases are created for the tests.
    """

    def setUp(self):
        self.skill = Skill.objects.create(name='Programming')
        self.student = Student.objects.create(name='Valery',
                                              last_name='Petrov',
                                              patronymic='Vladimirovich',
                                              description='Django backend dev')
        self.student.skills.add(self.skill)

    def test_create_student_skill_relationship(self):
        skill = Skill.objects.create(name='Management')
        self.student.skills.add(skill)
        self.assertIsNotNone(Skill.objects.get(pk=skill.id).student_set.get(pk=self.student.id))

    def test_create_skill_student_relationship(self):
        student = Student.objects.create(name='Valery1',
                                         last_name='Petrov1',
                                         patronymic='Vladimirovich1',
                                         description='Django backend dev1')
        self.skill.student_set.add(student)
        self.assertIsNotNone(Student.objects.get(pk=student.id).skills.get(pk=self.skill.id))

    def test_read_related_skill(self):
        self.assertIsNotNone(self.student.skills.get(pk=self.skill.id))

    def test_read_related_student(self):
        self.assertIsNotNone(self.skill.student_set.get(pk=self.student.id))

    def test_update_skill(self):
        new_name = 'Python programming'
        self.skill.name = new_name
        self.skill.save()
        self.assertEqual(self.student.skills.get(pk=self.skill.id).name, new_name)

    def test_update_student(self):
        new_name = 'Valery1'
        self.student.name = new_name
        self.student.save()
        self.assertEqual(self.skill.student_set.get(pk=self.student.id).name, new_name)

    def test_delete_skill(self):
        skill_id = self.skill.id
        self.student.skills.get(pk=skill_id).delete()
        with self.assertRaises(Skill.DoesNotExist):
            Skill.objects.get(pk=skill_id)

    def test_delete_student(self):
        student_id = self.student.id
        self.skill.student_set.get(pk=student_id).delete()
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(pk=student_id)
