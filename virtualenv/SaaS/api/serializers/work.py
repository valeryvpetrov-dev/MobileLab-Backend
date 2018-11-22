from rest_framework import serializers

from ..models.work import *

from .theme import ThemeSerializerRelatedID


class WorkStepStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkStepStatus
        fields = ('id', 'name')


class WorkSerializer(serializers.ModelSerializer):
    theme = ThemeSerializerRelatedID(read_only=True)

    class Meta:
        model = Work
        fields = ('id', 'date_start', 'date_finish', 'theme')


class WorkStepSerializer(serializers.ModelSerializer):
    status = WorkStepStatusSerializer(read_only=True)

    class Meta:
        model = WorkStep
        fields = ('id', 'title', 'description', 'date_start', 'date_finish',
                  'status')


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
