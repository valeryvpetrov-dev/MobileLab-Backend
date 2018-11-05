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


class Comment(models.Model):
    author_name = models.CharField(max_length=35)
    content = models.CharField(max_length=200)
    date_creation = models.DateTimeField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.date_creation > datetime.datetime.today():
            raise ValidationError('Date creation is in future.')
        super(Comment, self).save(*args, **kwargs)


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


class WorkStepStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "Work_step_status"


class SuggestionThemeStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "Suggestion_theme_status"


class SuggestionThemeProgress(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=75)
    description = models.CharField(max_length=150)
    date_update = models.DateTimeField()

    class Meta:
        db_table = "Suggestion_theme_progress"

    def save(self, *args, **kwargs):
        if self.date_update > datetime.datetime.today():
            raise ValidationError('Date update is in future.')
        super(SuggestionThemeProgress, self).save(*args, **kwargs)


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
            raise ValidationError('Date creation is greater than date acceptance.')
        if self.date_creation > datetime.datetime.today():
            raise ValidationError('Date creation is in future.')
        if self.date_acceptance > datetime.datetime.today():
            raise ValidationError('Date acceptance is in future.')
        super(Theme, self).save(*args, **kwargs)


class ThemeSkill(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, db_column='theme_id')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, db_column='skill_id')

    class Meta:
        db_table = "Theme_skill"


class Work(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, db_column='theme_id')
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()

    class Meta:
        db_table = "Work"

    def save(self, *args, **kwargs):
        if self.date_start > self.date_finish:
            raise ValidationError('Date start is greater than date finish.')
        if self.date_start > datetime.datetime.today():
            raise ValidationError('Date start is in future.')
        if self.date_finish > datetime.datetime.today():
            raise ValidationError('Date finish is in future.')
        super(Work, self).save(*args, **kwargs)


class WorkStep(models.Model):
    id = models.AutoField(primary_key=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, db_column='work_id')
    status = models.ForeignKey(WorkStepStatus, on_delete=models.SET_NULL, db_column='status_id')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()

    class Meta:
        db_table = "Work_step"

    def save(self, *args, **kwargs):
        if self.date_start > self.date_finish:
            raise ValidationError('Date start is greater than date finish.')
        if self.date_start > datetime.datetime.today():
            raise ValidationError('Date start is in future.')
        if self.date_finish > datetime.datetime.today():
            raise ValidationError('Date finish is in future.')
        super(WorkStep, self).save(*args, **kwargs)


class WorkStepComment(Comment):
    id = models.AutoField(primary_key=True)
    work_step = models.ForeignKey(WorkStep, on_delete=models.CASCADE, db_column='work_step_id')

    class Meta:
        db_table = "Work_step_comment"


class WorkStepMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    work_step = models.ForeignKey(WorkStep, on_delete=models.CASCADE, db_column='work_step_id')
    content = models.CharField(max_length=200)

    class Meta:
        db_table = "Work_step_material"


class SuggestionTheme(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, db_column='theme_id')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student_id')
    curator = models.ForeignKey(Curator, on_delete=models.CASCADE, db_column='curator_id')
    status = models.ForeignKey(SuggestionThemeStatus, on_delete=models.SET_NULL, db_column='status_id')
    progress = models.ForeignKey(SuggestionThemeProgress, on_delete=models.SET_NULL, db_column='suggestion_theme_progress_id')
    date_creation = models.DateTimeField()

    class Meta:
        db_table = "Suggestion_theme"

    def save(self, *args, **kwargs):
        if self.date_creation > datetime.datetime.today():
            raise ValidationError('Date creation is in future.')
        super(SuggestionTheme, self).save(*args, **kwargs)


class SuggestionThemeComment(models.Model):
    id = models.AutoField(primary_key=True)
    suggestion_theme = models.ForeignKey(SuggestionTheme, on_delete=models.CASCADE, db_column='suggestion_theme_id')

    class Meta:
        db_table = "Suggestion_theme_comment"
