from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .base import Man
from .skill import Skill


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "Group"


class Student(Man):
    id = models.AutoField(primary_key=True)
    course_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(4), MinValueValidator(1)])
    skills = models.ManyToManyField(Skill)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, db_column="group_id", null=True)

    class Meta:
        db_table = "Student"
