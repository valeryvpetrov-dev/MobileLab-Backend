from rest_framework import serializers

from ..models.curator import Curator
from ..models.skill import Skill

from .skill import SkillSerializer


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
