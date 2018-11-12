from django.db import models
from django.forms import ValidationError

from .curator import Curator
from .student import Student
from .skill import Skill

import datetime


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "Subject"


class Theme(models.Model):
    id = models.AutoField(primary_key=True)
    curator = models.ForeignKey(Curator, on_delete=models.SET_NULL, db_column="curator_id", null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, db_column="student_id", null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, db_column="subject_id", null=True)
    skills = models.ManyToManyField(Skill)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    date_creation = models.DateTimeField()
    date_acceptance = models.DateTimeField()

    class Meta:
        db_table = "Theme"

    def save(self, *args, **kwargs):
        if self.date_creation.date() >= self.date_acceptance.date() and \
                self.date_creation.time() > self.date_acceptance.time():
            raise ValidationError('Date creation is greater than date acceptance.')
        if self.date_creation.date() >= datetime.datetime.today().date() and \
                self.date_creation.time() > datetime.datetime.today().time():
            raise ValidationError('Date creation is in future.')
        if self.date_acceptance.date() >= datetime.datetime.today().date() and \
                self.date_acceptance.time() > datetime.datetime.today().time():
            raise ValidationError('Date acceptance is in future.')
        super(Theme, self).save(*args, **kwargs)
