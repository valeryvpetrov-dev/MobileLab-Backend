from rest_framework import serializers

from ..models.student import Student
from ..models.skill import Skill

from .skill import SkillSerializer


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
