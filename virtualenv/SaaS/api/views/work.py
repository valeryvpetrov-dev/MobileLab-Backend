from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.http import Http404

from ..models.work import Work, WorkStep

from ..serializers.work import WorkSerializer, WorkStepSerializer, WorkStepMaterialSerializer

from ..permissions.group_curators import IsMemberOfCuratorsGroup


class WorkBaseView(APIView):
    """
    Work base view
    """
    permission_classes = (IsAuthenticated, IsMemberOfCuratorsGroup,)  # TODO Change behavior when student app will be developed

    def get_work(self, pk):
        try:
            return Work.objects.get(pk=pk)
        except Work.DoesNotExist:
            raise Http404

    def get_related_step(self, work: Work, step_id: int):
        try:
            return work.step_set.get(pk=step_id)
        except WorkStep.DoesNotExist:
            raise Http404


class WorkList(WorkBaseView):
    """
    Methods: GET
    Description: List of works
    """

    def get(self, request):
        """
        READ: Work list
        :return: json of work list
        """
        works = Work.objects.all()
        serializer = WorkSerializer(works, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkDetail(WorkBaseView):
    """
    Methods: GET
    Description: Work details
    """

    def get(self, request, work_id):
        """
        READ: Work details
        :return: json of Work
        """
        work = self.get_work(work_id)
        serializer = WorkSerializer(work)
        return Response(serializer.data)


# related steps
class WorkStepList(WorkBaseView):
    """
    Methods: GET
    Description: Work related steps
    """
    def get(self, request, work_id):
        """
        READ: Work steps list
        :return: json of work steps list
        """
        work = self.get_work(work_id)
        serializer = WorkStepSerializer(work.step_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkStepDetail(WorkBaseView):
    """
    Methods: GET
    Description: Work related step details
    """
    def get(self, request, work_id, step_id):
        """
        READ: Work related step details
        :return: json of work related step
        """
        work = self.get_work(work_id)
        step = self.get_related_step(work, step_id)
        serializer = WorkStepSerializer(step)
        return Response(serializer.data, status=status.HTTP_200_OK)


# related step-materials
class WorkStepMaterialList(WorkBaseView):
    """
    Methods: GET
    Description: Work step related materials
    """

    def get(self, request, work_id, step_id):
        """
        READ: Work steps materials list
        :return: json of work step materials list
        """
        work = self.get_work(work_id)
        step = self.get_related_step(work, step_id)
        serializer = WorkStepMaterialSerializer(step.material_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
