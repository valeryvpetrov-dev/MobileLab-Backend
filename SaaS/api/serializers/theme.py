from rest_framework import serializers

from ..models.curator import Curator
from ..models.student import Student
from ..models.theme import Subject, Theme
from ..models.skill import Skill

from .curator import CuratorSerializerNoSkills
from .student import StudentSerializerNoSkills
from .skill import SkillSerializer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name')


class ThemeSerializerRelatedID(serializers.ModelSerializer):
    date_acceptance = serializers.DateTimeField(allow_null=True, required=False)

    curator_id = serializers.PrimaryKeyRelatedField(queryset=Curator.objects.all(), allow_null=True, required=False, source="curator")
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), allow_null=True, required=False, source="student")
    subject_id = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), allow_null=True, required=False, source="subject")
    skills_id = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all(), allow_null=True, required=False, source="skills")

    class Meta:
        model = Theme
        fields = ('id', 'title', 'description', 'date_creation', 'date_acceptance',
                  'curator_id', 'student_id', 'subject_id', 'skills_id')


class ThemeSerializerRelatedIntermediate(serializers.ModelSerializer):
    date_acceptance = serializers.DateTimeField(allow_null=True, required=False)

    curator = CuratorSerializerNoSkills(read_only=True, allow_null=True)
    student = StudentSerializerNoSkills(read_only=True, allow_null=True)
    subject = SubjectSerializer(read_only=True, allow_null=True)
    skills = SkillSerializer(many=True, read_only=True, allow_null=True)

    class Meta:
        model = Theme
        fields = ('id', 'title', 'description', 'date_creation', 'date_acceptance',
                  'curator', 'student', 'subject', 'skills')


class ThemeSerializerNoSkills(serializers.ModelSerializer):
    date_acceptance = serializers.DateTimeField(allow_null=True, required=False)

    curator = CuratorSerializerNoSkills(read_only=True, allow_null=True)
    student = StudentSerializerNoSkills(read_only=True, allow_null=True)
    subject = SubjectSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Theme
        fields = ('id', 'title', 'description', 'date_creation', 'date_acceptance',
                  'curator', 'student', 'subject')
