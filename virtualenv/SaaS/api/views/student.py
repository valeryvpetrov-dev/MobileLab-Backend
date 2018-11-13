from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from ..models.student import Student
from ..models.work import Work, WorkStep

from ..serializers.student import StudentSerializerSkillsIntermediate, StudentSerializerSkillsID
from ..serializers.skill import SkillSerializer
from ..serializers.work import WorkSerializer, WorkStepSerializer, WorkStepMaterialSerializer, WorkStepCommentSerializer
from ..serializers.theme import ThemeSerializerRelatedID, ThemeSerializerRelatedIntermediate
from ..serializers.suggestion import SuggestionThemeSerializer, SuggestionThemeCommentSerializer


class StudentBaseView(APIView):
    """
    Student base view
    """
    def get_student(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get_related_work(self, student: Student, work_id: int):
        for theme in student.theme_set.all():
            try:
                work = theme.work_set.get(pk=work_id)
                return work
            except Work.DoesNotExist:
                pass
        return None

    def get_related_step(self, related_work: Work, step_id: int):
        try:
            step = related_work.step_set.get(pk=step_id)
            return step
        except WorkStep.DoesNotExist:
            pass
        return None

    def get_related_theme(self, student: Student, theme_id: int):
        for theme in student.theme_set.all():
            if theme.id == theme_id:
                return theme
        return None

    def get_related_suggestion(self, student: Student, suggestion_id: int):
        for suggestion in student.suggestiontheme_set.all():
            if suggestion.id == suggestion_id:
                return suggestion
        return None


class StudentList(StudentBaseView):
    """
    Methods: GET
    Description: List of students
    """
    def get(self, request):
        """
        READ: Student list
        :return: json of Student list
        """
        students = Student.objects.all()
        serializer = StudentSerializerSkillsIntermediate(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentDetail(StudentBaseView):
    """
    Methods: GET, PUT
    Description: Student details
    """
    def get(self, request, student_id):
        """
        READ: Student details
        :return: json of student
        """
        student = self.get_student(student_id)
        serializer = StudentSerializerSkillsIntermediate(student)
        return Response(serializer.data)

    def put(self, request, student_id):
        """
        UPDATE: Student details
        :param request: json of updated student
        :param student_id:
        :return: json of updated student
        """
        student = self.get_student(student_id)
        serializer = StudentSerializerSkillsID(student, data=request.data)
        if serializer.is_valid():
            serializer.update(student, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related skills
class StudentSkillList(StudentBaseView):
    """
    Methods: GET
    Description: Student related skills
    """
    def get(self, request, student_id):
        """
        READ: Student skills list
        :return: json of student skills list
        """
        student = self.get_student(student_id)
        serializer = SkillSerializer(student.skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# related works
class StudentWorkList(StudentBaseView):
    """
    Methods: GET, POST
    Description: Student related works
    """
    def get(self, request, student_id):
        """
        READ: Student works list
        :return: json of student works list
        """
        student = self.get_student(student_id)
        related_works = []
        for theme in student.theme_set.all():
            for work in theme.work_set.all():
                related_works.append(work)
        serializer = WorkSerializer(related_works, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id):
        """
        CREATE: Student work
        :param request: json of new work
        :param student_id:
        :return: json of created work
        """
        student = self.get_student(student_id)
        serializer = WorkSerializer(data=request.data)
        if serializer.is_valid():
            work = serializer.create(validated_data=serializer.validated_data)
            student.theme_set.add(work.theme)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentWorkDetail(StudentBaseView):
    """
    Methods: GET, PUT
    Description: Student related work details
    """
    def get(self, request, student_id, work_id):
        """
        READ: Student related work details
        :return: json of student related work
        """
        student = self.get_student(student_id)
        work = self.get_related_work(student, work_id)
        if work:
            serializer = WorkSerializer(work)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, student_id, work_id):
        """
        UPDATE: Student related work details
        :param request: json of updated work
        :param student_id:
        :param work_id:
        :return: json of updated student related work
        """
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
    Methods: GET, POST
    Description: Student related work steps
    """
    def get(self, request, student_id, work_id):
        """
        READ: Student related work steps list
        :return: json of student related work steps list
        """
        work = self.get_related_work(self.get_student(student_id), work_id)
        related_steps = []
        for step in work.step_set.all():
            related_steps.append(step)
        serializer = WorkStepSerializer(related_steps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, work_id):
        """
        CREATE: Student related work step
        :param request: json of new step
        :param student_id:
        :param work_id:
        :return: json of new step
        """
        work = self.get_related_work(self.get_student(student_id), work_id)
        serializer = WorkStepSerializer(data=request.data)
        if serializer.is_valid():
            step = serializer.create(validated_data=serializer.validated_data)
            work.step_set.add(step)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentWorkStepDetail(StudentBaseView):
    """
    Methods: GET, PUT
    Description: Student related work step details
    """
    def get(self, request, student_id, work_id, step_id):
        """
        READ: Student related work step details
        :return: json of student related work step
        """
        student = self.get_student(student_id)
        related_work = self.get_related_work(student, work_id)
        step = self.get_related_step(related_work, step_id)
        if step:
            serializer = WorkStepSerializer(step)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, student_id, work_id, step_id):
        """
        UPDATE: Student related work step details
        :param request: json of updated work step
        :param student_id:
        :param work_id:
        :param step_id:
        :return: json of updated student related work step
        """
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
    Methods: GET, POST
    Description: Student related work step materials
    """
    def get(self, request, student_id, work_id, step_id):
        """
        READ: Student related work step materials list
        :return: json of student related work steps materials list
        """
        student = self.get_student(student_id)
        related_work = self.get_related_work(student, work_id)
        step = self.get_related_step(related_work, step_id)
        related_materials = []
        for material in step.material_set.all():
            related_materials.append(material)
        serializer = WorkStepMaterialSerializer(related_materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, work_id, step_id):
        """
        CREATE: Student related work step material
        :param request: json of new material
        :param student_id:
        :param work_id:
        :param step_id:
        :return: json of new material
        """
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
    Methods: GET, POST
    Description: Student related work step comments
    """
    def get(self, request, student_id, work_id, step_id):
        """
        READ: Student related work step comments list
        :return: json of student related work steps comments list
        """
        student = self.get_student(student_id)
        related_work = self.get_related_work(student, work_id)
        step = self.get_related_step(related_work, step_id)
        related_comments = []
        for comment in step.comment_set.all():
            related_comments.append(comment)
        serializer = WorkStepCommentSerializer(related_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, work_id, step_id):
        """
        CREATE: Student related work step comment
        :param request: json of new comment
        :param student_id:
        :param work_id:
        :param step_id:
        :return: json of new comment
        """
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
    Methods: GET, POST
    Description: Student related themes
    """
    def get(self, request, student_id):
        """
        READ: Student themes list
        :return: json of student themes list
        """
        student = self.get_student(student_id)
        serializer = ThemeSerializerRelatedIntermediate(student.theme_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id):
        """
        CREATE: Student theme
        :param request: json of new theme
        :param student_id:
        :return: json of created theme
        """
        student = self.get_student(student_id)
        serializer = ThemeSerializerRelatedIntermediate(data=request.data)
        if serializer.is_valid():
            theme = serializer.create(validated_data=serializer.validated_data)
            student.theme_set.add(theme)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentThemeDetail(StudentBaseView):
    """
    Methods: GET, PUT
    Description: Student related theme details
    """
    def get(self, request, student_id, theme_id):
        """
        READ: Student related theme details
        :return: json of student related theme
        """
        student = self.get_student(student_id)
        theme = self.get_related_theme(student, theme_id)
        if theme:
            serializer = ThemeSerializerRelatedIntermediate(theme)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, student_id, theme_id):
        """
        UPDATE: Student related theme details
        :param request: json of updated theme
        :param student_id:
        :param theme_id:
        :return: json of updated Student related theme
        """
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
    Methods: GET, POST
    Description: Student related suggestions
    """
    def get(self, request, student_id):
        """
        READ: Student suggestions list
        :return: json of student suggestions list
        """
        student = self.get_student(student_id)
        serializer = SuggestionThemeSerializer(student.suggestiontheme_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id):
        """
        CREATE: Student suggestion
        :param request: json of new suggestion
        :param student_id:
        :return: json of created suggestion
        """
        Student = self.get_student(student_id)
        serializer = SuggestionThemeSerializer(data=request.data)
        if serializer.is_valid():
            suggestion = serializer.create(validated_data=serializer.validated_data)
            Student.suggestiontheme_set.add(suggestion)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentSuggestionDetail(StudentBaseView):
    """
    Methods: GET, PUT
    Description: Student related suggestion details
    """
    def get(self, request, student_id, suggestion_id):
        """
        READ: Student related suggestion details
        :return: json of student related suggestion
        """
        student = self.get_student(student_id)
        suggestion = self.get_related_suggestion(student, suggestion_id)
        if suggestion:
            serializer = SuggestionThemeSerializer(suggestion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, student_id, suggestion_id):
        """
        UPDATE: Student related suggestion details
        :param request: json of updated suggestion
        :param student_id:
        :param suggestion_id:
        :return: json of updated student related suggestion
        """
        student = self.get_student(student_id)
        suggestion = self.get_related_suggestion(student, suggestion_id)
        serializer = SuggestionThemeSerializer(suggestion, data=request.data)
        if serializer.is_valid():
            serializer.update(suggestion, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related suggestion-comments
class StudentSuggestionCommentList(StudentBaseView):
    """
    Methods: GET, POST
    Description: Student related suggestion comments
    """
    def get(self, request, student_id, suggestion_id):
        """
        READ: Student suggestion comments list
        :return: json of student suggestion comments list
        """
        student = self.get_student(student_id)
        suggestion = self.get_related_suggestion(student, suggestion_id)
        serializer = SuggestionThemeCommentSerializer(suggestion.comment_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, student_id, suggestion_id):
        """
        CREATE: Student suggestion comment
        :param request: json of new comment
        :param student_id:
        :param suggestion_id:
        :return: json of created comment
        """
        student = self.get_student(student_id)
        suggestion = self.get_related_suggestion(student, suggestion_id)
        serializer = SuggestionThemeCommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.create(validated_data=serializer.validated_data)
            suggestion.comment_set.add(comment)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
