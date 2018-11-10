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
        if self.date_creation.date() >= datetime.datetime.today().date() and \
                self.date_creation.time() > datetime.datetime.today().time():
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
        if self.date_update.date() >= datetime.datetime.today().date() and \
                self.date_update.time() > datetime.datetime.today().time():
            raise ValidationError('Date update is in future.')
        super(SuggestionThemeProgress, self).save(*args, **kwargs)


class Student(Man):
    id = models.AutoField(primary_key=True)
    skills = models.ManyToManyField(Skill)

    class Meta:
        db_table = "Student"


class Curator(Man):
    id = models.AutoField(primary_key=True)
    skills = models.ManyToManyField(Skill)

    class Meta:
        db_table = "Curator"


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


class Work(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, db_column='theme_id')
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()

    class Meta:
        db_table = "Work"

    def save(self, *args, **kwargs):
        if self.date_start.date() >= self.date_finish.date() and \
                self.date_start.time() > self.date_finish.time():
            raise ValidationError('Date start is greater than date acceptance.')
        if self.date_start.date() >= datetime.datetime.today().date() and \
                self.date_start.time() > datetime.datetime.today().time():
            raise ValidationError('Date start is in future.')
        if self.date_finish.date() >= datetime.datetime.today().date() and \
                self.date_finish.time() > datetime.datetime.today().time():
            raise ValidationError('Date finish is in future.')
        super(Work, self).save(*args, **kwargs)


class WorkStep(models.Model):
    id = models.AutoField(primary_key=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, db_column='work_id')
    status = models.ForeignKey(WorkStepStatus, on_delete=models.DO_NOTHING, db_column='status_id')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()

    class Meta:
        db_table = "Work_step"

    def save(self, *args, **kwargs):
        if self.date_start.date() >= self.date_finish.date() and \
                self.date_start.time() > self.date_finish.time():
            raise ValidationError('Date start is greater than date acceptance.')
        if self.date_start.date() >= datetime.datetime.today().date() and \
                self.date_start.time() > datetime.datetime.today().time():
            raise ValidationError('Date start is in future.')
        if self.date_finish.date() >= datetime.datetime.today().date() and \
                self.date_finish.time() > datetime.datetime.today().time():
            raise ValidationError('Date finish is in future.')
        super(WorkStep, self).save(*args, **kwargs)


class WorkStepComment(Comment):
    id = models.AutoField(primary_key=True)
    step = models.ForeignKey(WorkStep, on_delete=models.CASCADE, db_column='work_step_id')

    class Meta:
        db_table = "Work_step_comment"


class WorkStepMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    step = models.ForeignKey(WorkStep, on_delete=models.CASCADE, db_column='step_id')
    content = models.CharField(max_length=200)

    class Meta:
        db_table = "Work_step_material"


class SuggestionTheme(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, db_column='theme_id')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student_id', null=True)
    curator = models.ForeignKey(Curator, on_delete=models.CASCADE, db_column='curator_id', null=True)
    status = models.ForeignKey(SuggestionThemeStatus, on_delete=models.DO_NOTHING, db_column='status_id')
    progress = models.ForeignKey(SuggestionThemeProgress, on_delete=models.SET_NULL, db_column='progress_id', null=True)
    date_creation = models.DateTimeField()

    class Meta:
        db_table = "Suggestion_theme"

    def save(self, *args, **kwargs):
        if self.date_creation.date() >= datetime.datetime.today().date() and \
                self.date_creation.time() > datetime.datetime.today().time():
            raise ValidationError('Date creation is in future.')
        super(SuggestionTheme, self).save(*args, **kwargs)


class SuggestionThemeComment(Comment):
    id = models.AutoField(primary_key=True)
    suggestion = models.ForeignKey(SuggestionTheme, on_delete=models.CASCADE, db_column='suggestion_id')

    class Meta:
        db_table = "Suggestion_theme_comment"
