from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])

    class Meta:
        db_table = "Skill"
