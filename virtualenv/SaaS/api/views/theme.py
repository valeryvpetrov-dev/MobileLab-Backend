from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from ..models.theme import Theme

from ..serializers.theme import ThemeSerializerRelatedID, ThemeSerializerRelatedIntermediate, ThemeSerializerNoSkills
from ..serializers.skill import SkillSerializer


class ThemeBaseView(APIView):
    """
    Theme base view
    """
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
        curators = Theme.objects.all()
        serializer = ThemeSerializerRelatedID(curators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    def put(self, request, theme_id):
        """
        UPDATE: Theme details
        :param request: json of updated theme
        :param theme_id:
        :return: json of updated theme
        """
        theme = self.get_theme(theme_id)
        serializer = ThemeSerializerRelatedID(theme, data=request.data)
        if serializer.is_valid():
            serializer.update(theme, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
