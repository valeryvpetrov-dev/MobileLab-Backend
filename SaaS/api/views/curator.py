from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication

from django.http import Http404

from ..models.theme import Theme
from ..models.suggestion import SuggestionTheme
from ..models.curator import Curator
from ..models.work import Work, WorkStep

from ..serializers.curator import CuratorSerializerSkillsIntermediate, CuratorSerializerSkillsID, CuratorSerializerNoSkills
from ..serializers.skill import SkillSerializer
from ..serializers.work import WorkSerializer, WorkStepSerializer, WorkStepMaterialSerializer, WorkStepCommentSerializer
from ..serializers.theme import ThemeSerializerRelatedID, ThemeSerializerRelatedIntermediate
from ..serializers.suggestion import SuggestionThemeSerializer, SuggestionThemeCommentSerializer

from ..permissions.group_curators import IsMemberOfCuratorsGroup


class CuratorBaseViewAbstract:
    """
    Curator base view
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsMemberOfCuratorsGroup, )   # TODO Change behavior when student app will be developed

    def get_curator(self, pk):
        try:
            return Curator.objects.get(pk=pk)
        except Curator.DoesNotExist:
            raise Http404

    def get_related_work(self, curator: Curator, work_id: int):
        work = None
        for theme in curator.theme_set.all():
            try:
                work = theme.work_set.get(pk=work_id)
            except Work.DoesNotExist:
                pass
        if ~work: raise Http404
        return work

    def get_related_step(self, related_work: Work, step_id: int):
        try:
            return related_work.step_set.get(pk=step_id)
        except WorkStep.DoesNotExist:
            raise Http404

    def get_related_theme(self, curator: Curator, theme_id: int):
        try:
            return curator.theme_set.get(pk=theme_id)
        except Theme.DoesNotExist:
            raise Http404

    def get_related_suggestion(self, curator: Curator, suggestion_id: int):
        try:
            return curator.suggestiontheme_set.get(pk=suggestion_id)
        except SuggestionTheme.DoesNotExist:
            raise Http404


class CuratorBaseView(CuratorBaseViewAbstract, APIView):
    pass


class CuratorList(CuratorBaseViewAbstract, ListAPIView):
    """
    get:
    READ - List of curators.
    """
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializerNoSkills


class CuratorDetail(CuratorBaseView):
    """
    get:
    READ - Curator instance details.

    put:
    UPDATE - Curator instance details.
    """
    def get(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = CuratorSerializerSkillsIntermediate(curator)
        return Response(serializer.data)

    def put(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = CuratorSerializerSkillsID(curator, data=request.data)
        if serializer.is_valid():
            serializer.update(curator, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related skills
class CuratorSkillList(CuratorBaseView):
    """
    get:
    READ - List of curator instance related skills.
    """
    def get(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = SkillSerializer(curator.skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# related works
class CuratorWorkList(CuratorBaseView):
    """
    get:
    READ - List of curator instance related works.

    post:
    CREATE - Curator instance related work.
    """
    def get(self, request, curator_id):
        curator = self.get_curator(curator_id)
        related_works = []
        for theme in curator.theme_set.all():
            for work in theme.work_set.all():
                related_works.append(work)
        serializer = WorkSerializer(related_works, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = WorkSerializer(data=request.data)
        if serializer.is_valid():
            work = serializer.create(validated_data=serializer.validated_data)
            curator.theme_set.add(work.theme)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuratorWorkDetail(CuratorBaseView):
    """
    get:
    READ - Curator instance related work.

    put:
    UPDATE - Curator instance related work.

    delete:
    DELETE - Curator instance related work.
    """
    def get(self, request, curator_id, work_id):
        curator = self.get_curator(curator_id)
        work = self.get_related_work(curator, work_id)
        if work:
            serializer = WorkSerializer(work)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, curator_id, work_id):
        curator = self.get_curator(curator_id)
        work = self.get_related_work(curator, work_id)
        serializer = WorkSerializer(work, data=request.data)
        if serializer.is_valid():
            serializer.update(work, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curator_id, work_id):
        curator = self.get_curator(curator_id)
        work = self.get_related_work(curator, work_id)
        serializer = WorkSerializer(work)
        if work.delete():
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# related work-steps
class CuratorWorkStepList(CuratorBaseView):
    """
    get:
    READ - Curator instance related work steps.

    post:
    CREATE - Curator instance related work step.
    """
    def get(self, request, curator_id, work_id):
        work = self.get_related_work(self.get_curator(curator_id), work_id)
        related_steps = []
        for step in work.step_set.all():
            related_steps.append(step)
        serializer = WorkStepSerializer(related_steps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id, work_id):
        work = self.get_related_work(self.get_curator(curator_id), work_id)
        serializer = WorkStepSerializer(data=request.data)
        if serializer.is_valid():
            step = serializer.create(validated_data=serializer.validated_data)
            work.step_set.add(step)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuratorWorkStepDetail(CuratorBaseView):
    """
    get:
    READ - Curator instance related work step details.

    put:
    UPDATE - Curator instance related work step details.

    delete:
    DELETE - Curator instance related work step.
    """
    def get(self, request, curator_id, work_id, step_id):
        curator = self.get_curator(curator_id)
        related_work = self.get_related_work(curator, work_id)
        step = self.get_related_step(related_work, step_id)
        if step:
            serializer = WorkStepSerializer(step)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, curator_id, work_id, step_id):
        curator = self.get_curator(curator_id)
        related_work = self.get_related_work(curator, work_id)
        step = self.get_related_step(related_work, step_id)
        serializer = WorkStepSerializer(step, data=request.data)
        if serializer.is_valid():
            serializer.update(step, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curator_id, work_id, step_id):
        curator = self.get_curator(curator_id)
        related_work = self.get_related_work(curator, work_id)
        step = self.get_related_step(related_work, step_id)
        serializer = WorkStepSerializer(step)
        if step.delete():
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# related work-step-materials
class CuratorWorkStepMaterialList(CuratorBaseView):
    """
    get:
    READ - Curator instance related work step materials.

    post:
    CREATE - Curator instance related work step material.
    """
    def get(self, request, curator_id, work_id, step_id):
        curator = self.get_curator(curator_id)
        related_work = self.get_related_work(curator, work_id)
        step = self.get_related_step(related_work, step_id)
        related_materials = []
        for material in step.material_set.all():
            related_materials.append(material)
        serializer = WorkStepMaterialSerializer(related_materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id, work_id, step_id):
        curator = self.get_curator(curator_id)
        related_work = self.get_related_work(curator, work_id)
        step = self.get_related_step(related_work, step_id)
        serializer = WorkStepMaterialSerializer(data=request.data)
        if serializer.is_valid():
            material = serializer.create(validated_data=serializer.validated_data)
            step.material_set.add(material)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related work-step-comments
class CuratorWorkStepCommentList(CuratorBaseView):
    """
    get:
    READ - Curator instance related work step comments.

    post:
    CREATE - Curator instance related work step comment.
    """
    def get(self, request, curator_id, work_id, step_id):
        curator = self.get_curator(curator_id)
        related_work = self.get_related_work(curator, work_id)
        step = self.get_related_step(related_work, step_id)
        related_comments = []
        for comment in step.comment_set.all():
            related_comments.append(comment)
        serializer = WorkStepCommentSerializer(related_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id, work_id, step_id):
        curator = self.get_curator(curator_id)
        related_work = self.get_related_work(curator, work_id)
        step = self.get_related_step(related_work, step_id)
        serializer = WorkStepCommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.create(validated_data=serializer.validated_data)
            step.comment_set.add(comment)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related themes
class CuratorThemeList(CuratorBaseView):
    """
    get:
    READ - Curator instance related themes.

    post:
    CREATE - Curator instance related theme.
    """
    def get(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = ThemeSerializerRelatedIntermediate(curator.theme_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = ThemeSerializerRelatedIntermediate(data=request.data)
        if serializer.is_valid():
            theme = serializer.create(validated_data=serializer.validated_data)
            curator.theme_set.add(theme)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuratorThemeDetail(CuratorBaseView):
    """
    get:
    READ - Curator instance related theme details.

    put:
    UPDATE - Curator instance related theme details.

    delete:
    DELETE - Curator instance related theme.
    """
    def get(self, request, curator_id, theme_id):
        curator = self.get_curator(curator_id)
        theme = self.get_related_theme(curator, theme_id)
        if theme:
            serializer = ThemeSerializerRelatedIntermediate(theme)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, curator_id, theme_id):
        curator = self.get_curator(curator_id)
        theme = self.get_related_theme(curator, theme_id)
        serializer = ThemeSerializerRelatedID(theme, data=request.data)
        if serializer.is_valid():
            serializer.update(theme, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curator_id, theme_id):
        curator = self.get_curator(curator_id)
        theme = self.get_related_theme(curator, theme_id)
        serializer = ThemeSerializerRelatedID(theme)
        if theme.delete():
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# related suggestions
class CuratorSuggestionList(CuratorBaseView):
    """
    get:
    READ - Curator instance related suggestions.

    post:
    CREATE - Curator instance related suggestion.
    """
    def get(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = SuggestionThemeSerializer(curator.suggestiontheme_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = SuggestionThemeSerializer(data=request.data)
        if serializer.is_valid():
            suggestion = serializer.create(validated_data=serializer.validated_data)
            curator.suggestiontheme_set.add(suggestion)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuratorSuggestionDetail(CuratorBaseView):
    """
    get:
    READ - Curator instance related suggestion details.

    put:
    UPDATE - Curator instance related suggestion details.

    delete:
    DELETE - Curator instance related suggestion.
    """
    def get(self, request, curator_id, suggestion_id):
        curator = self.get_curator(curator_id)
        suggestion = self.get_related_suggestion(curator, suggestion_id)
        if suggestion:
            serializer = SuggestionThemeSerializer(suggestion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, curator_id, suggestion_id):
        curator = self.get_curator(curator_id)
        suggestion = self.get_related_suggestion(curator, suggestion_id)
        serializer = SuggestionThemeSerializer(suggestion, data=request.data)
        if serializer.is_valid():
            serializer.update(suggestion, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curator_id, suggestion_id):
        curator = self.get_curator(curator_id)
        suggestion = self.get_related_suggestion(curator, suggestion_id)
        serializer = SuggestionThemeSerializer(suggestion)
        if suggestion.delete():
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# related suggestion-comments
class CuratorSuggestionCommentList(CuratorBaseView):
    """
    get:
    READ - Curator instance related suggestion comments.

    post:
    CREATE - Curator instance related suggestion comment.
    """
    def get(self, request, curator_id, suggestion_id):
        curator = self.get_curator(curator_id)
        suggestion = self.get_related_suggestion(curator, suggestion_id)
        serializer = SuggestionThemeCommentSerializer(suggestion.comment_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id, suggestion_id):
        curator = self.get_curator(curator_id)
        suggestion = self.get_related_suggestion(curator, suggestion_id)
        serializer = SuggestionThemeCommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.create(validated_data=serializer.validated_data)
            suggestion.comment_set.add(comment)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
