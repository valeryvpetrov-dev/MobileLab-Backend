from rest_framework import serializers

from ..models.suggestion import *

from .theme import ThemeSerializerNoSkills
from .student import StudentSerializerNoSkills
from .curator import CuratorSerializerNoSkills


class SuggestionThemeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionThemeStatus
        fields = ('id', 'name')


class SuggestionThemeProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionThemeProgress
        fields = ('id', 'title', 'description', 'date_update')


class SuggestionThemeSerializerRelatedID(serializers.ModelSerializer):
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), allow_null=False, required=True)
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), allow_null=False, required=True)
    curator = serializers.PrimaryKeyRelatedField(queryset=Curator.objects.all(), allow_null=False, required=True)
    status = serializers.PrimaryKeyRelatedField(queryset=SuggestionThemeStatus.objects.all(), allow_null=False,
                                                default=SuggestionThemeStatus.objects.get(name__exact="Нет ответа"))
    progress = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=False)

    class Meta:
        model = SuggestionTheme
        fields = ('id', 'date_creation',
                  'theme', 'student', 'curator', 'status', 'progress')


class SuggestionThemeSerializerRelatedIntermediate(serializers.ModelSerializer):
    theme = ThemeSerializerNoSkills(read_only=True)
    student = StudentSerializerNoSkills(read_only=True, allow_null=True)
    curator = CuratorSerializerNoSkills(read_only=True, allow_null=True)
    status = SuggestionThemeStatusSerializer(read_only=True)
    progress = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)

    class Meta:
        model = SuggestionTheme
        fields = ('id', 'date_creation',
                  'theme', 'student', 'curator', 'status', 'progress')


class SuggestionThemeCommentSerializer(serializers.ModelSerializer):
    suggestion = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SuggestionThemeComment
        fields = ('id', 'author_name', 'content', 'date_creation', 'suggestion')
