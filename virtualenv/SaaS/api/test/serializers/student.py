from django.test import TestCase

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import io

from ...serializers import StudentSerializerNoSkills, StudentSerializerSkillsID, StudentSerializerSkillsIntermediate
from ...models import Student, Skill


class TestStudentSerializer(TestCase):
    """
    CRU operations of Student serializer model

    Mention: Read, Update operations are performed by id.
             Delete operation doesn't require serialization.
    """
    def setUp(self):
        skill1 = Skill.objects.create(name='Skill1')
        skill2 = Skill.objects.create(name='Skill2')
        student = Student.objects.create(name='Valery',
                                         last_name='Petrov',
                                         patronymic='Vladimirovich',
                                         description='Django backend dev')
        student.skills.add(skill1)
        student.skills.add(skill2)
        self.student = student
        self.student_id = student.id  # RUD
        self.skills_id = [skill1.id, skill2.id]

    def test_create_student_with_skills(self):  # input - json
        student_bin = b'{"name":"V","last_name":"P","patronymic":"P","description":"D","skills":[1,2]}'
        stream = io.BytesIO(student_bin)
        data = JSONParser().parse(stream)  # returns dict
        serializer = StudentSerializerSkillsID(data=data)
        if serializer.is_valid():
            student = serializer.save()
            self.assertIsNotNone(student.id)

    def test_create_student_without_skills(self):  # input - json
        student_bin = b'{"name":"V","last_name":"P","patronymic":"P","description":"D","skills":[]}'
        stream = io.BytesIO(student_bin)
        data = JSONParser().parse(stream)  # returns dict
        serializer = StudentSerializerSkillsID(data=data)
        if serializer.is_valid():
            student = serializer.save()
            self.assertIsNotNone(student.id)

    def test_read_student_with_skills_id(self):  # output - json
        serializer = StudentSerializerSkillsID(self.student)
        json = JSONRenderer().render(serializer.data)
        print(json)
        self.assertIsNotNone(json)

    def test_read_student_with_skills_intermediate(self):  # output - json
        serializer = StudentSerializerSkillsIntermediate(self.student)
        json = JSONRenderer().render(serializer.data)
        print(json)
        self.assertIsNotNone(json)

    def test_read_student_without_skills(self):  # output - json
        serializer = StudentSerializerNoSkills(self.student)
        json = JSONRenderer().render(serializer.data)
        print(json)
        self.assertIsNotNone(json)

    def test_update_student_with_skills_id(self):  # input - json
        new_skill_name = "Skill3"
        Skill.objects.create(name=new_skill_name)
        student_json = b'{"name":"V","last_name":"P","patronymic":"P","description":"D","skills":[1,2,3]}'
        stream = io.BytesIO(student_json)
        data = JSONParser().parse(stream)
        serializer = StudentSerializerSkillsID(data=data)
        if serializer.is_valid():
            student = Student.objects.get(pk=self.student_id)  # skill to update
            student = serializer.update(student, serializer.validated_data)
            if student.id == self.student_id and student.name == 'V':
                self.assertEqual(len(student.skills.all()), 3)
