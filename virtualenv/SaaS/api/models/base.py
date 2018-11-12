from django.db import models
from django.forms import ValidationError

import datetime


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
