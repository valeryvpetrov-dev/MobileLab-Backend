from rest_framework import serializers

from .models import *


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name')


class WorkStepStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkStepStatus
        fields = ('id', 'name')


class SuggestionThemeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionThemeStatus
        fields = ('id', 'name')


class SuggestionThemeProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionThemeProgress
        fields = ('id', 'title', 'description', 'date_update')


class StudentSerializerSkillsID(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())

    class Meta:
        model = Student
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'skills')


class StudentSerializerSkillsIntermediate(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'skills')


class StudentSerializerNoSkills(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'last_name', 'patronymic', 'description')


class CuratorSerializerSkillsID(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())

    class Meta:
        model = Curator
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'skills')


class CuratorSerializerSkillsIntermediate(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Curator
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'skills')


class CuratorSerializerNoSkills(serializers.ModelSerializer):
    class Meta:
        model = Curator
        fields = ('id', 'name', 'last_name', 'patronymic', 'description')


class ThemeSerializerRelatedID(serializers.ModelSerializer):
    curator = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    student = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    subject = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    skills = serializers.PrimaryKeyRelatedField(many=True, read_only=True, allow_null=True)

    class Meta:
        model = Theme
        fields = ('id', 'title', 'description', 'date_creation', 'date_acceptance',
                  'curator', 'student', 'subject', 'skills')


class ThemeSerializerRelatedIntermediate(serializers.ModelSerializer):
    curator = CuratorSerializerNoSkills(read_only=True, allow_null=True)
    student = StudentSerializerNoSkills(read_only=True, allow_null=True)
    subject = SubjectSerializer(read_only=True, allow_null=True)
    skills = SkillSerializer(many=True, read_only=True, allow_null=True)

    class Meta:
        model = Theme
        fields = ('id', 'title', 'description', 'date_creation', 'date_acceptance',
                  'curator', 'student', 'subject', 'skills')


class ThemeSerializerNoSkills(serializers.ModelSerializer):
    curator = CuratorSerializerNoSkills(read_only=True, allow_null=True)
    student = StudentSerializerNoSkills(read_only=True, allow_null=True)
    subject = SubjectSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Theme
        fields = ('id', 'title', 'description', 'date_creation', 'date_acceptance',
                  'curator', 'student', 'subject')


class WorkSerializer(serializers.ModelSerializer):
    theme = ThemeSerializerNoSkills(read_only=True)

    class Meta:
        model = Work
        fields = ('id', 'date_start', 'date_finish', 'theme')


class WorkStepSerializer(serializers.ModelSerializer):
    work = WorkSerializer(read_only=True)
    status = WorkStepStatusSerializer(read_only=True)

    class Meta:
        model = WorkStep
        fields = ('id', 'title', 'description', 'date_start', 'date_finish',
                  'work', 'status')


class WorkStepCommentSerializer(serializers.ModelSerializer):
    step = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WorkStepComment
        fields = ('id', 'author_name', 'content', 'date_creation', 'step')


class WorkStepMaterialSerializer(serializers.ModelSerializer):
    step = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WorkStepMaterial
        fields = ('id', 'content', 'step')


class SuggestionThemeSerializer(serializers.ModelSerializer):
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
