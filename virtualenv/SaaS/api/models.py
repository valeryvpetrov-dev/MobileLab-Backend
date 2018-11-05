from django.db import models


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
