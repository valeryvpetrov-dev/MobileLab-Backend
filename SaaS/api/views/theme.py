from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.authentication import TokenAuthentication

from ..models.theme import Theme, Subject

from ..serializers.theme import ThemeSerializerRelatedID, ThemeSerializerRelatedIntermediate, SubjectSerializer
from ..serializers.skill import SkillSerializer

from ..permissions.group_curators import IsMemberOfCuratorsGroup


class ThemeBaseViewAbstract:
    """
    Theme base view
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMemberOfCuratorsGroup,)  # TODO Change behavior when student app will be developed

    def get_theme(self, pk):
        return get_object_or_404(Theme, pk=pk)


class ThemeBaseView(ThemeBaseViewAbstract, GenericAPIView):
    pass


class ThemeList(ThemeBaseViewAbstract, ListAPIView):
    """
    get:
    READ - List of themes.
    """
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializerRelatedID


class ThemeDetail(ThemeBaseView):
    """
    get:
    READ - Theme instance details.
    """
    def get(self, request, theme_id):
        theme = self.get_theme(theme_id)
        serializer = ThemeSerializerRelatedIntermediate(theme)
        return Response(serializer.data)


# related skills
class ThemeSkillList(ThemeBaseView):
    """
    get:
    READ - Theme instance related skills.
    """
    def get(self, request, theme_id):
        theme = self.get_theme(theme_id)
        serializer = SkillSerializer(theme.skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubjectList(ThemeBaseView, ListAPIView):
    """
    get:
    READ - Theme subjects list.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetail(ThemeBaseView):
    """
    get:
    READ - Theme subject details.
    """
    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data, status=status.HTTP_200_OK)
