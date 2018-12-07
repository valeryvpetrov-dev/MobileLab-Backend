from django.test import TestCase

from ...models.skill import Skill

# Create your tests here.
class TestSkill(TestCase):
    """
    CRUD operations of Skill model

    Mention: Tests that require a database (namely, model tests)
    will not use your “real” (production) database.
    Separate, blank databases are created for the tests.
    """
    def setUp(self):
        Skill.objects.create(name='Programming')

    def test_create_skill(self):
        skill = Skill.objects.create(name='Management')
        self.assertIsNotNone(skill)

    def test_read_skill(self):
        skill = Skill.objects.get(name__exact='Programming')
        self.assertIsNotNone(skill)

    def test_update_skill(self):
        new_name = 'Python programming'
        old_skill = Skill.objects.get(name__exact='Programming')
        old_skill_id = old_skill.id

        Skill.objects.filter(name__exact='Programming').update(name=new_name)
        new_skill = Skill.objects.get(id=old_skill_id)
        self.assertEqual(new_skill.name, new_name)

    def test_delete_skill(self):
        Skill.objects.get(name__exact='Programming').delete()
        with self.assertRaises(Skill.DoesNotExist):
            Skill.objects.get(name__exact='Programming')
