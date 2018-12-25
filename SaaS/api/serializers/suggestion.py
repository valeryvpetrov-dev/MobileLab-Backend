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


# TODO date_update
class SuggestionThemeProgressSerializer(serializers.ModelSerializer):
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


# PUT, POST
class SuggestionThemeSerializerRelatedIDNoProgress(serializers.ModelSerializer):
    theme_id = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), allow_null=False, required=True, source="theme")
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), allow_null=False, required=True, source="student")
    curator_id = serializers.PrimaryKeyRelatedField(queryset=Curator.objects.all(), allow_null=False, required=True, source="curator")
    status_id = serializers.PrimaryKeyRelatedField(queryset=SuggestionThemeStatus.objects.all(), allow_null=False, required=True, source="status")

    class Meta:
        model = SuggestionTheme
        fields = ('id', 'theme_id', 'student_id', 'curator_id', 'status_id')


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
