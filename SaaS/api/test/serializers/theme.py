from django.test import TestCase

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import io
from datetime import datetime, timezone, timedelta

from ...serializers.theme import ThemeSerializerRelatedID, ThemeSerializerRelatedIntermediate
from ...models.theme import Theme, Subject
from ...models.student import Student
from ...models.curator import Curator
from ...models.skill import Skill


class TestThemeSerializer(TestCase):
    """
    CRU operations of Theme serializer model

    Mention: Read, Update operations are performed by id.
             Delete operation doesn't require serialization.
    """
    def setUp(self):
        curator = Curator.objects.create(name='V', last_name='P', patronymic='V', description='D')
        student = Student.objects.create(name='V', last_name='P', patronymic='V', description='D')
        subject = Subject.objects.create(name='S')
        skill1 = Skill.objects.create(name='Skill1')
        skill2 = Skill.objects.create(name='Skill2')
        student.skills.add(skill1)
        curator.skills.add(skill2)
        theme = Theme.objects.create(title='T', description='D',
                                     date_creation=datetime.now(timezone.utc) - timedelta(days=1),
                                     date_acceptance=datetime.now(timezone.utc))
        theme.curator = curator
        theme.student = student
        theme.subject = subject
        theme.skills.add(skill1)
        theme.skills.add(skill2)

        self.theme = theme
        self.theme_id = theme.id  # RUD

    def test_create_theme_by_curator(self):  # input - json
        theme_bin = b'{"title":"T","description":"D","date_creation":"2018-11-09T18:17:25.473086Z","date_acceptance":"2018-11-10T18:17:25.473086Z","curator":1}'
        stream = io.BytesIO(theme_bin)
        data = JSONParser().parse(stream)  # returns dict
        serializer = ThemeSerializerRelatedID(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            theme = serializer.create(serializer.validated_data)
            self.assertIsNotNone(theme.id)

    def test_create_theme_by_student(self):
        theme_bin = b'{"title":"T","description":"D","date_creation":"2018-11-09T18:17:25.473086Z","date_acceptance":"2018-11-10T18:17:25.473086Z","student":1}'
        stream = io.BytesIO(theme_bin)
        data = JSONParser().parse(stream)  # returns dict
        serializer = ThemeSerializerRelatedID(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            theme = serializer.create(serializer.validated_data)
            self.assertIsNotNone(theme.id)

    def test_create_theme_with_curator_student(self):
        theme_bin = b'{"title":"T","description":"D","date_creation":"2018-11-09T18:17:25.473086Z","date_acceptance":"2018-11-10T18:17:25.473086Z","curator":1,"student":1}'
        stream = io.BytesIO(theme_bin)
        data = JSONParser().parse(stream)  # returns dict
        serializer = ThemeSerializerRelatedID(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            theme = serializer.create(serializer.validated_data)
            self.assertIsNotNone(theme.id)

    def test_create_theme_with_subject(self):
        theme_bin = b'{"title":"T","description":"D","date_creation":"2018-11-09T18:17:25.473086Z","date_acceptance":"2018-11-10T18:17:25.473086Z","curator":1,"subject":1}'
        stream = io.BytesIO(theme_bin)
        data = JSONParser().parse(stream)  # returns dict
        serializer = ThemeSerializerRelatedID(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            theme = serializer.create(serializer.validated_data)
            self.assertIsNotNone(theme.id)

    def test_create_theme_with_skills(self):
        theme_bin = b'{"title":"T","description":"D","date_creation":"2018-11-09T18:17:25.473086Z","date_acceptance":"2018-11-10T18:17:25.473086Z","curator":1,"skills":[1,2]}'
        stream = io.BytesIO(theme_bin)
        data = JSONParser().parse(stream)  # returns dict
        serializer = ThemeSerializerRelatedID(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            theme = serializer.create(serializer.validated_data)
            self.assertIsNotNone(theme.id)

    def test_create_theme_with_all_related(self):
        theme_bin = b'{"title":"T","description":"D","date_creation":"2018-11-09T18:17:25.473086Z","date_acceptance":"2018-11-10T18:17:25.473086Z","curator":1,"student":1,"subject":1,"skills":[1,2]}'
        stream = io.BytesIO(theme_bin)
        data = JSONParser().parse(stream)  # returns dict
        serializer = ThemeSerializerRelatedID(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            theme = serializer.create(serializer.validated_data)
            self.assertIsNotNone(theme.id)

    def test_create_theme_without_related(self):
        theme_bin = b'{"title":"T","description":"D","date_creation":"2018-11-09T18:17:25.473086Z","date_acceptance":"2018-11-10T18:17:25.473086Z"}'
        stream = io.BytesIO(theme_bin)
        data = JSONParser().parse(stream)  # returns dict
        serializer = ThemeSerializerRelatedID(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            theme = serializer.create(serializer.validated_data)
            self.assertIsNotNone(theme.id)

    def test_read_theme_with_all_related_ids(self):  # output - json
        serializer = ThemeSerializerRelatedID(self.theme)
        json = JSONRenderer().render(serializer.data)
        print(json)
        self.assertIsNotNone(json)

    def test_read_theme_with_all_related_intermediate(self):  # output - json
        serializer = ThemeSerializerRelatedIntermediate(self.theme)
        json = JSONRenderer().render(serializer.data)
        print(json)
        self.assertIsNotNone(json)

    def test_update_student_with_skills_id(self):  # input - json
        new_skill_name = "Skill3"
        Skill.objects.create(name=new_skill_name)
        theme_bin = b'{"title":"Title","description":"D","date_creation":"2018-11-09T19:18:10.046382Z","date_acceptance":"2018-11-10T19:18:10.046382Z","curator":1,"student":1,"subject":1,"skills":[1,2,3]}'
        stream = io.BytesIO(theme_bin)
        data = JSONParser().parse(stream)
        serializer = ThemeSerializerRelatedID(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            theme = Theme.objects.get(pk=self.theme_id)
            theme = serializer.update(theme, serializer.validated_data)
            if theme.id == self.theme_id and theme.title == 'Title':
                self.assertEqual(len(theme.skills.all()), 3)
