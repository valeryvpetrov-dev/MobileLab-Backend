from django.db import models
from django.forms import ValidationError
from django.utils.timezone import localtime

from .base import Comment
from .theme import Theme
from .student import Student
from .curator import Curator


class SuggestionThemeStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "Suggestion_theme_status"


class SuggestionThemeProgress(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=75)
    description = models.CharField(max_length=150)
    date_update = models.DateTimeField(null=True)

    class Meta:
        db_table = "Suggestion_theme_progress"

    def save(self, *args, **kwargs):
        self.date_update = localtime()

        super().save(*args, **kwargs)


class SuggestionTheme(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, db_column='theme_id')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student_id', null=True)
    curator = models.ForeignKey(Curator, on_delete=models.CASCADE, db_column='curator_id', null=True)
    status = models.ForeignKey(SuggestionThemeStatus, on_delete=models.DO_NOTHING, db_column='status_id')
    progress = models.ForeignKey(SuggestionThemeProgress, on_delete=models.SET_NULL, db_column='progress_id', null=True, related_name="suggestion")
    date_creation = models.DateTimeField()

    class Meta:
        db_table = "Suggestion_theme"

    def save(self, *args, **kwargs):
        if self.date_creation:
            self.date_creation = localtime(self.date_creation)

        if not self.date_creation:
            self.date_creation = localtime()

        if self.date_creation > localtime():
            raise ValidationError('Date creation is in future.')
        super().save(*args, **kwargs)


class SuggestionThemeComment(Comment):
    id = models.AutoField(primary_key=True)
    suggestion = models.ForeignKey(SuggestionTheme, on_delete=models.CASCADE, db_column='suggestion_id', related_name='comment_set')

    class Meta:
        db_table = "Suggestion_theme_comment"
