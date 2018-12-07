from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

from datetime import datetime, timezone


class Man(models.Model):
    credentials = models.OneToOneField(User, on_delete=models.CASCADE)
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
        if self.date_creation > datetime.now(timezone.utc):
            raise ValidationError('Date creation is in future.')
        super(Comment, self).save(*args, **kwargs)
