from rest_framework import serializers

from ..models.curator import Curator
from ..models.skill import Skill

from .skill import SkillSerializer


class CuratorSerializerSkillsID(serializers.ModelSerializer):
    skills_id = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())

    class Meta:
        model = Curator
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'skills_id')


class CuratorSerializerSkillsIntermediate(serializers.ModelSerializer):
    skills_id = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Curator
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'skills_id')


class CuratorSerializerNoSkills(serializers.ModelSerializer):
    class Meta:
        model = Curator
        fields = ('id', 'name', 'last_name', 'patronymic', 'description')
