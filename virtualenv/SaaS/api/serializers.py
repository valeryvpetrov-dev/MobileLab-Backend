from rest_framework import serializers

from .models import Skill


class SkillSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Create Skill instance based on validated_data
        :param validated_data: dict of validated by Serializer data which represents Skill instance
        :return: Skill instance based on validated_data
        """
        return Skill.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing Skill instance using given validate_data
        :param instance: given instance of Skill to be updated
        :param validated_data: data for updating instance
        :return: updated Skill instance
        """
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
