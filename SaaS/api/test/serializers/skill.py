from django.test import TestCase

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import io

from ...serializers.skill import SkillSerializer
from ...models.skill import Skill


class TestSkillSerializer(TestCase):
    """
    CRU operations of Skill serializer model

    Mention: Read, Update operations are performed by id.
             Delete operation doesn't require serialization.
    """
    def setUp(self):
        skill = Skill.objects.create(name='Serializers test')
        self.skill_id = skill.id   # RUD

    def test_create_skill(self):    # input - json
        skill_json = b'{"name":"Writing tests"}'    # bytes
        stream = io.BytesIO(skill_json)
        data = JSONParser().parse(stream)   # returns dict
        serializer = SkillSerializer(data=data)
        if serializer.is_valid():
            skill = serializer.save()
            self.assertIsNotNone(skill.id)

    def test_read_skill(self):  # output - json
        skill = Skill.objects.get(pk=self.skill_id)
        serializer = SkillSerializer(skill)
        json = JSONRenderer().render(serializer.data)
        self.assertIsNotNone(json)

    def test_update_skill(self):    # input - json
        new_name = "Writing tests Django"
        skill_json = b'{"name": "Writing tests Django"}'
        stream = io.BytesIO(skill_json)
        data = JSONParser().parse(stream)
        serializer = SkillSerializer(data=data)
        if serializer.is_valid():
            skill = Skill.objects.get(pk=self.skill_id) # skill to update
            skill = serializer.update(skill, serializer.validated_data)
            self.assertEqual(skill.name, new_name)
