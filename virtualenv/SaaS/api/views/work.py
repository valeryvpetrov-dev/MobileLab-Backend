from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from ..models.work import Work

from ..serializers.work import WorkSerializer, WorkStepSerializer, WorkStepMaterialSerializer


class WorkBaseView(APIView):
    """
    Work base view
    """
    def get_work(self, pk):
        try:
            return Work.objects.get(pk=pk)
        except Work.DoesNotExist:
            raise Http404

    def get_related_step(self, work: Work, step_id: int):
        try:
            return work.step_set.get(pk=step_id)
        except Work.DoesNotExist:
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
    Methods: GET, PUT
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

    def put(self, request, work_id):
        """
        UPDATE: Work details
        :param request: json of updated work
        :param work_id:
        :return: json of updated work
        """
        work = self.get_work(work_id)
        serializer = WorkSerializer(Work, data=request.data)
        if serializer.is_valid():
            serializer.update(work, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    Methods: GET, PUT
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

    def put(self, request, work_id, step_id):
        """
        UPDATE: Work related step details
        :param request: json of updated step
        :param work_id:
        :param step_id:
        :return: json of updated work related step
        """
        work = self.get_work(work_id)
        step = self.get_related_step(work, step_id)
        serializer = WorkSerializer(step, data=request.data, many=True)
        if serializer.is_valid():
            serializer.update(step, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # related steps
    class WorkStepList(WorkBaseView):
        """
        Methods: GET
        Description: Work related steps
        """

        def get(self, request, work_id):
            """
            READ: Work steps list
            :return: json of Work steps list
            """
            work = self.get_work(work_id)
            serializer = WorkStepSerializer(work.step_set, many=True)
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
