from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.authentication import TokenAuthentication

from ..models.skill import Skill

from ..serializers.skill import SkillSerializer

from ..permissions.group_curators import IsMemberOfCuratorsGroup


class SkillBaseViewAbstract:
    """
    Skill base view
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMemberOfCuratorsGroup,)  # TODO Change behavior when student app will be developed

    def get_skill(self, pk):
        return get_object_or_404(Skill, pk=pk)


class SkillBaseView(SkillBaseViewAbstract, GenericAPIView):
    pass


class SkillList(SkillBaseViewAbstract, ListAPIView):
    """
    get:
    READ - List of skills.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class SkillDetail(SkillBaseView):
    """
    get:
    READ - Theme instance details.
    """
    def get(self, request, skill_id):
        skill = self.get_skill(skill_id)
        serializer = SkillSerializer(skill)
        return Response(serializer.data, status=status.HTTP_200_OK)
