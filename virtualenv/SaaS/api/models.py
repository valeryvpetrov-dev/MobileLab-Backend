from django.db import models
from django.forms import ValidationError

import datetime


# base classes
class Man(models.Model):
    name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    patronymic = models.CharField(max_length=35)
    description = models.CharField(max_length=200)

    class Meta:
        abstract = True


# particular classes
class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "Skill"


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "Subject"


class Student(Man):
    id = models.AutoField(primary_key=True)
    skills = models.ManyToManyField(Skill, through='StudentSkill')

    class Meta:
        db_table = "Student"


class Curator(Man):
    id = models.AutoField(primary_key=True)
    skills = models.ManyToManyField(Skill, through='CuratorSkill')

    class Meta:
        db_table = "Curator"


class StudentSkill(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student_id')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, db_column='skill_id')

    class Meta:
        db_table = "Student_skill"


class CuratorSkill(models.Model):
    id = models.AutoField(primary_key=True)
    curator = models.ForeignKey(Curator, on_delete=models.CASCADE, db_column='curator_id')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, db_column='skill_id')

    class Meta:
        db_table = "Curator_skill"


class Theme(models.Model):
    id = models.AutoField(primary_key=True)
    curator = models.ForeignKey(Curator, on_delete=models.SET_NULL, db_column="curator_id")
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, db_column="student_id")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, db_column="subject_id")
    required_skills = models.ManyToManyField(Skill, through='ThemeSkill')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    date_creation = models.DateTimeField()
    date_acceptance = models.DateTimeField()

    class Meta:
        db_table = "Theme"

    def save(self, *args, **kwargs):
        if self.date_creation > self.date_acceptance:
            raise ValidationError(_('Date creation is greater than date acceptance.'))
        if self.date_creation > datetime.datetime.today():
            raise ValidationError(_('Date creation is in future.'))
        if self.date_acceptance > datetime.datetime.today():
            raise ValidationError(_('Date acceptance is in future.'))
        super(Theme, self).save(*args, **kwargs)


class ThemeSkill(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, db_column='theme_id')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, db_column='skill_id')

    class Meta:
        db_table = "Theme_skill"
