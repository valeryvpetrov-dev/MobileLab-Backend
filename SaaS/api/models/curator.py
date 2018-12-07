from django.db import models

from .base import Man
from .skill import Skill


class Curator(Man):
    id = models.AutoField(primary_key=True)
    skills = models.ManyToManyField(Skill)

    class Meta:
        db_table = "Curator"
