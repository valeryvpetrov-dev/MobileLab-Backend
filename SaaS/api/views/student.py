from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.authentication import TokenAuthentication

from ..models.theme import Theme
from ..models.suggestion import SuggestionTheme, SuggestionThemeStatus, SuggestionThemeProgress
from ..models.student import Student, Group
from ..models.work import Work, WorkStep

from ..serializers.student import StudentSerializerRelatedIntermediate, StudentSerializerNoSkills, StudentSerializerRelatedID, \
    GroupSerializer
from ..serializers.skill import SkillSerializer
from ..serializers.work import WorkSerializerRelatedID, WorkSerializerRelatedIntermediate, \
    WorkStepSerializer, WorkStepSerializerRelatedID, WorkStepSerializerRelatedIDNoStatus, \
    WorkStepMaterialSerializer, WorkStepMaterialSerializerNoRelated, \
    WorkStepCommentSerializer, WorkStepCommentSerializerNoRelated
from ..serializers.theme import ThemeSerializerRelatedID, ThemeSerializerRelatedIntermediate
from ..serializers.suggestion import \
    SuggestionThemeSerializerRelatedID, SuggestionThemeSerializerRelatedChangeable, SuggestionThemeSerializerRelatedIDNoProgress, \
    SuggestionThemeSerializerRelatedIntermediate, \
    SuggestionThemeProgressSerializer, \
    SuggestionThemeCommentSerializer, SuggestionThemeCommentSerializerNoRelated

from ..permissions.group_curators import IsMemberOfCuratorsGroup


