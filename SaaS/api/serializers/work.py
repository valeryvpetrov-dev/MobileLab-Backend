from rest_framework import serializers

from ..models.work import *

from .theme import ThemeSerializerRelatedID, ThemeSerializerRelatedIntermediate


class WorkStepStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkStepStatus
        fields = ('id', 'name')


class WorkSerializerRelatedID(serializers.ModelSerializer):
    theme = ThemeSerializerRelatedID(read_only=True)

    class Meta:
        model = Work
        fields = ('id', 'date_start', 'date_finish', 'theme')


class WorkSerializerRelatedIntermediate(serializers.ModelSerializer):
    theme = ThemeSerializerRelatedIntermediate(read_only=True)

    class Meta:
        model = Work
        fields = ('id', 'date_start', 'date_finish', 'theme')


class WorkStepSerializer(serializers.ModelSerializer):
    status = WorkStepStatusSerializer(read_only=True)

    class Meta:
        model = WorkStep
        fields = ('id', 'title', 'description', 'date_start', 'date_finish',
                  'status')


class WorkStepSerializerRelatedID(serializers.ModelSerializer):
    status_id = serializers.PrimaryKeyRelatedField(read_only=False, queryset=WorkStepStatus.objects.all())

    class Meta:
        model = WorkStep
        fields = ('id', 'title', 'description', 'date_start', 'date_finish', 'status_id')


class WorkStepCommentSerializer(serializers.ModelSerializer):
    step_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WorkStepComment
        fields = ('id', 'author_name', 'content', 'date_creation', 'step_id')


class WorkStepCommentSerializerNoRelated(serializers.ModelSerializer):
    class Meta:
        model = WorkStepComment
        fields = ('id', 'author_name', 'content', 'date_creation')


class WorkStepMaterialSerializer(serializers.ModelSerializer):
    step_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WorkStepMaterial
        fields = ('id', 'content', 'step_id')


class WorkStepMaterialSerializerNoRelated(serializers.ModelSerializer):
    class Meta:
        model = WorkStepMaterial
        fields = ('id', 'content')
