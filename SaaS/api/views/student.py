from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication

from django.http import Http404

from ..models.theme import Theme
from ..models.suggestion import SuggestionTheme
from ..models.student import Student
from ..models.work import Work, WorkStep

from ..serializers.student import StudentSerializerSkillsIntermediate, StudentSerializerNoSkills, StudentSerializerSkillsID
from ..serializers.skill import SkillSerializer
from ..serializers.work import WorkSerializer, WorkSerializerRelatedIntermediate, \
    WorkStepSerializer, WorkStepMaterialSerializer, WorkStepCommentSerializer
from ..serializers.theme import ThemeSerializerRelatedID, ThemeSerializerRelatedIntermediate
from ..serializers.suggestion import SuggestionThemeSerializerRelatedID, SuggestionThemeSerializerRelatedIntermediate, \
    SuggestionThemeCommentSerializer

from ..permissions.group_curators import IsMemberOfCuratorsGroup


class StudentBaseViewAbstract:
    """
    Student base view
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMemberOfCuratorsGroup,)  # TODO Change behavior when student app will be developed

    def get_student(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get_related_work(self, student: Student, work_id: int):
        work = None
        for theme in student.theme_set.all():
            try:
                work = theme.work_set.get(pk=work_id)
            except Work.DoesNotExist:
                pass
        if not work: raise Http404
        return work

    def get_related_step(self, related_work: Work, step_id: int):
        try:
            return related_work.step_set.get(pk=step_id)
        except WorkStep.DoesNotExist:
            raise Http404

    def get_related_theme(self, student: Student, theme_id: int):
        try:
            return student.theme_set.get(pk=theme_id)
        except Theme.DoesNotExist:
            raise Http404

    def get_related_suggestion(self, student: Student, suggestion_id: int):
        try:
            return student.suggestiontheme_set.get(pk=suggestion_id)
        except SuggestionTheme.DoesNotExist:
            raise Http404


class StudentBaseView(StudentBaseViewAbstract, APIView):
    pass


class StudentList(StudentBaseViewAbstract, ListAPIView):
    """
    get:
    READ - List of students.
    """
    permission_classes = (IsAuthenticated, IsMemberOfCuratorsGroup, )   # TODO Change behavior when student app will be developed
    queryset = Student.objects.all()
    serializer_class = StudentSerializerNoSkills


class StudentDetail(StudentBaseView):
    """
    get:
    READ - Student instance details.

    put:
    UPDATE - Student instance details.
    """
    @permission_classes((IsAuthenticated, IsMemberOfCuratorsGroup, ))   # TODO Change behavior when student app will be developed
    def get(self, request, student_id):
        student = self.get_student(student_id)
        serializer = StudentSerializerSkillsIntermediate(student)
        return Response(serializer.data)

    def put(self, request, student_id):
        student = self.get_student(student_id)
        serializer = StudentSerializerSkillsID(student, data=request.data)
        if serializer.is_valid():
            serializer.update(student, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related skills
class StudentSkillList(StudentBaseView):
    """
    get:
    READ - List of student instance related skills.
    """
    permission_classes = (IsAuthenticated, IsMemberOfCuratorsGroup,)  # TODO Change behavior when student app will be developed

    def get(self, request, student_id):
        student = self.get_student(student_id)
        serializer = SkillSerializer(student.skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# related works
class StudentWorkList(StudentBaseView):
    """
    get:
    READ - List of student instance related works.

    post:
    CREATE - Student instance related work.
    """
    @permission_classes((IsAuthenticated, IsMemberOfCuratorsGroup, )) # TODO Change behavior when student app will be developed
    def get(self, request, student_id):
        student = self.get_student(student_id)
        related_works = []
        for theme in student.theme_set.all():
            for work in theme.work_set.all():
                related_works.append(work)
        serializer = WorkSerializer(related_works, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id):
        student = self.get_student(student_id)
        serializer = WorkSerializer(data=request.data)
        if serializer.is_valid():
            work = serializer.create(validated_data=serializer.validated_data)
            student.theme_set.add(work.theme)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentWorkDetail(StudentBaseView):
    """
    get:
    READ - Student instance related work.

    put:
    UPDATE - Student instance related work.

    delete:
    DELETE - Student instance related work.
    """
    @permission_classes((IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, work_id):
        student = self.get_student(student_id)
        work = self.get_related_work(student, work_id)
        if work:
            serializer = WorkSerializerRelatedIntermediate(work)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, student_id, work_id):
        student = self.get_student(student_id)
        work = self.get_related_work(student, work_id)
        serializer = WorkSerializer(work, data=request.data)
        if serializer.is_valid():
            serializer.update(work, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related work-steps
class StudentWorkStepList(StudentBaseView):
    """
    get:
    READ - Student instance related work steps.

    post:
    CREATE - Student instance related work step.
    """
    @permission_classes((IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, work_id):
        work = self.get_related_work(self.get_student(student_id), work_id)
        related_steps = []
        for step in work.step_set.all():
            related_steps.append(step)
        serializer = WorkStepSerializer(related_steps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, work_id):
        work = self.get_related_work(self.get_student(student_id), work_id)
        serializer = WorkStepSerializer(data=request.data)
        if serializer.is_valid():
            step = serializer.create(validated_data=serializer.validated_data)
            work.step_set.add(step)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentWorkStepDetail(StudentBaseView):
    """
    get:
    READ - Student instance related work step details.

    put:
    UPDATE - Student instance related work step details.

    delete:
    DELETE - Student instance related work step.
    """
    @permission_classes((IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, work_id, step_id):
        student = self.get_student(student_id)
        related_work = self.get_related_work(student, work_id)
        step = self.get_related_step(related_work, step_id)
        if step:
            serializer = WorkStepSerializer(step)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, student_id, work_id, step_id):
        student = self.get_student(student_id)
        related_work = self.get_related_work(student, work_id)
        step = self.get_related_step(related_work, step_id)
        serializer = WorkStepSerializer(step, data=request.data)
        if serializer.is_valid():
            serializer.update(step, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related work-step-materials
class StudentWorkStepMaterialList(StudentBaseView):
    """
    get:
    READ - Student instance related work step materials.

    post:
    CREATE - Student instance related work step material.
    """
    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, work_id, step_id):
        student = self.get_student(student_id)
        related_work = self.get_related_work(student, work_id)
        step = self.get_related_step(related_work, step_id)
        related_materials = []
        for material in step.material_set.all():
            related_materials.append(material)
        serializer = WorkStepMaterialSerializer(related_materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, work_id, step_id):
        student = self.get_student(student_id)
        related_work = self.get_related_work(student, work_id)
        step = self.get_related_step(related_work, step_id)
        serializer = WorkStepMaterialSerializer(data=request.data)
        if serializer.is_valid():
            material = serializer.create(validated_data=serializer.validated_data)
            step.material_set.add(material)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related work-step-comments
class StudentWorkStepCommentList(StudentBaseView):
    """
    get:
    READ - Student instance related work step comments.

    post:
    CREATE - Student instance related work step comment.
    """
    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, work_id, step_id):
        student = self.get_student(student_id)
        related_work = self.get_related_work(student, work_id)
        step = self.get_related_step(related_work, step_id)
        related_comments = []
        for comment in step.comment_set.all():
            related_comments.append(comment)
        serializer = WorkStepCommentSerializer(related_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, work_id, step_id):
        student = self.get_student(student_id)
        related_work = self.get_related_work(student, work_id)
        step = self.get_related_step(related_work, step_id)
        serializer = WorkStepCommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.create(validated_data=serializer.validated_data)
            step.comment_set.add(comment)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related themes
class StudentThemeList(StudentBaseView):
    """
    get:
    READ - Student instance related themes.

    post:
    CREATE - Student instance related theme.
    """
    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id):
        student = self.get_student(student_id)
        serializer = ThemeSerializerRelatedID(student.theme_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id):
        student = self.get_student(student_id)
        serializer = ThemeSerializerRelatedID(data=request.data)
        if serializer.is_valid():
            theme = serializer.create(validated_data=serializer.validated_data)
            student.theme_set.add(theme)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentThemeDetail(StudentBaseView):
    """
    get:
    READ - Student instance related theme details.

    put:
    UPDATE - Student instance related theme details.

    delete:
    DELETE - Student instance related theme.
    """
    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, theme_id):
        student = self.get_student(student_id)
        theme = self.get_related_theme(student, theme_id)
        if theme:
            serializer = ThemeSerializerRelatedIntermediate(theme)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, student_id, theme_id):
        student = self.get_student(student_id)
        theme = self.get_related_theme(student, theme_id)
        serializer = ThemeSerializerRelatedID(theme, data=request.data)
        if serializer.is_valid():
            serializer.update(theme, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related suggestions
class StudentSuggestionList(StudentBaseView):
    """
    get:
    READ - Student instance related suggestions.

    post:
    CREATE - Student instance related suggestion.
    """
    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id):
        student = self.get_student(student_id)
        serializer = SuggestionThemeSerializerRelatedID(student.suggestiontheme_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id):
        student = self.get_student(student_id)
        serializer = SuggestionThemeSerializerRelatedID(data=request.data)
        if serializer.is_valid():
            suggestion = serializer.create(validated_data=serializer.validated_data)
            student.suggestiontheme_set.add(suggestion)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentSuggestionDetail(StudentBaseView):
    """
    get:
    READ - Student instance related suggestion details.

    put:
    UPDATE - Student instance related suggestion details.

    delete:
    DELETE - Student instance related suggestion.
    """
    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, suggestion_id):
        student = self.get_student(student_id)
        suggestion = self.get_related_suggestion(student, suggestion_id)
        if suggestion:
            serializer = SuggestionThemeSerializerRelatedIntermediate(suggestion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, student_id, suggestion_id):
        student = self.get_student(student_id)
        suggestion = self.get_related_suggestion(student, suggestion_id)
        serializer = SuggestionThemeSerializerRelatedID(suggestion, data=request.data)
        if serializer.is_valid():
            serializer.update(suggestion, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related suggestion-comments
class StudentSuggestionCommentList(StudentBaseView):
    """
    get:
    READ - Student instance related suggestion comments.

    post:
    CREATE - Student instance related suggestion comment.
    """
    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, suggestion_id):
        student = self.get_student(student_id)
        suggestion = self.get_related_suggestion(student, suggestion_id)
        serializer = SuggestionThemeCommentSerializer(suggestion.comment_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, suggestion_id):
        student = self.get_student(student_id)
        suggestion = self.get_related_suggestion(student, suggestion_id)
        serializer = SuggestionThemeCommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.create(validated_data=serializer.validated_data)
            suggestion.comment_set.add(comment)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
