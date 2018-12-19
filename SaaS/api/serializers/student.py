from rest_framework import serializers

from ..models.student import Student, Group
from ..models.skill import Skill

from .skill import SkillSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class GroupSerializerNameOnly(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )


class StudentSerializerRelatedID(serializers.ModelSerializer):
    skills_id = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all(), source="skills")
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), allow_null=True, required=False, source="group")

    class Meta:
        model = Student
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'course_number', 'skills_id', 'group_id')


class StudentSerializerRelatedIntermediate(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    group = GroupSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Student
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'course_number', 'skills', 'group')


class StudentSerializerNoSkills(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Student
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'course_number', 'group')
