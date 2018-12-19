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

    curator_id = serializers.PrimaryKeyRelatedField(queryset=Curator.objects.all(), allow_null=True, required=False)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), allow_null=True, required=False)
    subject_id = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), allow_null=True, required=False)
    skills_id = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Theme
        fields = ('id', 'title', 'description', 'date_creation', 'date_acceptance',
                  'curator_id', 'student_id', 'subject_id', 'skills_id')

    def create(self, validated_data):
        curator = validated_data.pop("curator", None)
        student = validated_data.pop("student", None)
        subject = validated_data.pop("subject", None)
        skills = validated_data.pop("skills", None)
        theme = Theme.objects.create(**validated_data)
        if curator:
            theme.curator = Curator.objects.get(pk=curator.id)
        if student:
            theme.student = Student.objects.get(pk=student.id)
        if subject:
            theme.subject = Subject.objects.get(pk=subject.id)
        if skills:
            for skill in skills:
                theme.skills.add(Skill.objects.get(pk=skill.id))
        theme.save()
        return theme


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

    def create(self, validated_data):
        curator = validated_data.pop("curator", None)
        student = validated_data.pop("student", None)
        subject = validated_data.pop("subject", None)
        skills = validated_data.pop("skills", None)
        theme = Theme.objects.create(**validated_data)
        if curator:
            theme.curator = Curator.objects.get(pk=curator.id)
        if student:
            theme.student = Student.objects.get(pk=student.id)
        if subject:
            theme.subject = Subject.objects.get(pk=subject.id)
        if skills:
            for skill in skills:
                theme.skills.add(Skill.objects.get(pk=skill.id))
        theme.save()
        return theme


class ThemeSerializerNoSkills(serializers.ModelSerializer):
    date_acceptance = serializers.DateTimeField(allow_null=True, required=False)

    curator = CuratorSerializerNoSkills(read_only=True, allow_null=True)
    student = StudentSerializerNoSkills(read_only=True, allow_null=True)
    subject = SubjectSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Theme
        fields = ('id', 'title', 'description', 'date_creation', 'date_acceptance',
                  'curator', 'student', 'subject')

    def create(self, validated_data):
        curator = validated_data.pop("curator", None)
        student = validated_data.pop("student", None)
        subject = validated_data.pop("subject", None)
        theme = Theme.objects.create(**validated_data)
        if curator:
            theme.curator = Curator.objects.get(pk=curator.id)
        if student:
            theme.student = Student.objects.get(pk=student.id)
        if subject:
            theme.subject = Subject.objects.get(pk=subject.id)
        theme.save()
        return theme
