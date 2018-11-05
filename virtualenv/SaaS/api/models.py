from django.db import models

# base classes
class Man(models.Model):
    name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    patronymic = models.CharField(max_length=35)
    description = models.CharField(max_length=200)

    class Meta:
        abstract = True

class Student(Man):
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "Student"

class Curator(Man):
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "Curator"