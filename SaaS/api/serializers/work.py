from rest_framework import serializers

from ..models.work import *

from .theme import ThemeSerializerRelatedID, ThemeSerializerRelatedIntermediate


# GET
class WorkStepStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkStepStatus
        fields = ('id', 'name')


# PUT
class WorkSerializerRelatedID(serializers.ModelSerializer):
    date_finish = serializers.DateTimeField(allow_null=True, required=False)
    theme = ThemeSerializerRelatedID(read_only=True)

    class Meta:
        model = Work
        fields = ('id', 'date_finish', 'theme')


# GET
class WorkSerializerRelatedIntermediate(serializers.ModelSerializer):
    theme = ThemeSerializerRelatedIntermediate(read_only=True)

    class Meta:
        model = Work
        fields = ('id', 'date_start', 'date_finish', 'theme')


# GET
class WorkStepSerializer(serializers.ModelSerializer):
    status = WorkStepStatusSerializer(read_only=True)

    class Meta:
        model = WorkStep
        fields = ('id', 'title', 'description', 'date_start', 'date_finish',
                  'status')


# POST, PUT
class WorkStepSerializerRelatedID(serializers.ModelSerializer):
    date_finish = serializers.DateTimeField(allow_null=True, required=False)
    status_id = serializers.PrimaryKeyRelatedField(read_only=False, queryset=WorkStepStatus.objects.all(), source="status")

    class Meta:
        model = WorkStep
        fields = ('id', 'title', 'description', 'date_finish', 'status_id')


# GET
class WorkStepCommentSerializer(serializers.ModelSerializer):
    step_id = serializers.PrimaryKeyRelatedField(read_only=False, queryset=WorkStep.objects.all(), source="step")

    class Meta:
        model = WorkStepComment
        fields = ('id', 'author_name', 'content', 'date_creation', 'step_id')


# POST
class WorkStepCommentSerializerNoRelated(serializers.ModelSerializer):
    class Meta:
        model = WorkStepComment
        fields = ('id', 'author_name', 'content')


# GET
class WorkStepMaterialSerializer(serializers.ModelSerializer):
    step_id = serializers.PrimaryKeyRelatedField(read_only=False, queryset=WorkStep.objects.all(), source="step")

    class Meta:
        model = WorkStepMaterial
        fields = ('id', 'content', 'step_id')


# POST
class WorkStepMaterialSerializerNoRelated(serializers.ModelSerializer):
    class Meta:
        model = WorkStepMaterial
        fields = ('id', 'content')
