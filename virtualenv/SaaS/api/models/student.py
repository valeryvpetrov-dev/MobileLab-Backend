from django.db import models

from .base import Man
from .skill import Skill


class Student(Man):
    id = models.AutoField(primary_key=True)
    skills = models.ManyToManyField(Skill)

    class Meta:
        db_table = "Student"
