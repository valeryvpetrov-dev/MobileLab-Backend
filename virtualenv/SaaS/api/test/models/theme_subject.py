from django.test import TestCase

from SaaS.api.models import Theme, Subject

import datetime


# Create your tests here.
class TestThemeSubject(TestCase):
    """
    CRUD operations of Theme-Subject relationship model (Many-to-one)

    Mention: Tests that require a database (namely, model tests)
    will not use your “real” (production) database.
    Separate, blank databases are created for the tests.
    """

    def setUp(self):
        self.subject = Subject.objects.create(name='Robotics')
        self.theme = Theme.objects.create(title='Theme',
                                          description='Description',
                                          date_creation=datetime.datetime.now() - datetime.timedelta(days=1),
                                          date_acceptance=datetime.datetime.now(),
                                          subject=self.subject)
        self.subject.theme_set.add(self.theme)

    def test_create_theme_subject_relationship(self):
        theme = Theme.objects.create(title='Theme1',
                                     description='Description1',
                                     date_creation=datetime.datetime.now() - datetime.timedelta(days=1),
                                     date_acceptance=datetime.datetime.now())
        theme.subject = self.subject
        self.assertEqual(Subject.objects.get(pk=self.subject.id), theme.subject)

    def test_create_subject_theme_relationship(self):
        subject = Subject.objects.create(name='Android dev')
        subject.theme_set.add(self.theme)
        self.assertIn(Theme.objects.get(pk=self.theme.id), subject.theme_set.all())

    def test_read_related_theme(self):
        self.assertIsNotNone(self.subject.theme_set.get(pk=self.theme.subject.id))

    def test_read_related_subject(self):
        self.assertIsNotNone(self.theme.subject)

    def test_update_theme(self):
        new_title = 'Theme1'
        self.theme.title = new_title
        self.theme.save()
        self.assertEqual(self.subject.theme_set.get(pk=self.theme.id).title, new_title)

    def test_update_subject(self):
        new_name = 'Robotics1'
        self.subject.name = new_name
        self.subject.save()
        self.assertEqual(self.theme.subject.name, new_name)

    def test_delete_theme(self):
        theme_id = self.theme.id
        self.theme.delete()
        with self.assertRaises(Theme.DoesNotExist):
            self.subject.theme_set.get(pk=theme_id)

    def test_delete_student(self):
        self.subject.delete()
        self.assertIsNone(self.theme.subject.id)
