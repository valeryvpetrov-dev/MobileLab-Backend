from rest_framework import serializers

from ..models.suggestion import *

from .theme import ThemeSerializerNoSkills
from .student import StudentSerializerNoSkills
from .curator import CuratorSerializerNoSkills


# GET
class SuggestionThemeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionThemeStatus
        fields = ('id', 'name')


# GET, PUT
class SuggestionThemeProgressSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    date_update = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SuggestionThemeProgress
        fields = ('id', 'title', 'description', 'date_update')


class SuggestionThemeSerializerRelatedID(serializers.ModelSerializer):
    theme_id = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), allow_null=False, required=True, source="theme")
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), allow_null=False, required=True, source="student")
    curator_id = serializers.PrimaryKeyRelatedField(queryset=Curator.objects.all(), allow_null=False, required=True, source="curator")
    status_id = serializers.PrimaryKeyRelatedField(queryset=SuggestionThemeStatus.objects.all(), allow_null=False, required=True, source="status")
    progress_id = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True, source="progress")

    class Meta:
        model = SuggestionTheme
        fields = ('id', 'theme_id', 'student_id', 'curator_id', 'status_id', 'progress_id')


# POST
class SuggestionThemeSerializerRelatedIDNoProgress(serializers.ModelSerializer):
    theme_id = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), allow_null=False, required=True, source="theme")
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), allow_null=False, required=True, source="student")
    curator_id = serializers.PrimaryKeyRelatedField(queryset=Curator.objects.all(), allow_null=False, required=True, source="curator")
    status_id = serializers.PrimaryKeyRelatedField(queryset=SuggestionThemeStatus.objects.all(), allow_null=False, required=False, source="status")

    class Meta:
        model = SuggestionTheme
        fields = ('id', 'theme_id', 'student_id', 'curator_id', 'status_id')


# PUT
class SuggestionThemeSerializerRelatedChangeable(serializers.ModelSerializer):
    status_id = serializers.PrimaryKeyRelatedField(queryset=SuggestionThemeStatus.objects.all(), allow_null=False, required=True, source="status")

    class Meta:
        model = SuggestionTheme
        fields = ('id', 'status_id')

    def update(self, instance: SuggestionTheme, validated_data):
        status_name = validated_data["status"].name
        if status_name == "WAITING_STUDENT" or status_name == "WAITING_CURATOR":
            pass
        elif status_name == "IN_PROGRESS_STUDENT" or status_name == "IN_PROGRESS_CURATOR":
            # create SuggestionThemeProgress if it does not exist
            if not instance.progress:
                instance.progress = SuggestionThemeProgress.objects.create(
                    title=instance.theme.title,
                    description=instance.theme.description,
                    date_update=localtime())
                instance.save()
        elif status_name == "REJECTED_STUDENT" or status_name == "REJECTED_CURATOR":
            pass
        elif status_name == "ACCEPTED_BOTH":
            # merge updated data with related theme (through UPDATE)
            if instance.progress:
                instance.theme.title = instance.progress.title
                instance.theme.description = instance.progress.description

            instance.theme.curator = instance.curator
            instance.theme.student = instance.student
            instance.theme.save()   # it calls sql UPDATE. it is IMPORTANT for database trigger

            # reject rest of suggestions
            SuggestionTheme.objects \
                .exclude(student=instance.student) \
                .filter(curator=instance.curator, theme=instance.theme) \
                .update(status=SuggestionThemeStatus.objects.get(name__exact="REJECTED_CURATOR"))

        # change date_update field
        if instance.progress:
            instance.progress.date_update = localtime()
            instance.progress.save()

        super().update(instance, validated_data)


# GET
class SuggestionThemeSerializerRelatedIntermediate(serializers.ModelSerializer):
    theme = ThemeSerializerNoSkills(read_only=True)
    student = StudentSerializerNoSkills(read_only=True, allow_null=True)
    curator = CuratorSerializerNoSkills(read_only=True, allow_null=True)
    status = SuggestionThemeStatusSerializer(read_only=True)
    progress = SuggestionThemeProgressSerializer(read_only=True, allow_null=True)

    class Meta:
        model = SuggestionTheme
        fields = ('id', 'date_creation',
                  'theme', 'student', 'curator', 'status', 'progress')


# GET
class SuggestionThemeCommentSerializer(serializers.ModelSerializer):
    suggestion_id = serializers.PrimaryKeyRelatedField(read_only=True, source="suggestion")

    class Meta:
        model = SuggestionThemeComment
        fields = ('id', 'author_name', 'content', 'date_creation', 'suggestion_id')


# POST
class SuggestionThemeCommentSerializerNoRelated(serializers.ModelSerializer):
    class Meta:
        model = SuggestionThemeComment
        fields = ('id', 'author_name', 'content')
