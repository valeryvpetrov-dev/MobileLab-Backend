from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.http import Http404

from ..models.theme import Theme

from ..serializers.theme import ThemeSerializerRelatedID, ThemeSerializerRelatedIntermediate, ThemeSerializerNoSkills
from ..serializers.skill import SkillSerializer

from ..permissions.group_curators import IsMemberOfCuratorsGroup


class ThemeBaseView(APIView):
    """
    Theme base view
    """
    permission_classes = (IsAuthenticated, IsMemberOfCuratorsGroup,)  # TODO Change behavior when student app will be developed

    def get_theme(self, pk):
        try:
            return Theme.objects.get(pk=pk)
        except Theme.DoesNotExist:
            raise Http404


class ThemeList(ThemeBaseView):
    """
    Methods: GET
    Description: List of themes
    """
    def get(self, request):
        """
        READ: Theme list
        :return: json of theme list
        """
        themes = Theme.objects.all()
        if themes:
            serializer = ThemeSerializerRelatedID(themes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ThemeDetail(ThemeBaseView):
    """
    Methods: GET, PUT
    Description: Theme details
    """
    def get(self, request, theme_id):
        """
        READ: Theme details
        :return: json of theme
        """
        theme = self.get_theme(theme_id)
        serializer = ThemeSerializerRelatedIntermediate(theme)
        return Response(serializer.data)


# related skills
class ThemeSkillList(ThemeBaseView):
    """
    Methods: GET
    Description: Theme related skills
    """
    def get(self, request, theme_id):
        """
        READ: Theme skills list
        :return: json of theme skills list
        """
        theme = self.get_theme(theme_id)
        serializer = SkillSerializer(theme.skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
