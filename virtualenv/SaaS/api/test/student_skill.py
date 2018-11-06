from django.test import TestCase

from ..models import Skill, Student, StudentSkill


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
        self.student_skill = StudentSkill.objects.create(student=self.student, skill=self.skill)

    def test_create_student_skill_relationship(self):
        skill = Skill.objects.create(name='Management')
        student_skill = StudentSkill.objects.create(student=self.student, skill=skill)
        self.assertEqual(StudentSkill.objects.all().get(id=student_skill.id).skill.name, skill.name)

    def test_create_skill_student_relationship(self):
        student = Student.objects.create(name='Valery1',
                                         last_name='Petrov1',
                                         patronymic='Vladimirovich1',
                                         description='Django backend dev1')
        skill_student = StudentSkill.objects.create(student=student, skill=self.skill)
        self.assertEqual(StudentSkill.objects.all().get(id=skill_student.id).student.name, student.name)

    def test_read_related_skill(self):
        related_skill = StudentSkill.objects.get(student_id=self.student.id).skill
        self.assertEqual(related_skill, self.skill)

    def test_read_related_student(self):
        related_student = StudentSkill.objects.get(skill_id=self.skill.id).student
        self.assertEqual(related_student, self.student)

    def test_update_skill(self):
        new_name = 'Python programming'
        self.student_skill.skill.name = new_name
        self.student_skill.skill.save()
        self.assertEqual(Skill.objects.get(pk=self.skill.id).name, new_name)

    def test_update_student(self):
        new_name = 'Valery1'
        self.student_skill.student.name = new_name
        self.student_skill.student.save()
        self.assertEqual(Student.objects.get(pk=self.student.id).name, new_name)

    def test_delete_skill(self):
        skill_id = self.student_skill.skill.id
        self.student_skill.skill.delete()
        with self.assertRaises(Skill.DoesNotExist):
            Skill.objects.get(pk=skill_id)

    def test_delete_student(self):
        student_id = self.student_skill.student.id
        self.student_skill.student.delete()
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(pk=student_id)
