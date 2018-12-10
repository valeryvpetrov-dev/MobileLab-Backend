from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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

from rest_framework.authentication import TokenAuthentication


class CuratorBaseView(APIView):
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


class CuratorList(CuratorBaseView):
    """
    Methods: GET
    Description: List of curators
    """
    def get(self, request):
        """
        READ: Curator list
        :return: json of curator list
        """
        curators = Curator.objects.all()
        serializer = CuratorSerializerNoSkills(curators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CuratorDetail(CuratorBaseView):
    """
    Methods: GET, PUT
    Description: Curator details
    """
    def get(self, request, curator_id):
        """
        READ: Curator details
        :return: json of curator
        """
        curator = self.get_curator(curator_id)
        serializer = CuratorSerializerSkillsIntermediate(curator)
        return Response(serializer.data)

    def put(self, request, curator_id):
        """
        UPDATE: Curator details
        :param request: json of updated curator
        :param curator_id:
        :return: json of updated curator
        """
        curator = self.get_curator(curator_id)
        serializer = CuratorSerializerSkillsID(curator, data=request.data)
        if serializer.is_valid():
            serializer.update(curator, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related skills
class CuratorSkillList(CuratorBaseView):
    """
    Methods: GET
    Description: Curator related skills
    """
    def get(self, request, curator_id):
        """
        READ: Curator skills list
        :return: json of curator skills list
        """
        curator = self.get_curator(curator_id)
        serializer = SkillSerializer(curator.skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# related works
class CuratorWorkList(CuratorBaseView):
    """
    Methods: GET, POST
    Description: Curator related works
    """
    def get(self, request, curator_id):
        """
        READ: Curator works list
        :return: json of curator works list
        """
        curator = self.get_curator(curator_id)
        related_works = []
        for theme in curator.theme_set.all():
            for work in theme.work_set.all():
                related_works.append(work)
        serializer = WorkSerializer(related_works, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id):
        """
        CREATE: Curator work
        :param request: json of new work
        :param curator_id:
        :return: json of created work
        """
        curator = self.get_curator(curator_id)
        serializer = WorkSerializer(data=request.data)
        if serializer.is_valid():
            work = serializer.create(validated_data=serializer.validated_data)
            curator.theme_set.add(work.theme)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuratorWorkDetail(CuratorBaseView):
    """
    Methods: GET, PUT, DELETE
    Description: Curator related work details
    """
    def get(self, request, curator_id, work_id):
        """
        READ: Curator related work details
        :return: json of curator related work
        """
        curator = self.get_curator(curator_id)
        work = self.get_related_work(curator, work_id)
        if work:
            serializer = WorkSerializer(work)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, curator_id, work_id):
        """
        UPDATE: Curator related work details
        :param request: json of updated work
        :param curator_id:
        :param work_id:
        :return: json of updated curator related work
        """
        curator = self.get_curator(curator_id)
        work = self.get_related_work(curator, work_id)
        serializer = WorkSerializer(work, data=request.data)
        if serializer.is_valid():
            serializer.update(work, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curator_id, work_id):
        """
        DELETE: Curator related work
        :param request:
        :param curator_id:
        :param work_id:
        :return: json of deleted curator related work
        """
        curator = self.get_curator(curator_id)
        work = self.get_related_work(curator, work_id)
        serializer = WorkSerializer(work)
        if work.delete():
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# related work-steps
class CuratorWorkStepList(CuratorBaseView):
    """
    Methods: GET, POST
    Description: Curator related work steps
    """
    def get(self, request, curator_id, work_id):
        """
        READ: Curator related work steps list
        :return: json of curator related work steps list
        """
        work = self.get_related_work(self.get_curator(curator_id), work_id)
        related_steps = []
        for step in work.step_set.all():
            related_steps.append(step)
        serializer = WorkStepSerializer(related_steps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id, work_id):
        """
        CREATE: Curator related work step
        :param request: json of new step
        :param curator_id:
        :param work_id:
        :return: json of new step
        """
        work = self.get_related_work(self.get_curator(curator_id), work_id)
        serializer = WorkStepSerializer(data=request.data)
        if serializer.is_valid():
            step = serializer.create(validated_data=serializer.validated_data)
            work.step_set.add(step)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuratorWorkStepDetail(CuratorBaseView):
    """
    Methods: GET, PUT, DELETE
    Description: Curator related work step details
    """
    def get(self, request, curator_id, work_id, step_id):
        """
        READ: Curator related work step details
        :return: json of curator related work step
        """
        curator = self.get_curator(curator_id)
        related_work = self.get_related_work(curator, work_id)
        step = self.get_related_step(related_work, step_id)
        if step:
            serializer = WorkStepSerializer(step)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, curator_id, work_id, step_id):
        """
        UPDATE: Curator related work step details
        :param request: json of updated work step
        :param curator_id:
        :param work_id:
        :param step_id:
        :return: json of updated curator related work step
        """
        curator = self.get_curator(curator_id)
        related_work = self.get_related_work(curator, work_id)
        step = self.get_related_step(related_work, step_id)
        serializer = WorkStepSerializer(step, data=request.data)
        if serializer.is_valid():
            serializer.update(step, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curator_id, work_id, step_id):
        """
        DELETE: Curator related work step
        :param request:
        :param curator_id:
        :param work_id:
        :param step_id: step to delete
        :return: json of deleted curator related work step
        """
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
    Methods: GET, POST
    Description: Curator related work step materials
    """
    def get(self, request, curator_id, work_id, step_id):
        """
        READ: Curator related work step materials list
        :return: json of curator related work steps materials list
        """
        curator = self.get_curator(curator_id)
        related_work = self.get_related_work(curator, work_id)
        step = self.get_related_step(related_work, step_id)
        related_materials = []
        for material in step.material_set.all():
            related_materials.append(material)
        serializer = WorkStepMaterialSerializer(related_materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id, work_id, step_id):
        """
        CREATE: Curator related work step material
        :param request: json of new material
        :param curator_id:
        :param work_id:
        :param step_id:
        :return: json of new material
        """
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
    Methods: GET, POST
    Description: Curator related work step comments
    """
    def get(self, request, curator_id, work_id, step_id):
        """
        READ: Curator related work step comments list
        :return: json of curator related work steps comments list
        """
        curator = self.get_curator(curator_id)
        related_work = self.get_related_work(curator, work_id)
        step = self.get_related_step(related_work, step_id)
        related_comments = []
        for comment in step.comment_set.all():
            related_comments.append(comment)
        serializer = WorkStepCommentSerializer(related_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id, work_id, step_id):
        """
        CREATE: Curator related work step comment
        :param request: json of new comment
        :param curator_id:
        :param work_id:
        :param step_id:
        :return: json of new comment
        """
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
    Methods: GET, POST
    Description: Curator related themes
    """
    def get(self, request, curator_id):
        """
        READ: Curator themes list
        :return: json of curator themes list
        """
        curator = self.get_curator(curator_id)
        serializer = ThemeSerializerRelatedIntermediate(curator.theme_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id):
        """
        CREATE: Curator theme
        :param request: json of new theme
        :param curator_id:
        :return: json of created theme
        """
        curator = self.get_curator(curator_id)
        serializer = ThemeSerializerRelatedIntermediate(data=request.data)
        if serializer.is_valid():
            theme = serializer.create(validated_data=serializer.validated_data)
            curator.theme_set.add(theme)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuratorThemeDetail(CuratorBaseView):
    """
    Methods: GET, PUT, DELETE
    Description: Curator related theme details
    """
    def get(self, request, curator_id, theme_id):
        """
        READ: Curator related theme details
        :return: json of curator related theme
        """
        curator = self.get_curator(curator_id)
        theme = self.get_related_theme(curator, theme_id)
        if theme:
            serializer = ThemeSerializerRelatedIntermediate(theme)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, curator_id, theme_id):
        """
        UPDATE: Curator related theme details
        :param request: json of updated theme
        :param curator_id:
        :param theme_id:
        :return: json of updated curator related theme
        """
        curator = self.get_curator(curator_id)
        theme = self.get_related_theme(curator, theme_id)
        serializer = ThemeSerializerRelatedID(theme, data=request.data)
        if serializer.is_valid():
            serializer.update(theme, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curator_id, theme_id):
        """
        DELETE: Curator related theme
        :param request:
        :param curator_id:
        :param theme_id: theme to delete
        :return: json of deleted curator related theme
        """
        curator = self.get_curator(curator_id)
        theme = self.get_related_theme(curator, theme_id)
        serializer = ThemeSerializerRelatedID(theme)
        if theme.delete():
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# related suggestions
class CuratorSuggestionList(CuratorBaseView):
    """
    Methods: GET, POST
    Description: Curator related suggestions
    """
    def get(self, request, curator_id):
        """
        READ: Curator suggestions list
        :return: json of curator suggestions list
        """
        curator = self.get_curator(curator_id)
        serializer = SuggestionThemeSerializer(curator.suggestiontheme_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id):
        """
        CREATE: Curator suggestion
        :param request: json of new suggestion
        :param curator_id:
        :return: json of created suggestion
        """
        curator = self.get_curator(curator_id)
        serializer = SuggestionThemeSerializer(data=request.data)
        if serializer.is_valid():
            suggestion = serializer.create(validated_data=serializer.validated_data)
            curator.suggestiontheme_set.add(suggestion)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuratorSuggestionDetail(CuratorBaseView):
    """
    Methods: GET, PUT, DELETE
    Description: Curator related suggestion details
    """
    def get(self, request, curator_id, suggestion_id):
        """
        READ: Curator related suggestion details
        :return: json of curator related suggestion
        """
        curator = self.get_curator(curator_id)
        suggestion = self.get_related_suggestion(curator, suggestion_id)
        if suggestion:
            serializer = SuggestionThemeSerializer(suggestion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, curator_id, suggestion_id):
        """
        UPDATE: Curator related suggestion details
        :param request: json of updated suggestion
        :param curator_id:
        :param suggestion_id:
        :return: json of updated curator related suggestion
        """
        curator = self.get_curator(curator_id)
        suggestion = self.get_related_suggestion(curator, suggestion_id)
        serializer = SuggestionThemeSerializer(suggestion, data=request.data)
        if serializer.is_valid():
            serializer.update(suggestion, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curator_id, suggestion_id):
        """
        DELETE: Curator related suggestion
        :param request:
        :param curator_id:
        :param suggestion_id: suggestion to delete
        :return: json of deleted curator related suggestion
        """
        curator = self.get_curator(curator_id)
        suggestion = self.get_related_suggestion(curator, suggestion_id)
        serializer = SuggestionThemeSerializer(suggestion)
        if suggestion.delete():
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# related suggestion-comments
class CuratorSuggestionCommentList(CuratorBaseView):
    """
    Methods: GET, POST
    Description: Curator related suggestion comments
    """
    def get(self, request, curator_id, suggestion_id):
        """
        READ: Curator suggestion comments list
        :return: json of curator suggestion comments list
        """
        curator = self.get_curator(curator_id)
        suggestion = self.get_related_suggestion(curator, suggestion_id)
        serializer = SuggestionThemeCommentSerializer(suggestion.comment_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id, suggestion_id):
        """
        CREATE: Curator suggestion comment
        :param request: json of new comment
        :param curator_id:
        :param suggestion_id:
        :return: json of created comment
        """
        curator = self.get_curator(curator_id)
        suggestion = self.get_related_suggestion(curator, suggestion_id)
        serializer = SuggestionThemeCommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.create(validated_data=serializer.validated_data)
            suggestion.comment_set.add(comment)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
