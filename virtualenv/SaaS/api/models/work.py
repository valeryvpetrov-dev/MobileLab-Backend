from django.db import models
from django.forms import ValidationError

from .base import Comment
from .theme import Theme

import datetime


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


class WorkStepStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "Work_step_status"


class WorkStep(models.Model):
    id = models.AutoField(primary_key=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, db_column='work_id', related_name='step_set')
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
    step = models.ForeignKey(WorkStep, on_delete=models.CASCADE, db_column='work_step_id', related_name='comment_set')

    class Meta:
        db_table = "Work_step_comment"


class WorkStepMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    step = models.ForeignKey(WorkStep, on_delete=models.CASCADE, db_column='step_id', related_name='material_set')
    content = models.CharField(max_length=200)

    class Meta:
        db_table = "Work_step_material"