class StudentBaseViewAbstract:
    """
    Student base view
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMemberOfCuratorsGroup,)  # TODO Change behavior when student app will be developed

    def get_student(self, student_id: int) -> Student:
        return get_object_or_404(Student, pk=student_id)

    def get_related_work(self, student_id: int, work_id: int) -> Work:
        return get_object_or_404(Work, theme__student__id=student_id, pk=work_id)

    def get_related_step(self, student_id: int, work_id: int, step_id: int) -> WorkStep:
        return get_object_or_404(WorkStep, work__theme__student__id=student_id, work_id=work_id, pk=step_id)

    def get_related_theme(self, student_id: int, theme_id: int) -> Theme:
        return get_object_or_404(Theme, student__id=student_id, pk=theme_id)

    def get_related_suggestion(self, student_id: int, suggestion_id: int) -> SuggestionTheme:
        return get_object_or_404(SuggestionTheme, student__id=student_id, pk=suggestion_id)

    def get_related_suggestion_progress(self, student_id: int, suggestion_id: int) -> SuggestionThemeProgress:
        suggestion = self.get_related_suggestion(student_id, suggestion_id)
        return get_object_or_404(SuggestionThemeProgress, suggestion=suggestion)


class StudentBaseView(StudentBaseViewAbstract, GenericAPIView):
    pass


class StudentGroupList(StudentBaseViewAbstract, ListAPIView):
    """
    get:
    READ - List of academic groups.
    """
    permission_classes = (IsAuthenticated, )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


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
    serializer_class = StudentSerializerRelatedID

    @permission_classes((IsAuthenticated, IsMemberOfCuratorsGroup, ))   # TODO Change behavior when student app will be developed
    def get(self, request, student_id):
        student = self.get_student(student_id)
        serializer = StudentSerializerRelatedIntermediate(student)
        return Response(serializer.data)

    def put(self, request, student_id):
        student = self.get_student(student_id)
        serializer = StudentSerializerRelatedID(student, data=request.data)
        if serializer.is_valid():
            serializer.update(student, validated_data=serializer.validated_data)
            # serializing response
            serializer_resp = StudentSerializerRelatedIntermediate(student)
            return Response(serializer_resp.data, status=status.HTTP_202_ACCEPTED)
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
    serializer_class = WorkSerializerRelatedID

    @permission_classes((IsAuthenticated, IsMemberOfCuratorsGroup, )) # TODO Change behavior when student app will be developed
    def get(self, request, student_id):
        student = self.get_student(student_id)
        related_works = []
        for theme in student.theme_set.all():
            for work in theme.work_set.all():
                related_works.append(work)
        serializer = WorkSerializerRelatedIntermediate(related_works, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentWorkDetail(StudentBaseView):
    """
    get:
    READ - Student instance related work.

    put:
    UPDATE - Student instance related work.
    """
    serializer_class = WorkSerializerRelatedID

    @permission_classes((IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, work_id):
        work = self.get_related_work(student_id, work_id)
        serializer = WorkSerializerRelatedIntermediate(work)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, student_id, work_id):
        work = self.get_related_work(student_id, work_id)
        serializer = WorkSerializerRelatedID(work, data=request.data)
        if serializer.is_valid():
            serializer.update(work, validated_data=serializer.validated_data)
            # serializing response
            serializer_resp = WorkSerializerRelatedIntermediate(work)
            return Response(serializer_resp.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related work-steps
class StudentWorkStepList(StudentBaseView):
    """
    get:
    READ - Student instance related work steps.

    post:
    CREATE - Student instance related work step.
    """
    serializer_class = WorkStepSerializerRelatedID

    @permission_classes((IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, work_id):
        work = self.get_related_work(student_id, work_id)
        related_steps = []
        for step in work.step_set.all():
            related_steps.append(step)
        serializer = WorkStepSerializer(related_steps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, work_id):
        work = self.get_related_work(student_id, work_id)
        serializer = WorkStepSerializerRelatedID(data=request.data)
        if serializer.is_valid():
            step = serializer.create(validated_data=serializer.validated_data)
            work.step_set.add(step)
            # serializing response
            serializer_resp = WorkStepSerializer(step)
            return Response(serializer_resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentWorkStepDetail(StudentBaseView):
    """
    get:
    READ - Student instance related work step details.

    put:
    UPDATE - Student instance related work step details.
    """
    serializer_class = WorkStepSerializerRelatedID

    @permission_classes((IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, work_id, step_id):
        step = self.get_related_step(student_id, work_id, step_id)
        serializer = WorkStepSerializer(step)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, student_id, work_id, step_id):
        step = self.get_related_step(student_id, work_id, step_id)
        serializer = WorkStepSerializerRelatedID(step, data=request.data)
        if serializer.is_valid():
            serializer.update(step, validated_data=serializer.validated_data)
            # serializing response
            serializer_resp = WorkStepSerializer(step)
            return Response(serializer_resp.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related work-step-materials
class StudentWorkStepMaterialList(StudentBaseView):
    """
    get:
    READ - Student instance related work step materials.

    post:
    CREATE - Student instance related work step material.
    """
    serializer_class = WorkStepMaterialSerializerNoRelated

    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, work_id, step_id):
        step = self.get_related_step(student_id, work_id, step_id)
        related_materials = []
        for material in step.material_set.all():
            related_materials.append(material)
        serializer = WorkStepMaterialSerializer(related_materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, work_id, step_id):
        step = self.get_related_step(student_id, work_id, step_id)
        serializer = WorkStepMaterialSerializerNoRelated(data=request.data)
        if serializer.is_valid():
            material = serializer.create(validated_data=serializer.validated_data)
            step.material_set.add(material)
            # serializing response
            serializer_resp = WorkStepMaterialSerializer(step)
            return Response(serializer_resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related work-step-comments
class StudentWorkStepCommentList(StudentBaseView):
    """
    get:
    READ - Student instance related work step comments.

    post:
    CREATE - Student instance related work step comment.
    """
    serializer_class = WorkStepCommentSerializerNoRelated

    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, work_id, step_id):
        step = self.get_related_step(student_id, work_id, step_id)
        related_comments = []
        for comment in step.comment_set.all():
            related_comments.append(comment)
        serializer = WorkStepCommentSerializer(related_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, work_id, step_id):
        step = self.get_related_step(student_id, work_id, step_id)
        serializer = WorkStepCommentSerializerNoRelated(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["step_id"] = step_id
            comment = serializer.create(validated_data=serializer.validated_data)
            step.comment_set.add(comment)
            # serializing response
            serializer_resp = WorkStepCommentSerializer(comment)
            return Response(serializer_resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related themes
class StudentThemeList(StudentBaseView):
    """
    get:
    READ - Student instance related themes.

    post:
    CREATE - Student instance related theme.
    """
    serializer_class = ThemeSerializerRelatedID

    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id):
        student = self.get_student(student_id)
        serializer = ThemeSerializerRelatedIntermediate(student.theme_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id):
        student = self.get_student(student_id)
        serializer = ThemeSerializerRelatedID(data=request.data)
        if serializer.is_valid():
            theme = serializer.create(validated_data=serializer.validated_data)
            student.theme_set.add(theme)
            # serializing response
            serializer_resp = ThemeSerializerRelatedIntermediate(theme)
            return Response(serializer_resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentThemeDetail(StudentBaseView):
    """
    get:
    READ - Student instance related theme details.

    put:
    UPDATE - Student instance related theme details.
    """
    serializer_class = SuggestionThemeSerializerRelatedChangeable

    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, theme_id):
        theme = self.get_related_theme(student_id, theme_id)
        if theme:
            serializer = ThemeSerializerRelatedIntermediate(theme)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, student_id, theme_id):
        theme = self.get_related_theme(student_id, theme_id)
        serializer = SuggestionThemeSerializerRelatedChangeable(theme, data=request.data)
        if serializer.is_valid():
            serializer.update(theme, validated_data=serializer.validated_data)
            # serializing response
            serializer_resp = ThemeSerializerRelatedIntermediate(theme)
            return Response(serializer_resp.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related suggestions
class StudentSuggestionList(StudentBaseView):
    """
    get:
    READ - Student instance related suggestions.

    post:
    CREATE - Student instance related suggestion.
    """
    serializer_class = SuggestionThemeSerializerRelatedIDNoProgress

    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id):
        student = self.get_student(student_id)
        serializer = SuggestionThemeSerializerRelatedIntermediate(student.suggestiontheme_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id):
        student = self.get_student(student_id)
        serializer = SuggestionThemeSerializerRelatedIDNoProgress(data=request.data)
        if serializer.is_valid():
            suggestion = serializer.create(validated_data=serializer.validated_data)
            student.suggestiontheme_set.add(suggestion)
            # serializing response
            serializer_resp = SuggestionThemeSerializerRelatedIntermediate(suggestion)
            return Response(serializer_resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentSuggestionDetail(StudentBaseView):
    """
    get:
    READ - Student instance related suggestion details.

    put:
    UPDATE - Student instance related suggestion details.
    """
    serializer_class = SuggestionThemeSerializerRelatedIDNoProgress

    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, suggestion_id):
        suggestion = self.get_related_suggestion(student_id, suggestion_id)
        if suggestion:
            serializer = SuggestionThemeSerializerRelatedIntermediate(suggestion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, student_id, suggestion_id):
        suggestion = self.get_related_suggestion(student_id, suggestion_id)
        serializer = SuggestionThemeSerializerRelatedIDNoProgress(suggestion, data=request.data)
        if serializer.is_valid():
            serializer.update(suggestion, validated_data=serializer.validated_data)
            # serializing response
            serializer_resp = SuggestionThemeSerializerRelatedIntermediate(suggestion)
            return Response(serializer_resp.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentSuggestionProgressDetail(StudentBaseView):
    """
    get:
    READ - Student instance related suggestion progress details.

    put:
    UPDATE - Student instance related suggestion progress details.
    """
    serializer_class = SuggestionThemeProgressSerializer

    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, suggestion_id):
        progress = self.get_related_suggestion_progress(student_id, suggestion_id)
        serializer = SuggestionThemeProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, student_id, suggestion_id):
        progress = self.get_related_suggestion_progress(student_id, suggestion_id)
        serializer = SuggestionThemeProgressSerializer(progress, data=request.data)
        if serializer.is_valid():
            serializer.update(progress, validated_data=serializer.validated_data)
            # serializing response
            serializer_resp = SuggestionThemeProgressSerializer(progress)
            return Response(serializer_resp.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related suggestion-comments
class StudentSuggestionCommentList(StudentBaseView):
    """
    get:
    READ - Student instance related suggestion comments.

    post:
    CREATE - Student instance related suggestion comment.
    """
    serializer_class = SuggestionThemeCommentSerializerNoRelated

    @permission_classes(
        (IsAuthenticated, IsMemberOfCuratorsGroup,))  # TODO Change behavior when student app will be developed
    def get(self, request, student_id, suggestion_id):
        suggestion = self.get_related_suggestion(student_id, suggestion_id)
        serializer = SuggestionThemeCommentSerializer(suggestion.comment_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, suggestion_id):
        suggestion = self.get_related_suggestion(student_id, suggestion_id)
        serializer = SuggestionThemeCommentSerializerNoRelated(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["suggestion_id"] = suggestion_id
            comment = serializer.create(validated_data=serializer.validated_data)
            suggestion.comment_set.add(comment)
            # serializing response
            serializer_resp = SuggestionThemeCommentSerializer(comment)
            return Response(serializer_resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
