from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.authentication import TokenAuthentication

from ..models.work import Work, WorkStep

from ..serializers.work import WorkSerializerRelatedID, WorkSerializerRelatedIntermediate, \
    WorkStepSerializer, WorkStepMaterialSerializer

from ..permissions.group_curators import IsMemberOfCuratorsGroup


class WorkBaseViewAbstract:
    """
    Work base view
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMemberOfCuratorsGroup,)  # TODO Change behavior when student app will be developed

    def get_work(self, pk):
        return get_object_or_404(Work, pk=pk)

    def get_related_step(self, work: Work, step_id: int):
        return get_object_or_404(work.step_set, pk=step_id)


class WorkBaseView(WorkBaseViewAbstract, GenericAPIView):
    pass


class WorkList(WorkBaseViewAbstract, ListAPIView):
    """
    get:
    READ - List of works.
    """
    queryset = Work.objects.all()
    serializer_class = WorkSerializerRelatedID


class WorkDetail(WorkBaseView):
    """
    get:
    READ - Work instance details.
    """
    def get(self, request, work_id):
        work = self.get_work(work_id)
        serializer = WorkSerializerRelatedIntermediate(work)
        return Response(serializer.data)


# related steps
class WorkStepList(WorkBaseView):
    """"
    get:
    READ - Work instance related steps.
    """
    def get(self, request, work_id):
        work = self.get_work(work_id)
        serializer = WorkStepSerializer(work.step_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkStepDetail(WorkBaseView):
    """"
    get:
    READ - Work instance related step details.
    """
    def get(self, request, work_id, step_id):
        work = self.get_work(work_id)
        step = self.get_related_step(work, step_id)
        serializer = WorkStepSerializer(step)
        return Response(serializer.data, status=status.HTTP_200_OK)


# related step-materials
class WorkStepMaterialList(WorkBaseView):
    """"
    get:
    READ - Work instance related step materials.
    """
    def get(self, request, work_id, step_id):
        work = self.get_work(work_id)
        step = self.get_related_step(work, step_id)
        serializer = WorkStepMaterialSerializer(step.material_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
